from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from handlers import get_main_menu, bot_welcome_phrase
from lexicon import BOT_BUTTONS, BOT_PHRASE, get_weather_information
from states import ChoiceCityWeather
from api_requests import get_weather
from database import add_city, create_report, get_user_city


router: Router = Router()


@router.message(Text(text=BOT_BUTTONS['menu']))
async def show_main_menu(message: Message, state: FSMContext) -> None:
    await state.set_state(state=None)
    keyboard: ReplyKeyboardMarkup = await get_main_menu()
    text: str = await bot_welcome_phrase(message.from_user.first_name)
    await message.answer(text=text, reply_markup=keyboard)


@router.message(Text(text=BOT_BUTTONS['weather_in_other_city']),
                StateFilter(default_state))
async def other_city_start(message: Message, state: FSMContext) -> None:
    menu_btn = KeyboardButton(text=BOT_BUTTONS['menu'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[menu_btn]],
                                                        resize_keyboard=True)
    await message.answer(text=BOT_PHRASE['input_city_name'],
                         reply_markup=keyboard)
    await state.set_state(ChoiceCityWeather.waiting_city)


@router.message(StateFilter(ChoiceCityWeather.waiting_city))
async def show_weather_in_chosen_city(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=BOT_PHRASE['incorrect_name_of_city'])
        return
    await state.update_data(waiting_city=message.text)
    keyboard: ReplyKeyboardMarkup = await get_main_menu()
    city = await state.get_data()
    data = get_weather(city.get('waiting_city'))
    info: str = f'Погода в городе {city.get("waiting_city")}\n' + \
        get_weather_information(data["temp"], data["feels_like"],
                                data["wind_speed"], data["pressure_mm"])
    create_report(str(message.from_user.id), int(data["temp"]),
                  int(data["feels_like"]), int(data["wind_speed"]),
                  int(data["pressure_mm"]), city.get("waiting_city"))
    await message.answer(text=info, reply_markup=keyboard)
    await state.set_state(state=None)


@router.message(Text(text=BOT_BUTTONS['set_your_city']))
async def my_city_start(message: Message, state: FSMContext) -> None:
    menu_btn = KeyboardButton(text=BOT_BUTTONS['menu'])
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[menu_btn]],
                                                        resize_keyboard=True)
    await message.answer(text=BOT_PHRASE['input_your_city_name'],
                         reply_markup=keyboard)
    await state.set_state(ChoiceCityWeather.my_city)


@router.message(StateFilter(ChoiceCityWeather.my_city))
async def my_city_input(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=BOT_PHRASE['incorrect_name_of_city'])
        return
    await state.update_data(my_city=message.text)
    keyboard: ReplyKeyboardMarkup = await get_main_menu()
    city = await state.get_data()
    my_city: str = city.get('my_city')
    text: str = f'Отлично! Ваш город: {my_city}\n'
    add_city(str(message.from_user.id), my_city)
    await message.answer(text=text, reply_markup=keyboard)
    await state.set_state(state=None)


@router.message(Text(text=BOT_BUTTONS['weather_in_my_city']))
async def show_weather_in_my_city(message: Message, state: FSMContext) -> None:
    my_city: str = get_user_city(str(message.from_user.id))
    keyboard: ReplyKeyboardMarkup = await get_main_menu()
    if not my_city:
        await message.answer(text=BOT_PHRASE['set_city_warning'],
                             reply_markup=keyboard)
        return
    data = get_weather(my_city)
    if data:
        create_report(str(message.from_user.id), int(data["temp"]),
                      int(data["feels_like"]), int(data["wind_speed"]),
                      int(data["pressure_mm"]), my_city)
        info: str = f'Погода в вашем городе {my_city}\n' + \
            get_weather_information(data["temp"], data["feels_like"],
                                    data["wind_speed"], data["pressure_mm"])
        await message.answer(text=info, reply_markup=keyboard)
    else:
        text: str = f"{BOT_PHRASE['not_such_city']}: {my_city}"
        await message.answer(text=text, reply_markup=keyboard)
