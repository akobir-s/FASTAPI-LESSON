from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine


DATABASE_URL = 'postgresql+psycopg://postgres:1245@localhost/day2_fastapi'


engine = create_engine(url=DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

SessionMaker = sessionmaker(bind=engine)


# ORM object ralational Mapper
# psycopg 

