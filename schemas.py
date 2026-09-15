from pydantic import BaseModel, Field, ConfigDict
from models import Group


class StudentIn(BaseModel):
    name: str = Field(max_length=55, examples=['Zafar'])
    age: int | None = Field(default=None, gt=0, lt=120)
    group_id: int |None = Field(default=None, gt=0, examples=[1])



class GroupIn(BaseModel):
    title: str = Field(max_length=55, examples=['Python 2 September'])
   


class GroupOut(BaseModel):
    id: int
    title: str
    


    model_config = ConfigDict(from_attributes=True)


class StudentShort(BaseModel):
    id: int 
    name: str
    age: int | None

    model_config = ConfigDict(from_attributes=True)


class GroupDetail(GroupOut):
    students: list[StudentShort]
    

class StudentOut(BaseModel):
    id: int
    name: str
    age: int | None
    group_id: int | None
    group: GroupOut | None
   


    model_config = ConfigDict(from_attributes=True)


class StudentPatch(BaseModel):
    name: str | None = Field(max_length=55, examples=['Zafar'])
    age: int | None = Field(gt=0, lt=120)
