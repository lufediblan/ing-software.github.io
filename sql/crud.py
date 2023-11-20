from sqlalchemy.orm import Session
from . import models, schemas
from auth.hpw import hash_password
from sqlalchemy import select

def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def get_mister_by_id(db: Session, mister_id: int):
    return db.query(models.Mister).filter(models.Mister.id == mister_id).first()

def get_student_by_email(db: Session, student_email: str):
    return db.query(models.Student).filter(models.Student.email == student_email).first()

def get_mister_by_email(db: Session, mister_email: str):
    return db.query(models.Mister).filter(models.Mister.email == mister_email).first()

def get_course_by_name(db: Session, name: str):
    return db.query(models.Course).filter(models.Course.name == name).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_misters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mister).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    
    try:
        db_student = models.Student(
            email=student.email, 
            hashed_password=student.hashed_password,
            name=student.name,
            full_name=student.full_name,
            semester=student.semester
        )

        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except Exception as e:
        return str(e)

def create_mister(db: Session, mister: schemas.MisterCreate):
    
    try:
        db_mister = models.Mister(
            email=mister.email, 
            hashed_password=mister.hashed_password,
            name=mister.name,
            full_name=mister.full_name,
            semester=mister.semester
        )

        db.add(db_mister)
        db.commit()
        db.refresh(db_mister)

        return db_mister

    except Exception as e:
        return str(e)
    

def create_course(db: Session, course: schemas.CourseCreate):
    
    try:
        db_course = models.Course(
            name=course.name, 
            description=course.description,
            semester=course.semester,
            mister_id=course.mister_id,
            hashed_password=hash_password(course.hashed_password)
        )

        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        return db_course

    except Exception as e:
        return str(e)
    


def get_inscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inscription).offset(skip).limit(limit).all()


def get_courses_by_professor_id(db: Session, professor_id: int, skip: int = 0, limit: int = 100):
    query = db.query(
        models.Course.name, 
        models.Course.description,
        models.Course.semester,
        models.Mister.name.label("professor_name"),
    )
    query = query.filter(models.Course.mister_id == professor_id)
    query = query.outerjoin(models.Mister, models.Course.mister_id == models.Mister.id)
    query = query.offset(skip)
    query = query.limit(limit)
    
    result = query.all()
    
    print(result)
    
    return result


def get_courses_with_misters(db: Session, mister_id: int):
    stmt = (
        select(
            models.Course.name, 
            models.Course.description, 
            models.Mister.name.label('profesor_name')
        )
        .select_from(models.Course)
        .join(models.Mister, models.Course.mister_id == models.Mister.id)
        .where(models.Course.mister_id == mister_id)
    )
    result = db.execute(stmt).fetchall()
    return result

def get_inscriptions_for_student(db: Session, student_id: int):
    stmt = (
        select(
            models.Inscription.id.label('inscription_id'),
            models.Student.name.label('student_name'),
            models.Course.name.label('course_name'),
            models.Course.description.label('course_description'),
            models.Mister.name.label('mister_name')
        )
        .select_from(models.Inscription)
        .join(models.Student, models.Inscription.student_id == models.Student.id)
        .join(models.Course, models.Inscription.course_id == models.Course.id)
        .join(models.Mister, models.Course.mister_id == models.Mister.id)
        .where(models.Inscription.student_id == student_id)
    )
    result = db.execute(stmt).fetchall()
    return result

def create_inscription(db: Session, inscription: schemas.InscriptionCreate):
    
    try:
        db_inscription = models.Inscription(
            student_id=inscription.student_id, 
            course_id=inscription.course_id
        )

        db.add(db_inscription)
        db.commit()
        db.refresh(db_inscription)

        return db_inscription

    except Exception as e:
        return str(e)
