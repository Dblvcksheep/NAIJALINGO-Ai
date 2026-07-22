from fastapi import APIRouter, Request,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.main import templates
from app.models import Contribution,User,ContributionStatus


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
def profile_page(request: Request, db: Session = Depends(get_db)):
    user =request.session.get("user")
    if not user:
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": None, "access_message": "Please sign in to view your profile."})
    all_contribution = db.query(Contribution).filter(Contribution.contributor_id== user["id"]).count()
    approved_contribution = db.query(Contribution).filter(Contribution.contributor_id== user["id"], Contribution.status == ContributionStatus.approved).count()
    user_object = (
        db.query(User)
        .filter(User.id == user["id"])
        .first()
    )
    points = user_object.points
    return templates.TemplateResponse(request=request, name="profile.html", context={"current_user": request.session.get("user"), "stats": {"points": points, "contributions": all_contribution, "approved": approved_contribution}})
