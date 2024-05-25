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

class PatientUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    DateOfBirth: Optional[date] = None
    Gender: Optional[str] = None
    Email: Optional[EmailStr] = None
    Password: Optional[str] = None
    Phone: Optional[str] = None

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

class DoctorUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Specialty: Optional[str] = None
    Email: Optional[EmailStr] = None
    Password: Optional[str] = None
    Phone: Optional[str] = None

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

class AppointmentUpdate(BaseModel):
    PatientID: Optional[int] = None
    DoctorID: Optional[int] = None
    AppointmentDate: Optional[date] = None

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

class PrescriptionUpdate(BaseModel):
    PatientID: Optional[int] = None
    MedicationID: Optional[int] = None
    DoctorID: Optional[int] = None
    PrescriptionDate: Optional[date] = None

class Prescription(BaseModel):
    PrescriptionID: int
    PatientID: int
    MedicationID: int
    DoctorID: int
    PrescriptionDate: date

    class Config:
        orm_mode = True

# Medication schema
class MedicationCreate(BaseModel):
    Name: str
    Dosage: str

class MedicationUpdate(BaseModel):
    Name: Optional[str] = None
    Dosage: Optional[str] = None

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
