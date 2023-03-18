from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, Integer, String
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('PG_USER')
psw = os.getenv('PG_PASSWORD')
db = os.getenv('PG_DB')
host = os.getenv('PG_HOST')
port = os.getenv('PG_PORT')


# Подключение к БД
PG_DSN = f'postgresql+asyncpg://{user}:{psw}@{host}:{port}/{db}'
# Движок
engine = create_async_engine(PG_DSN)
# expire_on_commit=False, чтобы сессия не истекала, после того как мы сделали коммит
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# Базовый класс
Base = declarative_base()


# Модель БД, таблица
class SwapiPeople(Base):

    __tablename__ = 'swapi_people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)  # url --> title: []
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)  # url --> name: str
    mass = Column(String)
    skin_color = Column(String)
    species = Column(String)  # url --> name: []
    starships = Column(String)  # url --> name: []
    vehicles = Column(String)  # url --> name: []
