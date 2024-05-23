from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = 'Patients'
    PatientID = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(100))
    LastName = Column(String(100))
    DateOfBirth = Column(Date)
    Gender = Column(String(1))
    Email = Column(String(100), unique=True, index=True)
    Password = Column(String(255))
    Phone = Column(String(15))

class Doctor(Base):
    __tablename__ = 'Doctors'
    DoctorID = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(100))
    LastName = Column(String(100))
    Specialty = Column(String(100))
    Email = Column(String(100), unique=True, index=True)
    Password = Column(String(255))
    Phone = Column(String(15))

class Medication(Base):
    __tablename__ = 'Medications'
    MedicationID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Dosage = Column(String(100))

class Appointment(Base):
    __tablename__ = 'Appointments'
    AppointmentID = Column(Integer, primary_key=True, index=True)
    PatientID = Column(Integer, ForeignKey('Patients.PatientID'))
    DoctorID = Column(Integer, ForeignKey('Doctors.DoctorID'))
    AppointmentDate = Column(Date)

    # Define relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class Prescription(Base):
    __tablename__ = 'Prescriptions'
    PrescriptionID = Column(Integer, primary_key=True, index=True)
    PatientID = Column(Integer, ForeignKey('Patients.PatientID'))
    MedicationID = Column(Integer, ForeignKey('Medications.MedicationID'))
    DoctorID = Column(Integer, ForeignKey('Doctors.DoctorID'))
    PrescriptionDate = Column(Date)

    # Define relationships
    patient = relationship("Patient", back_populates="prescriptions")
    medication = relationship("Medication", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")

# Define back_populates for relationships
Patient.appointments = relationship("Appointment", back_populates="patient")
Patient.prescriptions = relationship("Prescription", back_populates="patient")
Doctor.appointments = relationship("Appointment", back_populates="doctor")
Doctor.prescriptions = relationship("Prescription", back_populates="doctor")
Medication.prescriptions = relationship("Prescription", back_populates="medication")
