"""
    Handler-ы срабатывающие при появлении callback-ов
"""
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards import get_reports_desk
from lexicon import BOT_BUTTONS, BOT_PHRASE, get_weather_information
from states import ReportsPages
from filters import IsNextOrBackClick, IsNotCallClick, IsCityReport
from database import WeatherReports, get_reports, get_report_city

router: Router = Router()


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
        f'{report.date.strftime("%d-%m-%Y %H:%M:%S")}'

    await callback.answer(text=f'{city_and_date}\n\n{weather_info}',
                          show_alert=True)


@router.callback_query(IsNotCallClick())
async def empty_answer(callback: CallbackQuery) -> None:
    await callback.answer()
