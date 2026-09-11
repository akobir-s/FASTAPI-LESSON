from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(url=os.getenv('DATABASE_URL'), echo=True)

class Base(DeclarativeBase):  # models.Model
    pass 


SessionMaker  = sessionmaker(bind=engine)


def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()

