from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Student(Base):  # models.Model  app_ ORM
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int]
 
    





