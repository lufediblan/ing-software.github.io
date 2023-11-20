from sqlalchemy import Column, Integer, String, NotNullable, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(50), nullable=False, index=True, unique=True)
    hashed_password = Column(String(70), nullable=False)
    name = Column(String(50), nullable=False)
    full_name = Column(String(50), nullable=False)
    semester = Column(Integer, nullable=False, index=True)
    
    inscriptions = relationship("Inscription", back_populates="student")
    
class Mister(Base):
    __tablename__ = "misters"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(50), nullable=False, index=True, unique=True)
    hashed_password = Column(String(70), nullable=False)
    name = Column(String(50), nullable=False)
    full_name = Column(String(50), nullable=False)
    semester = Column(Integer, nullable=True, index=True)
    
    courses = relationship("Course", back_populates="mister")
    
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    hashed_password = Column(String(70), nullable=False)
    description = Column(String(255))
    semester = Column(Integer, nullable=False, index=True)
    mister_id = Column(Integer, ForeignKey("misters.id"), nullable=False)
    
    mister = relationship("Mister", back_populates="courses")
    
    inscriptions = relationship("Inscription", back_populates="course")
    
class Inscription(Base):
    __tablename__ = "inscriptions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="inscriptions")
    
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="inscriptions")
    
class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    note1 = Column(DECIMAL(3, 2), nullable=True)
    note2 = Column(DECIMAL(3, 2), nullable=True)
    note3 = Column(DECIMAL(3, 2), nullable=True)
    
    
    
    

    
