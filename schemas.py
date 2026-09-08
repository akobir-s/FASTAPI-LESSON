from pydantic import BaseModel, Field, ConfigDict



class StudentIn(BaseModel):
    name: str = Field(max_length=55, examples=['Zafar'])
    age: int = Field(ge=0, le=120)
    


class StudentOut(BaseModel):
    id: int
    name: str
    age: int


    model_config = ConfigDict(from_attributes=True)
    
class StudentPatch(BaseModel):
    name: str | None = Field(default=None, max_length=55)
    age: int | None = Field(default=None, gt=0, le=120)
