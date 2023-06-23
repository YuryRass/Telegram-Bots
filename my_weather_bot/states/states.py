from aiogram.filters.state import State, StatesGroup


class ChoiceCityWeather(StatesGroup):
    waiting_city: State = State()
    my_city: State = State()
