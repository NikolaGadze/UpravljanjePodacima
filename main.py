from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud, auth
from database import SessionLocal, engine, get_db

# Initialize the FastAPI app
app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Security definitions for Swagger
app.post("/login", response_model=schemas.Token)(auth.login_for_access_token)

# Dependency to get the database session
@app.post("/register/patient", response_model=schemas.Patient)
def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = crud.get_user(db, patient.Email)
    if db_patient:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_patient(db=db, patient=patient)

@app.post("/register/doctor", response_model=schemas.Doctor)
def register_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = crud.get_user(db, doctor.Email)
    if db_doctor:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_doctor(db=db, doctor=doctor)

@app.get("/appointments/patient", response_model=List[schemas.Appointment], dependencies=[Depends(auth.oauth2_scheme)])
def read_appointments_for_patient(current_user: schemas.Patient = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_appointments_for_patient(db=db, patient_id=current_user.PatientID)

@app.get("/appointments/doctor", response_model=List[schemas.Appointment], dependencies=[Depends(auth.oauth2_scheme)])
def read_appointments_for_doctor(current_user: schemas.Doctor = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_appointments_for_doctor(db=db, doctor_id=current_user.DoctorID)

@app.post("/appointments", response_model=schemas.Appointment, dependencies=[Depends(auth.oauth2_scheme)])
def create_appointment(appointment: schemas.AppointmentCreate, current_user: schemas.Patient = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.create_appointment(db=db, appointment=appointment)

@app.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth.oauth2_scheme)])
def delete_appointment(appointment_id: int, current_user: schemas.Doctor = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    crud.delete_appointment(db=db, appointment_id=appointment_id)

@app.get("/prescriptions/patient", response_model=List[schemas.Prescription], dependencies=[Depends(auth.oauth2_scheme)])
def read_prescriptions_for_patient(current_user: schemas.Patient = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_prescriptions_for_patient(db=db, patient_id=current_user.PatientID)

@app.get("/prescriptions/doctor", response_model=List[schemas.Prescription], dependencies=[Depends(auth.oauth2_scheme)])
def read_prescriptions_for_doctor(current_user: schemas.Doctor = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_prescriptions_for_doctor(db=db, doctor_id=current_user.DoctorID)

@app.post("/prescriptions", response_model=schemas.Prescription, dependencies=[Depends(auth.oauth2_scheme)])
def create_prescription(prescription: schemas.PrescriptionCreate, current_user: schemas.Doctor = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.create_prescription(db=db, prescription=prescription)

@app.delete("/prescriptions/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth.oauth2_scheme)])
def delete_prescription(prescription_id: int, current_user: schemas.Doctor = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    crud.delete_prescription(db=db, prescription_id=prescription_id)
