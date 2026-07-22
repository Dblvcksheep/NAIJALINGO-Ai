from fastapi import APIRouter, Request,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.templating import Jinja2Templates
from app.main import templates
from app.models import Contribution, ContributionStatus


router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def dashboard(request: Request,  db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": None, "access_message": "Please sign in to access your contributor workspace."})
    all_contribution = db.query(Contribution).filter(Contribution.contributor_id== user["id"]).count()
    approved_contribution = db.query(Contribution).filter(Contribution.contributor_id== user["id"], Contribution.status == ContributionStatus.approved).count()
    user_object = (
        db.query(User)
        .filter(User.id == user["id"])
        .first()
    )
    points = user_object.points
    last_three = (
        db.query(Contribution)
        .filter(Contribution.contributor_id == user["id"])
        .order_by(Contribution.created_at.desc())
        .limit(3)
        .all()
    )
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"current_user": request.session.get("user"),"last_three":last_three, "stats": {"contributions": all_contribution, "points": points, "approved": approved_contribution}})
