import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine
import app.models

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NAIJALINGO AI", version="0.1.0")

BASE_DIR = Path(__file__).resolve().parent
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"), max_age=60 * 60 * 24 * 7)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

import os
from app.routes import auth, dashboard, contribute, review, admin, dataset, profile,ai,becomereviewer

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(contribute.router)
app.include_router(review.router)
app.include_router(admin.router)
app.include_router(dataset.router)
app.include_router(profile.router)
app.include_router(ai.router)
app.include_router(becomereviewer.router)

@app.get("/")
def landing_page(request: Request):
    return templates.TemplateResponse(request=request, name="landing.html", context={"current_user": request.session.get("user"), "active_nav": "home"})
