from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from sqlalchemy.orm import Session
from myapplications.api.Database.database import get_db
from myapplications.api.Database import models
from myapplications.api.Database.database import SessionLocal
from myapplications.api.crud import get_gym_by_email
from myapplications.api.utils.security import verify_password, decode_access_token
from myapplications.api.Database.schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_gym(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        gym_id: int = payload.get("sub")
        if gym_id is None:
            raise credentials_exception
        token_data = TokenData(gym_id=gym_id)
    except JWTError:
        raise credentials_exception

    gym = db.query(get_gym_by_email).filter(models.Gym.gym_id == token_data.gym_id).first()
    if gym is None:
        raise credentials_exception
    return gym
