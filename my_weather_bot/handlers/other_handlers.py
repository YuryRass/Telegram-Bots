from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from keyboards import get_main_menu_kb, get_menu_kb, get_reports_desk
from lexicon import BOT_BUTTONS, BOT_PHRASE, get_weather_information, \
    bot_welcome_phrase
from states import ChoiceCityWeather, ReportsPages
from api_requests import WeatherInCity
from database import WeatherReports, add_city, create_report, \
    get_user_city, get_reports


router: Router = Router()


@router.message(Text(text=BOT_BUTTONS['menu']))
async def show_main_menu(message: Message, state: FSMContext) -> None:
    await state.set_state(state=None)
    keyboard: ReplyKeyboardMarkup = get_main_menu_kb()
    text: str = bot_welcome_phrase(message.from_user.first_name)
    await message.answer(text=text, reply_markup=keyboard)


@router.message(Text(text=BOT_BUTTONS['weather_in_other_city']))
async def other_city_start(message: Message, state: FSMContext) -> None:
    menu_kb: ReplyKeyboardMarkup = get_menu_kb()
    await message.answer(text=BOT_PHRASE['input_city_name'],
                         reply_markup=menu_kb)
    await state.set_state(ChoiceCityWeather.waiting_city)


@router.message(StateFilter(ChoiceCityWeather.waiting_city))
async def show_weather_in_chosen_city(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=BOT_PHRASE['incorrect_name_of_city'])
        return
    await state.update_data(waiting_city=message.text)
    main_kb: ReplyKeyboardMarkup = get_main_menu_kb()
    city = await state.get_data()
    weather_in_city: WeatherInCity = WeatherInCity(city.get('waiting_city'))
    data = weather_in_city.get_weather()
    info: str = f'Погода в городе {city.get("waiting_city")}\n' + \
        get_weather_information(data["temp"], data["feels_like"],
                                data["wind_speed"], data["pressure_mm"])
    create_report(str(message.from_user.id), int(data["temp"]),
                  int(data["feels_like"]), int(data["wind_speed"]),
                  int(data["pressure_mm"]), city.get("waiting_city"))
    await message.answer(text=info, reply_markup=main_kb)
    await state.set_state(state=None)


@router.message(Text(text=BOT_BUTTONS['set_your_city']))
async def my_city_start(message: Message, state: FSMContext) -> None:
    menu_kb: ReplyKeyboardMarkup = get_menu_kb()
    await message.answer(text=BOT_PHRASE['input_your_city_name'],
                         reply_markup=menu_kb)
    await state.set_state(ChoiceCityWeather.my_city)


@router.message(Text(text=BOT_BUTTONS['history']), StateFilter(default_state))
async def update_current_page(message: Message, state: FSMContext):
    reports: list[WeatherReports] = get_reports(str(message.from_user.id))
    inline_kb: InlineKeyboardMarkup = get_reports_desk(reports, 1)
    await message.answer(text=BOT_PHRASE['history_of_queries'],
                         reply_markup=inline_kb)
    await state.set_state(state=ReportsPages.current_page)
    await state.update_data(current_page=1)


@router.message(StateFilter(ChoiceCityWeather.my_city))
async def my_city_input(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer(text=BOT_PHRASE['incorrect_name_of_city'])
        return
    await state.update_data(my_city=message.text)
    keyboard: ReplyKeyboardMarkup = get_main_menu_kb()
    city = await state.get_data()
    my_city: str = city.get('my_city')
    text: str = f'Отлично! Ваш город: {my_city}\n'
    add_city(str(message.from_user.id), my_city)
    await message.answer(text=text, reply_markup=keyboard)
    await state.set_state(state=None)


@router.message(Text(text=BOT_BUTTONS['weather_in_my_city']))
async def show_weather_in_my_city(message: Message, state: FSMContext) -> None:
    my_city: str = get_user_city(str(message.from_user.id))
    keyboard: ReplyKeyboardMarkup = get_main_menu_kb()
    if not my_city:
        await message.answer(text=BOT_PHRASE['set_city_warning'],
                             reply_markup=keyboard)
        return
    weather_in_city: WeatherInCity = WeatherInCity(my_city)
    data = weather_in_city.get_weather()
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
