"""
Модуль orm.py предназначен для подключения к базе данных PostgreSQL,
создания таблиц, извлечения и добавления данных в таблицы
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import load_config, Config
from database import Base, User, WeatherReports

config: Config = load_config()  # загрузка конфиг. данных
engine = create_engine(url=f'postgresql://{config.db.user_name}:' +
                       f'{config.db.user_passsword}@{config.db.address}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_user(tg_id: str) -> None:
    """
    Добавление пользователя в таблицу User, в случае его отсутсвия там
    Аргумент tg_id: str - идентификатор пользователя в телеграме
    """
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        session.commit()


def add_city(tg_id: str, city: str) -> None:
    """
    Добавление нового города в таблицу User
    Аргументы:
    1. tg_id: str - идентификатор пользователя в телеграме
    2. city: str - название города
    """
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.city = city
    session.commit()


def create_report(tg_id: str, temp: int, feels_like: int,
                  wind_speed: int, pressure_mm: int, city: str) -> None:
    """
    Добавление в таблицу WeatherReports информации о погоде
    Аргументы:
        tg_id: str - идентификатор пользователя в телеграме,
    который захотел узнать информацию о погоде
        temp: int - температура в городе
        feels_like: int - температура в городе по ощущениям
        wind_speed: int - скорость ветра
        pressure_mm: int - атм. давление
        city: str - название города
    """
    user: User = session.query(User).filter(User.tg_id == tg_id).first()
    new_report = WeatherReports(temp=temp, owner=user.user_id,
                                feels_like=feels_like, wind_speed=wind_speed,
                                pressure_mm=pressure_mm, city=city)
    session.add(new_report)
    session.commit()


def get_user_city(tg_id: str) -> str | None:
    """
    Возвращает название города, за которым закрпелен пользователь Telegram-а
    Атрибут tg_id: str - идентификатор пользователя в телеграме
    """
    user: User = session.query(User).filter(User.tg_id == tg_id).first()
    return user.city


def get_reports(tg_id: str) -> list[WeatherReports]:
    """
    Получение отчетной информации о погоде для все городов,
    которые запрашивал пользователь
    Атрибут tg_id: str - идентификатор пользователя в телеграме
    """
    user: User = session.query(User).filter(User.tg_id == tg_id).first()
    return user.reports


def get_report_city(tg_id: str, report_id: int) -> WeatherReports | None:
    """
    Получение отчетной информации о погоде для конкретного города
    Атрибуты:
    1. tg_id: str - идентификатор пользователя в телеграме
    2. report_id - идентификатор отчета о погоде
    """
    reports: list[WeatherReports] = get_reports(tg_id)
    for report in reports:
        if report.id == report_id:
            return report
    return None
