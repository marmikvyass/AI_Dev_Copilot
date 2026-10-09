from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session


from core.config import settings
from core.dbconnect import get_db
from models.users import Users
from respos.users import UserRepo

oauth2_schema  = OAuth2PasswordBearer(tokenUrl='/api/auth/login')
def get_current_user(token: str = Depends(oauth2_schema),  db: Session = Depends(get_db))-> Users:
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        username = payload.get('sub')

        if username is None:
            return credentials_exceptions


    except (JWTError, ValueError):
        raise credentials_exceptions

    repository = UserRepo(db)

    user = repository.get_user_by_username(username)

    if user is None:
        raise credentials_exceptions

    return user