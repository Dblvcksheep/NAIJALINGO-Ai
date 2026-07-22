from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.models import User, UserRole
from app.auth import hash_password, verify_password, get_user_by_email
from app.main import templates

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={})


@router.post("/register")
def register_user(request: Request, fullname: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(fullname=fullname, email=email, password_hash=hash_password(password), role=UserRole.contributor, is_verified=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    request.session["user"] = {"id": user.id, "email": user.email, "fullname": user.fullname, "role": user.role.value}
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})


@router.post("/login")
def login_user(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    request.session["user"] = {"id": user.id, "email": user.email, "fullname": user.fullname, "role": user.role.value}
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
