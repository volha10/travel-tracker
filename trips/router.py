from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from sqlmodel import Session

import models as base_models
from database import engine
from trips import models as trips_models
from trips import schemas as trips_schemas
from trips import service as trips_service

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(session: SessionDep) -> base_models.User:
    current_user = session.get(base_models.User, 1)

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user


CurrentUser = Annotated[base_models.User, Depends(get_current_user)]


def get_trip_or_raise_404(session, user_id, trip_id) -> trips_models.Trip:
    result = trips_service.select_user_trip_by_trip_id(
        session, user_id, trip_id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Trip not found")

    return result


@router.get("/trips", response_model=trips_schemas.TripListPublic)
def get_trip_list(session: SessionDep, current_user: CurrentUser):
    current_user_id = current_user.id
    result = trips_service.select_user_trips(session, current_user_id)

    return trips_schemas.TripListPublic(trips=result)


@router.get("/trips/{id}", response_model=trips_schemas.TripPublic)
def get_trip(*, session: SessionDep, current_user: CurrentUser, trip_id: int):
    current_user_id = current_user.id
    result = get_trip_or_raise_404(session, current_user_id, trip_id)

    return result


@router.patch("/trips/{id}", response_model=trips_schemas.TripPublic)
def update_trip(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    trip_id: int,
    trip_in: trips_schemas.TripToUpdate
):
    current_user_id = current_user.id

    result = get_trip_or_raise_404(session, current_user_id, trip_id)

    update_dict = trip_in.model_dump(exclude_unset=True)
    result.sqlmodel_update(update_dict)
    session.add(result)
    session.commit()
    session.refresh(result)

    return result


@router.post("/trips", response_model=trips_schemas.TripPublic)
def create_trip(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    trip_in: trips_schemas.TripToCreate
):
    current_user_id = current_user.id

    trip = trips_models.Trip.model_validate(
        trip_in, update={"user_id": current_user_id}
    )

    session.add(trip)
    session.commit()
    session.refresh(trip)

    return trip


@router.delete("/trips/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    *, session: SessionDep, current_user: CurrentUser, trip_id: int
):
    current_user_id = current_user.id

    trip = get_trip_or_raise_404(session, current_user_id, trip_id)

    session.delete(trip)
    session.commit()
