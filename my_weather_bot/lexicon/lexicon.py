BOT_PHRASE: dict[str, str] = {
    'welcome': 'я бот, который расскажет тебе о погоде на сегодня',
    'inability': 'Я пока так не умею :-(',
    'incorrect_name_of_city': 'Названия городов пишутся с большой буквы',
    'input_city_name': 'Введите название города',
    'input_your_city_name': 'Введите название города, в котором Вы находитесь',
    'set_city_warning': 'Установите сначала город, в котором находитесь',
    'not_such_city': 'Не удалось найти информацию по данному городу'
}

BOT_BUTTONS: dict[str, str] = {
    'weather_in_my_city': 'Погода в моем городе',
    'weather_in_other_city': 'Погода в другом городе',
    'history': 'История',
    'set_your_city': 'Установить свой город',
    'menu': 'Меню'
}


def get_weather_information(temp: str, feels_like: str,
                            wind_speed: str, pressure_mm: str) -> str:
    return f'Температура: {temp} C\n' + \
        f'Ощущается как: {feels_like} C \n' + \
        f'Скорость ветра: {wind_speed}м/с\n' + \
        f'Давление: {pressure_mm}мм'


def bot_welcome_phrase(first_name: str):
    return f'Привет {first_name}, ' + BOT_PHRASE['welcome']