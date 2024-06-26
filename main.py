from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Union
import models, schemas, crud, auth
from kafka_config import send_notification
from session_manager import session_manager
from database import SessionLocal, engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.Email}, expires_delta=access_token_expires)
    session_manager.store_token(access_token, user.Email)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout(token: HTTPAuthorizationCredentials = Security(security)):
    access_token = token.credentials
    session_manager.delete_token(access_token)
    return {"message": "Successfully logged out"}

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

@app.get("/appointments/patient", response_model=List[schemas.Appointment])
async def read_appointments_for_patient(current_user: schemas.Patient = Depends(auth.get_current_patient), db: Session = Depends(get_db)):
    return crud.get_appointments_for_patient(db=db, patient_id=current_user.PatientID)

@app.get("/appointments/doctor", response_model=List[schemas.Appointment])
async def read_appointments_for_doctor(current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    return crud.get_appointments_for_doctor(db=db, doctor_id=current_user.DoctorID)

@app.get("/appointment/{appointment_id}", response_model=schemas.Appointment)
async def read_appointment(appointment_id: int, current_user: Union[schemas.Patient, schemas.Doctor] = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    appointment = crud.get_appointment(db=db, appointment_id=appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if (hasattr(current_user, 'PatientID') and appointment.PatientID == current_user.PatientID) or \
       (hasattr(current_user, 'DoctorID') and appointment.DoctorID == current_user.DoctorID):
        return appointment
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view this appointment")


@app.post("/appointments", response_model=schemas.Appointment)
async def create_appointment(appointment: schemas.AppointmentCreate,
                             current_user: schemas.Patient = Depends(auth.get_current_patient),
                             db: Session = Depends(get_db)):
    new_appointment = crud.create_appointment(db=db, appointment=appointment)

    message = {
        "event": "AppointmentCreated",
        "message": "A new appointment has been created."
    }

    send_notification("appointments", message)

    return new_appointment

@app.put("/appointments/{appointment_id}", response_model=schemas.Appointment)
async def update_appointment(appointment_id: int, appointment: schemas.AppointmentUpdate, current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment(db, appointment_id)
    if not db_appointment or db_appointment.DoctorID != current_user.DoctorID:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.update_appointment(db=db, appointment_id=appointment_id, appointment=appointment)

@app.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment(db, appointment_id)
    if not db_appointment or db_appointment.DoctorID != current_user.DoctorID:
        raise HTTPException(status_code=404, detail="Appointment not found")
    crud.delete_appointment(db=db, appointment_id=appointment_id)

@app.get("/prescriptions/patient", response_model=List[schemas.Prescription])
async def read_prescriptions_for_patient(current_user: schemas.Patient = Depends(auth.get_current_patient), db: Session = Depends(get_db)):
    return crud.get_prescriptions_for_patient(db=db, patient_id=current_user.PatientID)

@app.get("/prescriptions/doctor", response_model=List[schemas.Prescription])
async def read_prescriptions_for_doctor(current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    return crud.get_prescriptions_for_doctor(db=db, doctor_id=current_user.DoctorID)


@app.get("/prescription/{prescription_id}", response_model=schemas.Prescription)
async def read_prescription(prescription_id: int,
                            current_user: Union[schemas.Patient, schemas.Doctor] = Depends(auth.get_current_user),
                            db: Session = Depends(get_db)):
    prescription = crud.get_prescription(db=db, prescription_id=prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    if isinstance(current_user, schemas.Patient) and prescription.PatientID != current_user.PatientID:
        raise HTTPException(status_code=403, detail="Not authorized to access this prescription")
    if isinstance(current_user, schemas.Doctor) and prescription.DoctorID != current_user.DoctorID:
        raise HTTPException(status_code=403, detail="Not authorized to access this prescription")

    return prescription


@app.post("/prescriptions", response_model=schemas.Prescription)
async def create_prescription(prescription: schemas.PrescriptionCreate, current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    return crud.create_prescription(db=db, prescription=prescription)

@app.put("/prescriptions/{prescription_id}", response_model=schemas.Prescription)
async def update_prescription(prescription_id: int, prescription: schemas.PrescriptionUpdate, current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    db_prescription = crud.get_prescription(db, prescription_id)
    if not db_prescription or db_prescription.DoctorID != current_user.DoctorID:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return crud.update_prescription(db=db, prescription_id=prescription_id, prescription=prescription)

@app.delete("/prescriptions/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription(prescription_id: int, current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    db_prescription = crud.get_prescription(db, prescription_id)
    if not db_prescription or db_prescription.DoctorID != current_user.DoctorID:
        raise HTTPException(status_code=404, detail="Prescription not found")
    crud.delete_prescription(db=db, prescription_id=prescription_id)

@app.get("/doctors", response_model=List[schemas.Doctor])
async def get_all_doctors(
    current_patient: schemas.Patient = Depends(auth.get_current_patient),
    db: Session = Depends(get_db)
):
    return crud.get_all_doctors(db=db)


@app.put("/patient/{patient_id}", response_model=schemas.Patient)
async def update_patient(patient_id: int, patient: schemas.PatientUpdate, current_user: schemas.Patient = Depends(auth.get_current_patient), db: Session = Depends(get_db)):
    if patient_id != current_user.PatientID:
        raise HTTPException(status_code=403, detail="Not authorized to update this patient")
    update_data = patient.dict(exclude_unset=True)
    if "Password" in update_data:
        update_data["Password"] = auth.get_password_hash(update_data["Password"])
    return crud.update_patient(db=db, patient_id=patient_id, patient=update_data)

@app.delete("/patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, current_user: schemas.Patient = Depends(auth.get_current_patient), db: Session = Depends(get_db)):
    if patient_id != current_user.PatientID:
        raise HTTPException(status_code=403, detail="Not authorized to delete this patient")
    crud.delete_patient(db=db, patient_id=patient_id)

@app.put("/doctor/{doctor_id}", response_model=schemas.Doctor)
async def update_doctor(doctor_id: int, doctor: schemas.DoctorUpdate, current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    if doctor_id != current_user.DoctorID:
        raise HTTPException(status_code=403, detail="Not authorized to update this doctor")
    update_data = doctor.dict(exclude_unset=True)
    if "Password" in update_data:
        update_data["Password"] = auth.get_password_hash(update_data["Password"])
    return crud.update_doctor(db=db, doctor_id=doctor_id, doctor=update_data)

@app.delete("/doctor/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: int, current_user: schemas.Doctor = Depends(auth.get_current_doctor), db: Session = Depends(get_db)):
    if doctor_id != current_user.DoctorID:
        raise HTTPException(status_code=403, detail="Not authorized to delete this doctor")
    crud.delete_doctor(db=db, doctor_id=doctor_id)
