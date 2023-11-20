from fastapi import FastAPI, Depends, Request, Form, HTTPException, status, logger
from fastapi.staticfiles import StaticFiles
from sql.database import SessionLocal, engine
from sql import crud, models, schemas
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from auth.hpw import hash_password, verfiy_password
from fastapi.responses import JSONResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="./front/static"), name="static")
templates = Jinja2Templates(directory="./front/templates")

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/mister_create_notes")
def get_mister_create_notes(request: Request):
    return templates.TemplateResponse("mister_create_notes.html", {"request": request})

@app.get("/mister_vew_course")
def get_mister_vew_course(request: Request):
    return templates.TemplateResponse("mister_vew_curse.html", {"request": request})

@app.get("/mister_create_course")
def get_mister_create_course(request: Request):
    return templates.TemplateResponse("mister_createcourse.html", {"request": request})

@app.get("/mister_vew_homeworks")
def get_mister_create_course(request: Request):
    return templates.TemplateResponse("mister_vew_homeworks", {"request": request})



@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/sloginsni")
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signupsni")
def read_root(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/form_create")
def form_fields(
        request: Request, email: str = Form(...),
        name = Form(...), lastname = Form(...),
        password = Form(...), password2 = Form(...),
        rol = Form(...), semester = Form(...),
        db: Session = Depends(get_db)
    ):
    
    if not email.endswith("@unilibre.edu.co"):
        return templates.TemplateResponse("signup.html", {"request": request, "message": "Email domain must be @unilibre.edu.co"})
    
    db_student = crud.get_student_by_email(db, email)
    db_mister = crud.get_mister_by_email(db, email)
    
    if db_student or db_mister:
        return templates.TemplateResponse("signup.html", {"request": request, "message": "Email already registered."})
    
    if not password == password2:
        return templates.TemplateResponse("signup.html", {"request": request, "message": "Passwords must be match."})
    
    if rol == "Student":
        
        data = {
            "email": email,
            "name": name,
            "full_name": lastname,
            "semester": semester,
            "hashed_password": hash_password(password)
        }
        
        student_db = schemas.StudentCreate(**data)
        
        return create_student(request=request, student=student_db, db=db)
    
    elif rol == "Mister":
        
        data = {
            "email": email,
            "name": name,
            "full_name": lastname,
            "semester": semester,
            "hashed_password": hash_password(password)
        }
        
        print(data)
        
        mister_db = schemas.MisterCreate(**data)
        
        print(mister_db)
        
        return create_mister(request=request, mister=mister_db, db=db)
        

@app.post("/create_student", response_model=schemas.StudentCreate)
def create_student(request: Request, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    
    try:
        crud.create_student(db=db, student=student)
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "message": str(e)})
    
    return templates.TemplateResponse("signup.html", {"request": request, "message": "You have been successfully registered."})
    

@app.post("/create_mister", response_model=schemas.MisterCreate)
def create_mister(request: Request, mister: schemas.MisterCreate, db: Session = Depends(get_db)):
    
    try:
        crud.create_mister(db=db, mister=mister)
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "message": str(e)})
    
    return templates.TemplateResponse("signup.html", {"request": request, "message": "You have been successfully registered."})

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    
    student_db = crud.get_student_by_email(db=db, student_email=email)
    mister_db = crud.get_mister_by_email(db=db, mister_email=email)
    
    if student_db:
        if verfiy_password(password, student_db.hashed_password):
            return templates.TemplateResponse("studenthome.html", {"request": request, "student": student_db})
        else:
            return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials."})
    elif mister_db:
        if verfiy_password(password, mister_db.hashed_password):
            return templates.TemplateResponse("mister_home.html", {"request": request, "mister": mister_db})
        else:
            return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials."})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "User not found."})

        
@app.post("/create_course_form")
def form_fields_create_course(
        request: Request, 
        name: str = Form(...),
        password: str = Form(...),
        description: str = Form(...),
        semester: int = Form(...),
        mister_id: int = Form(...),
        db: Session = Depends(get_db)
    ):
    
    if crud.get_course_by_name(db=db, name=name):
        return templates.TemplateResponse("mister_createcourse.html", {"request": request, "message": "Name not avaliable."})
    
    if not crud.get_mister_by_id(db=db, mister_id=mister_id):
        return templates.TemplateResponse("mister_createcourse.html", {"request": request, "message": "Invalid mister id."})
        
    data = {
        "name": name,
        "description": description,
        "semester": semester,
        "mister_id": mister_id,
        "hashed_password": password
    }
    
    course_db = schemas.CourseCreate(**data)       
    return create_course(request=request, course=course_db, db=db)
    
@app.post("/create_course", response_model=schemas.CourseCreate)
def create_course(request: Request, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    
    if crud.get_course_by_name(db=db, name=course.name):
        return templates.TemplateResponse("mister_createcourse.html", {"request": request, "message": "Name not avaliable."})
    
    if not crud.get_mister_by_id(db=db, mister_id=course.mister_id):
        return templates.TemplateResponse("mister_createcourse.html", {"request": request, "message": "Invalid mister id"})
            
    try:
        crud.create_course(db=db, course=course)
    except Exception as e:
        # Loguea la excepción para obtener más detalles
        logger.error(f"Error creating course: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    return templates.TemplateResponse("mister_createcourse.html", {"request": request, "message": "Course created successfully."})

@app.get("/get_courses_by_id")
def get_courses_by_id(db: Session = Depends(get_db))       :
    
    courses = crud.get_courses_by_professor_id(db=db, professor_id=1)
    # Asegúrate de devolver solo los campos necesarios
    return [{"name": course.name, "description": course.description, "professor_name": course.professor_name, "semester": course.semester} for course in courses]

@app.get("/misterhome")
def show_courses_mister(request: Request):
    
    return templates.TemplateResponse("mister_vew_curse.html", {"request": request})

@app.get("/viewnotes")
def show_courses_mister(request: Request):
    
    return templates.TemplateResponse("mister_vew_homeworks.html", {"request": request})

@app.post("/mistergetcourses")
def show_courses_mister(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    courses = crud.get_courses_by_professor_id(db=db, professor_id=id)
    # Asegúrate de devolver solo los campos necesarios y en formato JSON
    courses_json = [{"name": course.name, "description": course.description, "semester": course.semester, "professor_name": course.professor_name} for course in courses]
    return JSONResponse(content=courses_json)

@app.post("/getcoursesstudent")

def show_courses_student(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    inscriptions = crud.get_inscriptions_for_student(db=db, student_id=id)
    
    inscriptions_json = []
    
    for inscription in inscriptions:
        course_data = {
            "inscription_id": inscription.inscription_id,
            "student_name": inscription.student_name,
            "course_name": inscription.course_name,
            "course_description": inscription.course_description,
            "mister_name": inscription.mister_name
        }
        inscriptions_json.append(course_data)
    
    return JSONResponse(content=inscriptions_json)

@app.get("/createcourse")
def show_courses_mister(request: Request):
    
    return templates.TemplateResponse("mister_createcourse.html", {"request": request})

@app.get("/student_courses")
def show_courses_mister(request: Request):
    
    return templates.TemplateResponse("studentcourse.html", {"request": request})


@app.get("/student_inscription")
def show_courses_student(request: Request):
    
    return templates.TemplateResponse("student_inscription.html", {"request": request})

@app.post("/getformfieldsinscription")
def inscription_course_student(
        request: Request,
        course_id: int = Form(...),
        student_id: int = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
    ):
    
    course_db = crud.get_course_by_id(db=db, course_id=course_id)
    student_db = crud.get_student_by_id(db=db, student_id=student_id)
    
    if not course_db:
        return templates.TemplateResponse("student_inscription.html", {"request": request, "message": "Course not found."})
    
    if not student_db:
        return templates.TemplateResponse("student_inscription.html", {"request": request, "message": "Student not found."})
    
    if not verfiy_password(plane_password=password, hashed_password=course_db.hashed_password):
        return templates.TemplateResponse("student_inscription.html", {"request": request, "message": "Invalid password."})

    inscription_db = schemas.InscriptionCreate(student_id=student_db.id, course_id=course_db.id)
    
    return create_inscription(inscription=inscription_db, request=request, db=db)
    
@app.post("/create_inscription")
def create_inscription(inscription: schemas.InscriptionCreate, request: Request, db: Session = Depends(get_db)):
    
    crud.create_inscription(db=db, inscription=inscription)
    
    return templates.TemplateResponse("student_inscription.html", {"request": request, "message": "Successfull inscription."})

