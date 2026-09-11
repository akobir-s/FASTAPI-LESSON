from fastapi import FastAPI, Depends, HTTPException
from schemas import StudentIn, StudentOut, StudentPatch, GroupIn, GroupOut
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import Student, Group


app = FastAPI(title="Crud Api on FAstapi")

@app.get("/")
def status():
    return {'status': 'healthy'}



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

@app.get('/students', response_model=list[StudentOut], status_code=200)
def get_students(db:Session = Depends(get_db)):
    smtm = select(Student)
    students = db.execute(smtm).scalars().all()
    

    return students

@app.get('/students/{student_id}', response_model=StudentOut, status_code=200)
def student_by_id(student_id:int, db:Session = Depends(get_db)):
    student = db.get(Student, student_id)
    return student




@app.put('/students/{student_id}', response_model=StudentOut)
def put_student(student_id:int, data: StudentIn, db:Session = Depends(get_db)):
    student = db.get(Student, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail='Student by this id not found')
    
    student.name = data.name
    student.age = data.age

    db.commit()
    db.refresh(student)
    return student
    


@app.patch('/students/{student_id}', response_model=StudentOut)
def update_with_patch(student_id:int, data: StudentIn, db:Session = Depends(get_db)):
    student = db.get(Student, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail='Student by this id not found')
    
    new_data = data.model_dump(exclude_unset=True)

    for key, value in new_data.items():
        setattr(student, key, value)   # student.name = Munus

    db.commit()
    db.refresh(student)
    return student


@app.delete('/students/{student_id}', status_code=204)
def delete(student_id:int, db:Session = Depends(get_db)):
    student = db.get(Student, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail='Student by this id not found')
    
  
    db.delete(student)
    db.commit()

    
