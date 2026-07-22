from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.models import ContributionType, ContributionStatus, UserRole


class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LanguageCreate(BaseModel):
    name: str
    region: str
    family: str


class ContributionCreate(BaseModel):
    language_id: int
    type: ContributionType
    source_text: str
    translated_text: Optional[str] = None
    explanation: Optional[str] = None
    example_usage: Optional[str] = None
    translated_usage: Optional[str] = None


class ReviewCreate(BaseModel):
    decision: str
    comment: Optional[str] = None

class ExplanationResponse(BaseModel):
    explanation: str

class PronunciationResponse(BaseModel):
    pronunciation: str
    
class TranslationResponse(BaseModel):
    translation: str

class ExampleSentenceResponse(BaseModel):
    sentence: str

class GrammarResponse(BaseModel):
    corrected_text: str


class ReviewResponse(BaseModel):
    confidence: str
    summary: str

class AnalyzeRequest(BaseModel):
    language: str
    target_language: str
    text: str


class ReviewRequest(BaseModel):
    language: str
    contribution_type: str
    source: str
    translated: str