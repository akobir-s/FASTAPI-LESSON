from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Constraint


class Student(Base):
    __tablename__  = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(55))
    age: Mapped[int  | None] 

    def __repr__(self):
        return self.name 
    
    







   
    



