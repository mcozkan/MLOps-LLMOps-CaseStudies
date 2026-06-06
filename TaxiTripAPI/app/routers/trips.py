import hashlib

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session, select

from app.database import get_db
from app.models import TaxiTrip, User
from app.schemas import TaxiTripCreate, TaxiTripRead
from app.routers.auth import SECRET_KEY, ALGORITHM

router = APIRouter(tags=["Taxi Trips"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def generate_row_id(trip_data: TaxiTripCreate) -> str:
    raw_data = str(trip_data.model_dump(exclude={"row_id"}))
    return hashlib.md5(raw_data.encode()).hexdigest()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.exec(select(User).where(User.username == username)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


@router.post("/trips")
def create_trip(
    trip_data: TaxiTripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row_id = trip_data.row_id or generate_row_id(trip_data)

    existing_trip = db.get(TaxiTrip, row_id)

    if existing_trip:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trip already exists",
        )

    trip = TaxiTrip(
        **trip_data.model_dump(exclude={"row_id"}),
        row_id=row_id,
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip created successfully",
        "row_id": trip.row_id,
    }


@router.get("/trips", response_model=list[TaxiTripRead])
def get_trips(
    limit: int = Query(default=10, ge=1, le=10),
    db: Session = Depends(get_db),
    ):
    trips = db.exec(
        select(TaxiTrip)
        .order_by(TaxiTrip.tpep_pickup_datetime.desc())
        .limit(limit)
    ).all()

    return trips


@router.get("/trips/{row_id}", response_model=TaxiTripRead)
def get_trip_by_id(
    row_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trip = db.get(TaxiTrip, row_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found",
        )

    return trip