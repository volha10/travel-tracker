import datetime

from sqlmodel import Session

from database import create_db_and_tables, engine
from models import PurposeType, Trip, User


def populate_users():
    user_1 = User(email="user_1@gmail.com", password="12345")

    with Session(engine) as session:
        session.add(user_1)
        session.commit()


def populate_trips():
    trip_1 = Trip(
        user_id=1,
        country="France",
        start_date=datetime.date(year=2023, month=5, day=1),
        end_date=datetime.date(year=2023, month=5, day=5),
        purpose=PurposeType.TOURISM,
    )
    trip_2 = Trip(
        user_id=1,
        country="Poland",
        start_date=datetime.date(year=2024, month=5, day=1),
        # end_date=datetime.date(year=2024, month=5, day=5),
        purpose=PurposeType.NOT_SELECTED,
    )

    with Session(engine) as session:
        session.add(trip_1)
        session.add(trip_2)
        session.commit()


def create_and_populate_db():
    create_db_and_tables()
    populate_users()
    populate_trips()


create_and_populate_db()
