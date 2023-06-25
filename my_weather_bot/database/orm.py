from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import load_config, Config
from database import Base, User, WeatherReports

config: Config = load_config()
engine = create_engine(url=f'postgresql://{config.db.user_name}:' +
                       f'{config.db.user_passsword}@{config.db.address}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_user(tg_id: str) -> None:
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        session.commit()


def add_city(tg_id: str, city: str) -> None:
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.city = city
    session.commit()


def create_report(tg_id: str, temp: int, feels_like: int,
                  wind_speed: int, pressure_mm: int, city: str) -> None:
    user: User = session.query(User).filter(User.tg_id == tg_id).first()
    new_report = WeatherReports(temp=temp, owner=user.user_id,
                                feels_like=feels_like, wind_speed=wind_speed,
                                pressure_mm=pressure_mm, city=city)
    session.add(new_report)
    session.commit()


def get_user_city(tg_id: str) -> str | None:
    user: User = session.query(User).filter(User.tg_id == tg_id).first()
    return user.city


def get_reports(tg_id: str) -> list[WeatherReports]:
    user: User = session.query(User).filter(User.tg_id == tg_id).first()
    return user.reports


def get_report_city(tg_id: str, report_id: int) -> WeatherReports:
    reports: list[WeatherReports] = get_reports(tg_id)
    for report in reports:
        if report.id == report_id:
            return report
