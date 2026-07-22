import bcrypt
from sqlalchemy.orm import Session
from app.models import User


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
