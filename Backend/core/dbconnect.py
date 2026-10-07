from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from core.config import settings

engine = create_engine(settings.DB_URL)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()