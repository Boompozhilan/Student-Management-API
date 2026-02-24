from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System")

@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Add a new student record [cite: 26]"""
    # Check if email already exists
    db_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_student = models.Student(name=student.name, email=student.email, course=student.course)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    # Matching the sample output requested [cite: 30]
    return {
        "message": "Student record created successfully",
        "id": new_student.id,
        "name": new_student.name,
        "email": new_student.email,
        "course": new_student.course
    }

@app.get("/students/", response_model=list[schemas.StudentListResponse])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """View student lists [cite: 26]"""
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@app.get("/students/{student_id}", response_model=schemas.StudentListResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """View a single student's details"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.StudentListResponse)
def update_student(student_id: int, student_data: schemas.StudentUpdate, db: Session = Depends(get_db)):
    """Update student details [cite: 26]"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.name = student_data.name
    student.email = student_data.email
    student.course = student_data.course
    
    db.commit()
    db.refresh(student)
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete records [cite: 26]"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return {"message": "Student record deleted successfully"}
