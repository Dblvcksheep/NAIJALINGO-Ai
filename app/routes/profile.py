from fastapi import APIRouter, Request
from app.main import templates

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
def profile_page(request: Request):
    if not request.session.get("user"):
        return templates.TemplateResponse(request=request, name="locked.html", context={"current_user": None, "access_message": "Please sign in to view your profile."})
    return templates.TemplateResponse(request=request, name="profile.html", context={"current_user": request.session.get("user"), "stats": {"points": 120, "contributions": 4, "approved": 2}})
