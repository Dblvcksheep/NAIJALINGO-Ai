# Northern Voices AI

## Overview
Northern Voices AI is an AI-assisted language data collection platform for Northern Nigerian languages. The platform keeps native speakers as the source of truth while using Gemma-style assistance to suggest translations, example sentences, grammar feedback, and meaning explanations.

## Architecture
- FastAPI for the web application
- SQLAlchemy 2.0 for ORM models
- SQLite for local development and PostgreSQL-ready configuration
- Jinja2 for server-rendered HTML templates
- Modular route/service structure

## Features
- Landing page with mission and impact messaging
- Contributor dashboard and contribution flow
- Reviewer workflow for approval and rejection
- Dataset overview with aggregate statistics only
- Admin panel for language management
- AI analysis suggestions generated through a service layer

## Tech stack
- FastAPI
- SQLAlchemy
- Pydantic
- Jinja2
- Python dotenv
- Passlib + bcrypt

## Installation
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update values.

## Running locally
```bash
uvicorn app.main:app --reload
```

## Database migrations
The project uses SQLAlchemy models and can be bootstrapped with:
```bash
python -c "from app.database import engine, Base; from app import models; Base.metadata.create_all(bind=engine)"
```

## Gemma integration overview
The AI assistance is handled through the service layer in `app/services/gemma_service.py`. Suggestions are advisory and never replace human review.

## Folder structure
- `app/main.py` – application entrypoint
- `app/routes/` – route modules
- `app/services/` – AI and business logic services
- `app/models.py` – ORM models
- `app/schemas.py` – request/response schemas
- `app/templates/` – server-rendered pages
- `app/static/` – CSS and JavaScript assets
