from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import jwt

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserRead, Token

router = APIRouter(tags=["Authentication"])

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.exec(
        select(User).where(User.username == login_data.username)
    ).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})

    return Token(access_token=access_token)