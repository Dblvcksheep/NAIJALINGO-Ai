from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    contributor = "contributor"
    reviewer = "reviewer"
    admin = "admin"


class ContributionType(str, enum.Enum):
    word = "word"
    sentence = "sentence"
    proverb = "proverb"


class ContributionStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.contributor, nullable=False)
    points = Column(Integer, default=0)
    is_verified = Column(Integer, default=0)
    profile_picture = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())
    applicant = relationship(
        "BecomeReviewer",
        back_populates="applicant",
        uselist=False,
    )


class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    region = Column(String(255), nullable=False)
    family = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Contribution(Base):
    __tablename__ = "contributions"
    id = Column(Integer, primary_key=True, index=True)
    contributor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    type = Column(Enum(ContributionType), nullable=False)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    example_usage = Column(Text, nullable=True)
    translated_usage = Column(Text, nullable=True)
    pronunciation = Column(Text, nullable=True)
    status = Column(Enum(ContributionStatus), default=ContributionStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    contributor = relationship("User", foreign_keys=[contributor_id])
    language = relationship("Language", foreign_keys=[language_id])
    ai_analysis = relationship(
        "AIAnalysis",
        back_populates="contribution",
        uselist=False,
    )


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"
    id = Column(Integer, primary_key=True, index=True)
    contribution_id = Column(Integer, ForeignKey("contributions.id"), nullable=False)
    summary = Column(Text, nullable=True)
    confidence = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    contribution = relationship(
        "Contribution",
        back_populates="ai_analysis"
    )


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    contribution_id = Column(Integer, ForeignKey("contributions.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BecomeReviewer(Base):
    __tablename__ = "becomereviewer"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language = Column(String(50), nullable=False)
    native = Column(String(50), nullable=False)
    proficiency = Column(String(50), nullable=False)
    status = Column(Enum(ContributionStatus), default=ContributionStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    applicant = relationship(
        "User",
        back_populates="applicant"
    )
