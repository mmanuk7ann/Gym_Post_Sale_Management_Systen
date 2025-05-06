from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from sqlalchemy.orm import Session
from Database.database import get_db
from Database import models
from Database.database import SessionLocal
from crud import get_gym_by_email
# from utils.security import verify_password, decode_access_token
from Database.schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_gym(gym_id, db: Session = Depends(get_db)): # token: str = Depends(oauth2_scheme),
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # try:
    #     payload = decode_access_token(token)
    #     gym_id: int = payload.get("sub")
    #     if gym_id is None:
    #         raise credentials_exception
    #     token_data = TokenData(gym_id=gym_id)
    # except JWTError:
    #     raise credentials_exception

    gym = db.query(get_gym_by_email).filter(models.Gym.gym_id == gym_id).first() #
    if gym is None:
        raise credentials_exception
    return gym
