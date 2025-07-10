from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Date, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_chat_id = Column(BigInteger, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'DOCTOR' or 'PATIENT'
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    patient_details = relationship("Patient", back_populates="user", uselist=False)
    doctor_patients = relationship("Patient", back_populates="doctor", foreign_keys="[Patient.doctor_id]")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="patient_details", foreign_keys=[user_id])
    doctor = relationship("User", back_populates="doctor_patients", foreign_keys=[doctor_id])
    followups = relationship("PatientFollowup", back_populates="patient")

class PatientFollowup(Base):
    __tablename__ = "patient_followups"
    id = Column(Integer, primary_key=True, index=True)
    patient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    protocol_code = Column(String, nullable=False)
    current_schedule_step = Column(Integer, default=1)
    next_followup_date = Column(Date, nullable=False)
    status = Column(String, default='PENDING')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    patient = relationship("User", foreign_keys=[patient_user_id])
    data = relationship("FollowupData", back_populates="followup")


class FollowupData(Base):
    __tablename__ = "followup_data"
    id = Column(Integer, primary_key=True, index=True)
    followup_id = Column(Integer, ForeignKey("patient_followups.id"), nullable=False)
    data_key = Column(String)
    data_value = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    followup = relationship("PatientFollowup", back_populates="data")