from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Language, Contribution,ContributionStatus,BecomeReviewer,UserRole
from app.main import templates

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": user, "access_message": "Only administrators can access the admin dashboard."})
    users = db.query(User).all()
    languages = db.query(Language).all()
    contributions = db.query(Contribution).all()
    pending= db.query(BecomeReviewer).filter(BecomeReviewer.status == ContributionStatus.pending).all()
    return templates.TemplateResponse(request=request, name="admin.html", context={"current_user": user, "pending": pending, "users": users, "languages": languages, "contributions": contributions, "stats": {"users": len(users), "languages": len(languages), "contributions": len(contributions)}})


@router.post("/languages")
def add_language(name: str = Form(...), region: str = Form(...), family: str = Form(...), db: Session = Depends(get_db)):
    language = Language(name=name, region=region, family=family)
    db.add(language)
    db.commit()
    return {"status": "created"}

@router.post("/reviewer/decision")
def submit_review(applicant_id: int = Form(...), decision: str = Form(...), db: Session = Depends(get_db)):
    applicant = db.query(BecomeReviewer).filter(BecomeReviewer.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Contribution not found")
    
    if decision == "approve":
        applicant.status = ContributionStatus.approved 
        user = db.query(User).filter(User.id == applicant.applicant_id).first()
        user.role = UserRole.reviewer
    else:
        applicant.status = ContributionStatus.rejected
    db.commit()
    return {"status": "ok"}
