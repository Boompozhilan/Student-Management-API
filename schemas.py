from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    email: str
    course: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentResponse(StudentBase):
    message: str = "Student record created successfully"
    id: int

    class Config:
        from_attributes = True
        
class StudentListResponse(StudentBase):
    id: int
    
    class Config:
        from_attributes = True
