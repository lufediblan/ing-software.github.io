from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional

class StudentBase(BaseModel):
    email: EmailStr
    name: str
    full_name: str
    semester: int
    
    @validator("email")
    def validate_email_domain(cls, value):
        if not value.endswith("@unilibre.edu.co"):
            raise ValueError("Email domain must be @unilibre.edu.co")
        return value

class StudentCreate(StudentBase):
    hashed_password: str

class Student(StudentBase):
    id: int
    inscriptions: List["Inscription"] = []

    class Config:
        orm_mode = True

class MisterBase(BaseModel):
    email: EmailStr
    name: str
    full_name: str
    semester: int
    
    @validator("email")
    def validate_email_domain(cls, value):
        if not value.endswith("@unilibre.edu.co"):
            raise ValueError("Email domain must be @unilibre.edu.co")
        return value

class MisterCreate(MisterBase):
    hashed_password: str

class Mister(MisterBase):
    id: int
    courses: List["Course"] = []

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    semester: int
    mister_id: int

class CourseCreate(CourseBase):
    hashed_password: str

class Course(CourseBase):
    id: int
    mister: Mister
    inscriptions: List["Inscription"] = []

    class Config:
        orm_mode = True

class InscriptionBase(BaseModel):
    student_id: int
    course_id: int

class InscriptionCreate(InscriptionBase):
    pass

class Inscription(InscriptionBase):
    id: int
    student: Student
    course: Course

    class Config:
        orm_mode = True

class NoteBase(BaseModel):
    note1: Optional[float] = None
    note2: Optional[float] = None
    note3: Optional[float] = None

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int

    class Config:
        orm_mode = True