from fastapi import APIRouter, Depends
from services.auth_service import AuthService
from schemas.users import UserLogin, UserRegister, UserResponse, TokenResponse
from core.dbconnect import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/register', response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    service = AuthService(db)

    return service.register_user(user)

@router.post('/login', response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)

    return service.login_user(user)