from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from keyboards import get_main_menu_kb, get_menu_kb, get_reports_desk
from lexicon import BOT_BUTTONS, BOT_PHRASE, \
    get_weather_information, bot_welcome_phrase
from states import ChoiceCityWeather, ReportsPages
from api_requests import WeatherInCity
from filters import IsNextOrBackClick, IsNotCallClick, IsCityReport
from database import WeatherReports, add_city, create_report, \
    get_user_city, get_reports, get_report_city


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


@router.callback_query(IsNextOrBackClick(),
                       StateFilter(ReportsPages.current_page))
async def callback_query(callback: CallbackQuery, state: FSMContext) -> None:
    reports: list[WeatherReports] = get_reports(str(callback.from_user.id))
    data = await state.get_data()
    current_page: int = data.get('current_page')

    if callback.data == BOT_BUTTONS['next']:
        current_page += 1
    else:  # back_page
        current_page -= 1

    inline_kb: InlineKeyboardMarkup | None = get_reports_desk(
        reports, current_page)

    if not inline_kb:
        await callback.answer()
    else:
        await state.update_data(current_page=current_page)
        await callback.message.edit_text(
            text=BOT_PHRASE['history_of_queries'], reply_markup=inline_kb)


@router.callback_query(IsCityReport())
async def get_city_report(callback: CallbackQuery) -> None:
    report_id: int = int(callback.data.split('_')[1])
    report: WeatherReports = get_report_city(str(callback.from_user.id),
                                             report_id)

    weather_info: str = get_weather_information(report.temp, report.feels_like,
                                                str(report.wind_speed),
                                                str(report.pressure_mm))
    city_and_date: str = f'{report.city} ' + \
        f'{report.date.strftime("%d-%m-%Y")}'

    await callback.answer(text=f'{city_and_date}\n\n{weather_info}',
                          show_alert=True)


@router.callback_query(IsNotCallClick())
async def empty_answer(callback: CallbackQuery) -> None:
    await callback.answer()
