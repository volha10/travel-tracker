from typing import Sequence, Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import engine
from models import (
    User,
    Trip,
    TripToCreate,
    TripToUpdate,
    TripPublic,
    TripListPublic,
)

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(session: SessionDep) -> User:
    current_user = session.get(User, 1)

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user


CurrentUser = Annotated[User, Depends(get_current_user)]


def select_user_trips(session, user_id: int) -> Sequence[Trip]:
    query = select(Trip).where(Trip.user_id == user_id)
    result = session.exec(query).all()

    return result


def select_user_trip_by_trip_id(session, user_id, trip_id) -> Trip | None:
    query = select(Trip).where(Trip.user_id == user_id, Trip.id == trip_id)
    result = session.exec(query).first()
    return result


def get_trip_or_raise_404(session, user_id, trip_id) -> Trip:
    result = select_user_trip_by_trip_id(session, user_id, trip_id)

    if not result:
        raise HTTPException(status_code=404, detail="Trip not found")

    return result


@app.get("/trips", response_model=TripListPublic)
def get_trip_list(session: SessionDep, current_user: CurrentUser):
    current_user_id = current_user.id
    result = select_user_trips(session, current_user_id)

    return TripListPublic(trips=result)


@app.get("/trips/{id}", response_model=TripPublic)
def get_trip(*, session: SessionDep, current_user: CurrentUser, trip_id: int):
    current_user_id = current_user.id
    result = get_trip_or_raise_404(session, current_user_id, trip_id)

    return result


@app.patch("/trips/{id}", response_model=TripPublic)
def update_trip(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    trip_id: int,
    trip_in: TripToUpdate
):
    current_user_id = current_user.id

    result = get_trip_or_raise_404(session, current_user_id, trip_id)

    update_dict = trip_in.model_dump(exclude_unset=True)
    result.sqlmodel_update(update_dict)
    session.add(result)
    session.commit()
    session.refresh(result)

    return result


@app.post("/trips", response_model=TripPublic)
def create_trip(
    *, session: SessionDep, current_user: CurrentUser, trip_in: TripToCreate
):
    current_user_id = current_user.id

    trip = Trip.model_validate(trip_in, update={"user_id": current_user_id})

    session.add(trip)
    session.commit()
    session.refresh(trip)

    return trip


@app.delete("/trips/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    *, session: SessionDep, current_user: CurrentUser, trip_id: int
):
    current_user_id = current_user.id

    trip = get_trip_or_raise_404(session, current_user_id, trip_id)

    session.delete(trip)
    session.commit()


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8001, reload=True)
