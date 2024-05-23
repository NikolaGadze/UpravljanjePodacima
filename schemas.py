from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

# Patient schemas
class PatientCreate(BaseModel):
    FirstName: str
    LastName: str
    DateOfBirth: date
    Gender: str
    Email: EmailStr
    Password: str
    Phone: str

class Patient(BaseModel):
    PatientID: int
    FirstName: str
    LastName: str
    DateOfBirth: date
    Gender: str
    Email: EmailStr
    Phone: str

    class Config:
        orm_mode = True

# Doctor schemas
class DoctorCreate(BaseModel):
    FirstName: str
    LastName: str
    Specialty: str
    Email: EmailStr
    Password: str
    Phone: str

class Doctor(BaseModel):
    DoctorID: int
    FirstName: str
    LastName: str
    Specialty: str
    Email: EmailStr
    Phone: str

    class Config:
        orm_mode = True

# Appointment schemas
class AppointmentCreate(BaseModel):
    PatientID: int
    DoctorID: int
    AppointmentDate: date

class Appointment(BaseModel):
    AppointmentID: int
    PatientID: int
    DoctorID: int
    AppointmentDate: date

    class Config:
        orm_mode = True

# Prescription schemas
class PrescriptionCreate(BaseModel):
    PatientID: int
    MedicationID: int
    DoctorID: int
    PrescriptionDate: date

class Prescription(BaseModel):
    PrescriptionID: int
    PatientID: int
    MedicationID: int
    DoctorID: int
    PrescriptionDate: date

    class Config:
        orm_mode = True

# Medication schema
class Medication(BaseModel):
    MedicationID: int
    Name: str
    Dosage: str

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
