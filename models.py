import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel, text


class Id(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class Timestamp(SQLModel):
    created_at: datetime.datetime | None = Field(
        default=None,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )


class User(Timestamp, Id, table=True):
    email: str
    password: str

    trips: List["Trip"] = Relationship(back_populates="user")
