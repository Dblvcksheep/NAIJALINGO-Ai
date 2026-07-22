from fastapi import APIRouter, Request, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Contribution, ContributionStatus, Review,User
from app.main import templates

router = APIRouter(prefix="/review", tags=["review"])


@router.get("")
def review_dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") not in  ["admin", "reviewer"]:
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": user, "access_message": "Only administrators can access the review queue."})
    pending = db.query(Contribution).filter(Contribution.status == ContributionStatus.pending).all()
    return templates.TemplateResponse(request=request, name="review.html", context={"current_user": user, "pending": pending})


@router.post("/decision")
def submit_review(request: Request,contribution_id: int = Form(...), decision: str = Form(...), comment: str = Form(None), db: Session = Depends(get_db)):
    user = request.session.get("user")
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(status_code=404, detail="Contribution not found")
    if decision == "approve":
        contribution.status = ContributionStatus.approved 
        user = db.query(User).filter(User.id == contribution.contributor_id).first()
        user.points += 10  # Award points for approved contribution
    else:
        contribution.status = ContributionStatus.rejected
    review = Review(contribution_id=contribution.id, reviewer_id=1, decision=decision, comment=comment)
    db.add(review)
    db.commit()
    pending = db.query(Contribution).filter(Contribution.status == ContributionStatus.pending).all()
    return templates.TemplateResponse(request=request, name="review.html", context={"current_user": user, "pending": pending})

