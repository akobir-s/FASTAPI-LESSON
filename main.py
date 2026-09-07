from fastapi import FastAPI
from pydantic import BaseModel, Field


class StudentIn(BaseModel):
    name:str = Field(description='should be string', examples=['Zafar'])
    age: int = Field(gt=0, lte=120, description='should be integer greater thean')

app = FastAPI(title="Our Api", description='our api for thsi project')



@app.get('/')
def home_page():
    return {"Status": "Healthy"}



@app.post('/student')
def add_student(student:StudentIn):
    return student