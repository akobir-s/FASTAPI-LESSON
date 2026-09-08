from fastapi import FastAPI, Depends, HTTPException
from schemas import StudentIn, StudentOut, StudentPatch
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from sqlalchemy import select

app = FastAPI(title ="Crud" )

@app.get("/")
def get_status():
    return {"status": "healthy"}





@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(data: StudentIn, db: Session = Depends(get_db)):
    student = Student(name=data.name, age=data.age)
    db.add(student)
    db.commit()
    db.refresh(student)

    return student




@app.get("/students", response_model=list[StudentOut], status_code=200)
def get_students(db: Session = Depends(get_db)):
    stmt = select(Student)  # select * from studnets
    students = db.execute(stmt).scalars().all()

    return students




@app.get("/students/{student_id}", response_model=StudentOut, status_code=200)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Not found student by this id")

    return student




@app.patch("/students/{student_id}", response_model=StudentOut, status_code=200)
def get_student_by_id(student_id: int, data: StudentPatch,  db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Not found student by this id")

    new = data.model_dump(exclude_unset=True)

    for key, value in new.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student





@app.put("/students/{student_id}", response_model=StudentOut, status_code=200)
def get_student_by_id(student_id: int, data: StudentIn,  db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Not found student by this id")

    student.name = data.name
    student.age = data.age


    db.commit()
    db.refresh(student)
    return student



@app.delete("/students/{student_id}", status_code=204)
def get_student_by_id(student_id: int,  db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Not found student by this id")

   


    db.delete(student)
    db.commit()





