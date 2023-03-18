import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import SwapiPeople


load_dotenv()

user = os.getenv('PG_USER')
psw = os.getenv('PG_PASSWORD')
db = os.getenv('PG_DB')
host = os.getenv('PG_HOST')
port = os.getenv('PG_PORT')

DSN = f'postgresql://{user}:{psw}@{host}:{port}/{db}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()


def print_from_db():
    for c in session.query(SwapiPeople).all():
        print(f'{c.id}: {c.name}')
    print()
    print(f"Всего {session.query(SwapiPeople).count()} героя. id=17 'Not found'")


def clear_table():
    session.query(SwapiPeople).delete()
    session.commit()
    session.close()
    print(f"Все записи удалены.")


clear_table()