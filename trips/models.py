import datetime

from sqlmodel import Column, Field, Relationship, SQLModel, String

import models as base_models
from trips import enums as trips_enums


class TripBase(SQLModel):
    country: str
    purpose: trips_enums.PurposeType
    start_date: datetime.date
    end_date: datetime.date | None = Field(default=None)
    comment: str | None = Field(default=None, sa_column=Column(String(50)))


class Trip(base_models.Timestamp, TripBase, base_models.Id, table=True):
    user_id: int = Field(foreign_key="user.id")

    user: base_models.User = Relationship(back_populates="trips")
