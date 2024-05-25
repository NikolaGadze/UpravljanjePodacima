from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash

def get_user(db: Session, email: str):
    user = db.query(models.Patient).filter(models.Patient.Email == email).first()
    if user:
        return user
    return db.query(models.Doctor).filter(models.Doctor.Email == email).first()

def get_patient_by_email(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.Email == email).first()

def get_doctor_by_email(db: Session, email: str):
    return db.query(models.Doctor).filter(models.Doctor.Email == email).first()

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

# Remaining CRUD operations for appointments, prescriptions, and medications
# ...

def get_appointments_for_patient(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.PatientID == patient_id).all()

def get_appointments_for_doctor(db: Session, doctor_id: int):
    return db.query(models.Appointment).filter(models.Appointment.DoctorID == doctor_id).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.AppointmentID == appointment_id).first()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, appointment_id: int, appointment: schemas.AppointmentUpdate):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.AppointmentID == appointment_id).first()
    if db_appointment:
        for key, value in appointment.dict().items():
            if value is not None:
                setattr(db_appointment, key, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.AppointmentID == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()

def get_prescriptions_for_patient(db: Session, patient_id: int):
    return db.query(models.Prescription).filter(models.Prescription.PatientID == patient_id).all()

def get_prescriptions_for_doctor(db: Session, doctor_id: int):
    return db.query(models.Prescription).filter(models.Prescription.DoctorID == doctor_id).all()

def get_prescription(db: Session, prescription_id: int):
    return db.query(models.Prescription).filter(models.Prescription.PrescriptionID == prescription_id).first()

def create_prescription(db: Session, prescription: schemas.PrescriptionCreate):
    db_prescription = models.Prescription(**prescription.dict())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def update_prescription(db: Session, prescription_id: int, prescription: schemas.PrescriptionUpdate):
    db_prescription = db.query(models.Prescription).filter(models.Prescription.PrescriptionID == prescription_id).first()
    if db_prescription:
        for key, value in prescription.dict().items():
            if value is not None:
                setattr(db_prescription, key, value)
        db.commit()
        db.refresh(db_prescription)
    return db_prescription

def delete_prescription(db: Session, prescription_id: int):
    db_prescription = db.query(models.Prescription).filter(models.Prescription.PrescriptionID == prescription_id).first()
    if db_prescription:
        db.delete(db_prescription)
        db.commit()

def get_all_doctors(db: Session):
    return db.query(models.Doctor).all()

def update_patient(db: Session, patient_id: int, patient: schemas.PatientUpdate):
    db_patient = db.query(models.Patient).filter(models.Patient.PatientID == patient_id).first()
    if db_patient:
        for key, value in patient.dict().items():
            if value is not None:
                setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(models.Patient).filter(models.Patient.PatientID == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()

def update_doctor(db: Session, doctor_id: int, doctor: schemas.DoctorUpdate):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.DoctorID == doctor_id).first()
    if db_doctor:
        for key, value in doctor.dict().items():
            if value is not None:
                setattr(db_doctor, key, value)
        db.commit()
        db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.DoctorID == doctor_id).first()
    if db_doctor:
        db.delete(db_doctor)
        db.commit()



