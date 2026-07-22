from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Language, Contribution, ContributionStatus
from app.main import templates

router = APIRouter(prefix="/dataset", tags=["dataset"])


@router.get("")
def dataset_page(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": None, "access_message": "Please sign in to view the dataset overview."})
    languages = db.query(Language).all()
    stats = []
    for language in languages:
        contributions = db.query(Contribution).filter(Contribution.language_id == language.id).all()
        stats.append({
            "language": language,
            "total": len(contributions),
            "approved": sum(1 for item in contributions if item.status == ContributionStatus.approved),
            "pending": sum(1 for item in contributions if item.status == ContributionStatus.pending),
        })
    return templates.TemplateResponse(request=request, name="dataset.html", context={"current_user": user, "stats": stats})
