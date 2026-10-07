from schemas.users import UserRegister
from models.users import Users

from sqlalchemy.orm import Session
from sqlalchemy import select

class UserRepo:
    def __init__(self, db:Session):
        self.db = db


    def create_user(self, user:UserRegister, hashed_password: str)-> Users:

        user = Users(
            username = user.username,
            email = user.email,
            password = hashed_password
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_by_username(self, username:str)-> Users | None:
        result =  self.db.execute(
            select(Users).where(
                Users.username == username
            )
        )

        return result.scalar_one_or_none()

    def get_user_by_email(self, email:str)-> Users | None:
        result = self.db.execute(
            select(Users).where(
                Users.email == email
            )
        )

        return result.scalar_one_or_none()
