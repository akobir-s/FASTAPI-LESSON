from fastapi import FastAPI, Depends, HTTPException, Query
from schemas import StudentIn, StudentOut, StudentPatch, GroupIn, GroupOut, GroupDetail, StudentDetail
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import select, func
from database import get_db
from models import Student, Group
from typing import Annotated, Literal
from math import ceil


app = FastAPI(title="Crud Api on FAstapi")

@app.get("/")
def status():
    return {'status': 'healthy'}

#Author book 


def get_student_or_404(student_id, db:Session):
    student = db.get(Student, student_id, options=[joinedload(Student.group)])
    if not student:
        raise HTTPException(status_code=404, detail=f'Student with this id {student_id} not found')
    return student

@app.post('/students', response_model=StudentOut, status_code=201)
def create_student(data:StudentIn, db:Session = Depends(get_db)):
    student = Student(**data.model_dump(exclude_unset=True))
    db.add(student)
    db.commit()
    db.refresh(student)


    return student



@app.post('/groups', response_model=GroupOut, status_code=201)
def create_group(data:GroupIn, db:Session = Depends(get_db)):
    group = Group(title=data.title)
    db.add(group)
    db.commit()
    db.refresh(group)

    return group


@app.get('/group', response_model=list[GroupDetail], status_code=200)
def get_group_by_id( db:Session = Depends(get_db)):
    stmt = select(Group).options(selectinload(Group.students))
    groups = db.execute(stmt).scalars().all()
    return groups


@app.get('/group/{group_id}', response_model=GroupDetail, status_code=200)
def get_group_by_id(group_id: int, db:Session = Depends(get_db)):
    group = db.get(Group, group_id, options=[selectinload(Group.students)])
    if not group:
        raise HTTPException(status_code=404, detail="not found anygroup with this id ")
    return group



@app.get('/students', response_model=list[StudentOut], status_code=200)
def get_students(db:Session = Depends(get_db)):
    smtm = select(Student).options(joinedload(Student.group)) 
    students = db.execute(smtm).scalars().all()
    

    return students

@app.get('/students/{student_id}', response_model=StudentOut, status_code=200)
def student_by_id(student_id:int, db:Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    return student




@app.put('/students/{student_id}', response_model=StudentOut)
def put_student(student_id:int, data: StudentIn, db:Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    
    student.name = data.name
    student.age = data.age

    db.commit()
    db.refresh(student)
    return student
    


@app.patch('/students/{student_id}', response_model=StudentOut)
def update_with_patch(student_id:int, data: StudentIn, db:Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    
    new_data = data.model_dump(exclude_unset=True)

    for key, value in new_data.items():
        setattr(student, key, value)   # student.name = Munus

    db.commit()
    db.refresh(student)
    return student


@app.delete('/students/{student_id}', status_code=204)
def delete(student_id:int, db:Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)

  
    db.delete(student)
    db.commit()

    




@app.get('/students-detail', response_model=StudentDetail)
def filter_students(
    q: Annotated[str | None, Query(max_length=100, description='Search for students name')] = None,
    group_id: Annotated[int | None, Query(gt=0)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    size:Annotated[int, Query(ge=1, le=100)] = 10,
    min_age: Annotated[int | None, Query(gt=0, le=120)] = None, # 20 
    max_age: Annotated[int | None, Query(gt=0, le=120)] = None,
    sort: Literal['id', 'name', 'age'] = 'id',  # 
    order: Literal['desc', 'asc'] = 'desc',
    db: Session = Depends(get_db)
):
    filters = []  
    if q:
        filters.append(Student.name.ilike(f'%{q}%'))
    if group_id:
        filters.append(Student.group_id == group_id)
    if min_age:
        filters.append(Student.age >= min_age)
    if max_age:
        filters.append(Student.age <= max_age)
    # [1, 2, 3, ]
    
    total = db.scalar(select(func.count()).select_from(Student).where(*filters)) # select count(*) from student where

    column = getattr(Student, sort) # Student.age
    sort_by = column.desc() if order == 'desc' else column.asc()
   
    stmt = (
        select(Student)
        .options(joinedload(Student.group))  #  (student.group) -> joinedload
        .where(*filters)
        .order_by(sort_by, Student.id)       # Student.id — s
        .offset((page - 1) * size)
        .limit(size)
    )
    items = db.execute(stmt).scalars().all()

    return {
        'total': total,
        'page': page,
        'size': size,
        'pages': ceil(total / size),
        'items': items
    }