import datetime

from sqlmodel import SQLModel

from trips import models as trips_models
from trips import enums as trips_enums


class TripToCreate(trips_models.TripBase):
    pass


class TripToUpdate(SQLModel):
    country: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    purpose: trips_enums.PurposeType | None = None
    comment: str | None = None


class TripPublic(SQLModel):
    id: int
    country: str
    purpose: trips_enums.PurposeType
    start_date: datetime.date
    end_date: datetime.date | None
    comment: str | None

    user_id: int
    created_at: datetime.datetime


class TripListPublic(SQLModel):
    trips: list[TripPublic]
