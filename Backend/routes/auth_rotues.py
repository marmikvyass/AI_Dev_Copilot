from fastapi import APIRouter, Depends
from services.auth_service import AuthService
from schemas.users import UserLogin, UserRegister, UserResponse, TokenResponse
from core.dbconnect import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/register', response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    service = AuthService(db)

    return service.register_user(user)

@router.post('/login', response_model=TokenResponse)
def login(db: Session = Depends(get_db), form_data : OAuth2PasswordRequestForm = Depends()):
    service = AuthService(db)

    return service.login_user(
        form_data.username,
        form_data.password
    )