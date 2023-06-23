"""
Таблица 1 - её имя User в ней есть:
1. Естественно id
2. tg_id - это id пользователя в телеграмме
3. city - город в котором пользователь живёт
4. connection_date - мы будем записывать дату, когда пользователь первый раз
    запустил бота, это будет колонка с типом данных DateTime
    и параметром default=datetime.now
5. reports - это отношение? в котором будут храниться
    все запрошенные отчёты по погоде

Таблица 2 - её имя WeatherReports в ней есть:
1. Естественно id
2. date - дата запроса погоды, здесь реализация аналогична connection_date
3. temp - температура
4. feels_like - температура по ощущениям
5. wind_speed - скорость ветра
6. pressure_mm - давление
7. city - город по которому запрашивали погоду
"""

from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Integer, String, DateTime,\
                       Column, create_engine, ForeignKey

Base = declarative_base()


@dataclass
class User(Base):
    """Таблица пользователей, делающих запросы на получение
    информации о погоде в некотором городе"""

    __tablename__ = 'Users'
    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    tg_id = Column('tg_id', String, nullable=False, unique=True)
    city = Column('city', String)
    connection_date = Column('connection_date', DateTime,
                             default=datetime.now(), nullable=False)
    reports = relationship('WeatherReports', backref='report',
                           cascade='all, delete-orphan', lazy=True)


@dataclass
class WeatherReports(Base):
    """Таблица, отображающая отчет о погоде"""

    __tablename__ = 'WeatherReports'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    owner = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    date = Column('date', DateTime, default=datetime.now(), nullable=False)
    temp = Column('temperature', Integer, nullable=False)
    feels_like = Column('feels_like', Integer, nullable=False)
    wind_speed = Column('wind_speed', Integer, nullable=False)
    pressure_mm = Column('pressure_mm', Integer, nullable=False)
    city = Column('city', String, nullable=False)


# def create_tables(db_user: str, db_passwd: str, db_address: str):
#     """Подключение к базе данных и создание таблиц"""

#     engine: Engine = create_engine(f'postgresql://{db_user}:{db_passwd}'
#                                    '@{db_address}', echo=True)
#     Base.metadata.create_all(engine)
