from fastapi import APIRouter, Request, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.models import BecomeReviewer

router = APIRouter(prefix="/becomereviewer", tags=["becomereviewer"])


@router.get("")
def becomereviewer(request: Request):
    user = request.session.get("user")
    if not user:
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": user, "access_message": "Only Logged in user can view this page."})
    
    return templates.TemplateResponse(request=request, name="becomereviewer.html", context={"languages": db.query(Language).all()})

@router.post("/submit")
def submitapplication(request: Request,language: int = Form(...), native: str = Form(...), proficiency: str = Form(None), db: Session = Depends(get_db)):
    user = request.session.get("user")
    application = BecomeReviewer(
        applicant_id=user["id"],
        language = language,
        native = native,
        proficiency = proficiency
    )
    db.add(application)
    db.commit()
    return {"status": "ok"}
    
