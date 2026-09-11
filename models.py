from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint, ForeignKey, Table, Column

# 1: 1 , G) N : S) M 

student_course = Table(
    'student_course',
    Base.metadata,
    Column('student_id', ForeignKey('students.id', ondelete='CASCADE')),
    Column('course_id', ForeignKey('courses.id', ondelete='CASCADE')),
)

class Student(Base):
    __tablename__  = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(55))
    age: Mapped[int | None] 
    group_id: Mapped[int | None] = mapped_column(ForeignKey('groups.id'))

    #student.group_id.

    profile: Mapped["Profile | None"] = relationship(  # student.profile 
        cascade='all, delete-orphan',
        back_populates='student'  # profile.student
    )
    #student.group_id
    group: Mapped["Group | None"] = relationship(back_populates='students')

    courses: Mapped[list["Course"]] = relationship(
        secondary=student_course,
        back_populates='students'
    )

    __table_args__ = (CheckConstraint('age > 0', name='check_age_positve' ), )

    def __repr__(self):
        return self.name
    

class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(55))


    students: Mapped[list[Student]] = relationship(back_populates='group')

    def __repr__(self):
        return self.title
    
class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('students.id'), unique=True)
    address: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(15))


    student:Mapped[Student] = relationship(back_populates='profile')
    
    def __repr__(self):
        return self.user_id.name
    


class  Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(55), unique=True)


    students: Mapped[list[Student]] =relationship(
        secondary=student_course,
        back_populates='courses'
    )

    def __repr__(self):
        return self.title




