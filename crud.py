from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash

def get_user(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.Email == email).first() or db.query(models.Doctor).filter(models.Doctor.Email == email).first()

def create_patient(db: Session, patient: schemas.PatientCreate):
    hashed_password = get_password_hash(patient.Password)
    patient_data = patient.dict()
    patient_data['Password'] = hashed_password
    db_patient = models.Patient(**patient_data)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    hashed_password = get_password_hash(doctor.Password)
    doctor_data = doctor.dict()
    doctor_data['Password'] = hashed_password
    db_doctor = models.Doctor(**doctor_data)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_appointments_for_patient(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.PatientID == patient_id).all()

def get_appointments_for_doctor(db: Session, doctor_id: int):
    return db.query(models.Appointment).filter(models.Appointment.DoctorID == doctor_id).all()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.AppointmentID == appointment_id).first()
    db.delete(db_appointment)
    db.commit()

def get_prescriptions_for_patient(db: Session, patient_id: int):
    return db.query(models.Prescription).filter(models.Prescription.PatientID == patient_id).all()

def get_prescriptions_for_doctor(db: Session, doctor_id: int):
    return db.query(models.Prescription).filter(models.Prescription.DoctorID == doctor_id).all()

def create_prescription(db: Session, prescription: schemas.PrescriptionCreate):
    db_prescription = models.Prescription(**prescription.dict())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def delete_prescription(db: Session, prescription_id: int):
    db_prescription = db.query(models.Prescription).filter(models.Prescription.PrescriptionID == prescription_id).first()
    db.delete(db_prescription)
    db.commit()
