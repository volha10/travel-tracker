from typing import Sequence

from sqlmodel import select

from trips import models as trips_models


def select_user_trips(session, user_id: int) -> Sequence[trips_models.Trip]:
    query = select(trips_models.Trip).where(
        trips_models.Trip.user_id == user_id
    )
    result = session.exec(query).all()

    return result


def select_user_trip_by_trip_id(
    session, user_id, trip_id
) -> trips_models.Trip | None:
    query = select(trips_models.Trip).where(
        trips_models.Trip.user_id == user_id, trips_models.Trip.id == trip_id
    )
    result = session.exec(query).first()
    return result
