from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base

# Database configuration
host = 'xxx-yyy-zzz' # Endpoint of the DbSystem i.e use localhost incase if you don't have cloud account  
user = 'admin'
password = 'changeme'
database_name = 'student_db'

# Define the database connection
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}".format(user, password, host, database_name)

# Create the SQLAlchemy engine and sessionmaker
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Define the base model and session function
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Define the models
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    age = Column(Integer)
    gender = Column(String(10))
    grade = Column(Integer)

    courses = relationship("Course", secondary="student_courses")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

    students = relationship("Student", secondary="student_courses")

class StudentCourse(Base):
    __tablename__ = "student_courses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    course_id = Column(Integer, index=True)

# Define the input and output schemas
class StudentInput(BaseModel):
    name: str
    age: int
    gender: str
    grade: int

class StudentOutput(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    grade: int

class CourseInput(BaseModel):
    name: str

class CourseOutput(BaseModel):
    id: int
    name: str

class StudentCourseInput(BaseModel):
    student_id: int
    course_id: int

class StudentCourseOutput(BaseModel):
    id: int
    student_id: int
    course_id: int

# Instantiate the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the routes
@app.post("/students", response_model=StudentOutput)
def create_student(student: StudentInput, db: Session = Depends(get_db)):
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students", response_model=List[StudentOutput])
def read_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.get("/students/{student_id}", response_model=StudentOutput)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=StudentOutput)
def update_student(student_id: int, student: StudentInput, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict(exclude_unset=True).items():
        setattr(db_student, key, value)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}

@app.post("/courses", response_model=CourseOutput)
def create_course(course: CourseInput, db: Session = Depends(get_db)):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.get("/courses", response_model=List[CourseOutput])
def read_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@app.get("/courses/{course_id}", response_model=CourseOutput)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=CourseOutput)
def update_course(course_id: int, course: CourseInput, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted"}

@app.post("/student_courses", response_model=StudentCourseOutput)
def create_student_course(student_course: StudentCourseInput, db: Session = Depends(get_db)):
    new_student_course = StudentCourse(**student_course.dict())
    db.add(new_student_course)
    db.commit()
    db.refresh(new_student_course)
    return new_student_course

@app.get("/student_courses", response_model=List[StudentCourseOutput])
def read_student_courses(db: Session = Depends(get_db)):
    student_courses = db.query(StudentCourse).all()
    return student_courses

@app.get("/student_courses/{student_course_id}", response_model=StudentCourseOutput)
def read_student_course(student_course_id: int, db: Session = Depends(get_db)):
    student_course = db.query(StudentCourse).filter(StudentCourse.id == student_course_id).first()
    if not student_course:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    return student_course

@app.put("/student_courses/{student_course_id}", response_model=StudentCourseOutput)
def update_student_course(student_course_id: int, student_course: StudentCourseInput, db: Session = Depends(get_db)):
    db_student_course = db.query(StudentCourse).filter(StudentCourse.id == student_course_id).first()
    if not db_student_course:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    for key, value in student_course.dict(exclude_unset=True).items():
        setattr(db_student_course, key, value)
    db.add(db_student_course)
    db.commit()
    db.refresh(db_student_course)
    return db_student_course

@app.delete("/student_courses/{student_course_id}")
def delete_student_course(student_course_id: int, db: Session = Depends(get_db)):
    db_student_course = db.query(StudentCourse).filter(StudentCourse.id == student_course_id).first()
    if not db_student_course:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    db.delete(db_student_course)
    db.commit()
    return {"message": "StudentCourse deleted"}
