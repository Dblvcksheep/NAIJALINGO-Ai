from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Language, Contribution, ContributionType, ContributionStatus, AIAnalysis
from app.main import templates

router = APIRouter(tags=["contribute"])


@router.get("/contribute")
def contribute_page(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("user"):
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": None, "access_message": "Please sign in to start contributing."})
    languages = db.query(Language).all()
    return templates.TemplateResponse(request=request, name="contribute.html", context={"current_user": request.session.get("user"), "languages": languages})


@router.post("/contribute")
def submit_contribution(
    request: Request,
    language_id: int = Form(...),
    type: str = Form(...),
    source_text: str = Form(...),
    translated_text: str = Form(None),
    explanation: str = Form(None),
    example_usage: str = Form(None),
    summary: str = Form(None),
    confidence: str = Form(None),
    pronunciation: str = Form(None),
    translated_usage: str = Form(None),
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    language = db.query(Language).filter(Language.id == language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    existing_contribution = db.query(Contribution).filter(Contribution.source_text==source_text).first()
    
    if existing_contribution:
        raise HTTPException(status_code=404, detail="Same contribution in database")
    contribution = Contribution(
        contributor_id=user["id"],
        language_id=language_id,
        type=ContributionType(type),
        source_text=source_text,
        translated_text=translated_text,
        pronunciation = pronunciation,
        explanation=explanation,
        example_usage=example_usage,
        translated_usage = translated_usage,
        status=ContributionStatus.pending,
    )
    db.add(contribution)
    db.flush()
    
    

    ai_analysis = AIAnalysis(
        contribution_id=contribution.id,
        summary=summary,
        confidence=confidence,
    )
    db.add(ai_analysis)
    db.commit()
    db.refresh(contribution)
    return templates.TemplateResponse(request=request, name="contribute.html", context={"current_user": request.session.get("user"), "languages": db.query(Language).all(), "submitted": True})

