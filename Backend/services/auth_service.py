from respos.users import UserRepo
from core.security import hash_password, verify_password, create_access_token
from schemas.users import UserRegister, UserLogin
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, db:Session):
        self.repository = UserRepo(db)

    def register_user(self, user: UserRegister):
        existing_user = self.repository.get_user_by_username(user.username)

        if existing_user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail='User with that username already exists!'
            )
        else:
            hashed_password = hash_password(
                user.password
            )

            return self.repository.create_user(
                user,
                hashed_password
            )

    def login_user(self, username: str, password : str):
        existing_user = self.repository.get_user_by_username(username)

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User with that username does not exist!'
            )
        else:
            verified_password = verify_password(password, existing_user.password)

            if not verified_password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid user credentials!'
                )
            else:
                access_token = create_access_token(
                    data = {
                        "sub" : str(existing_user.username)
                    }
                )

                return {
                    'access_token' : access_token,
                    'token_type' : 'bearer'
                }
