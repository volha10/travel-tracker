import datetime
import enum
from typing import List

from sqlmodel import Column, Field, Relationship, SQLModel, String, text


class PurposeType(enum.StrEnum):
    NOT_SELECTED = "NOT SELECTED"
    TOURISM = "Tourism"
    TRANSIT = "Transit"
    VISITING_FRIENDS_OR_RELATIVES = "Visiting friends or relatives"
    BUSINESS_TRIP = "Business trip"
    EDUCATION_OR_TRAINING = "Education or training"
    MEDICAL_TREATMENT = "Medical treatment"
    SPORTS_EVENTS_OR_COMPETITIONS_PARTICIPATION = (
        "Sports events or competitions participation"
    )
    OTHER = "Other"


class _Id(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class _Timestamp(SQLModel):
    created_at: datetime.datetime | None = Field(
        default=None,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )


class User(_Timestamp, _Id, table=True):
    email: str
    password: str

    trips: List["Trip"] = Relationship(back_populates="user")


class _TripBase(SQLModel):
    country: str
    purpose: PurposeType
    start_date: datetime.date
    end_date: datetime.date | None = Field(default=None)
    comment: str | None = Field(default=None, sa_column=Column(String(50)))


class Trip(_Timestamp, _TripBase, _Id, table=True):
    user_id: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="trips")


class TripToCreate(_TripBase):
    pass


class TripToUpdate(SQLModel):
    country: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    purpose: PurposeType | None = None
    comment: str | None = None


class TripPublic(SQLModel):
    id: int
    country: str
    purpose: PurposeType
    start_date: datetime.date
    end_date: datetime.date | None
    comment: str | None

    user_id: int
    created_at: datetime.datetime


class TripListPublic(SQLModel):
    trips: list[TripPublic]
