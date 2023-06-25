from aiogram.filters.state import State, StatesGroup


class ChoiceCityWeather(StatesGroup):
    waiting_city: State = State()
    my_city: State = State()


class ReportsPages(StatesGroup):
    current_page: State = State()
    reports: State = State()
