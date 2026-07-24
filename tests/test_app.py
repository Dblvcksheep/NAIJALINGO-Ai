from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app import models
from app.auth import hash_password, verify_password

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_landing_page():
    response = client.get("/")
    assert response.status_code == 200


def test_login_page():
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_dashboard_page():
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_protected_links_are_hidden_for_guests():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert 'data-nav="dashboard"' not in html
    assert 'data-nav="contribute"' not in html
    assert 'data-nav="review"' not in html
    assert 'data-nav="dataset"' not in html
    assert 'data-nav="profile"' not in html
    assert 'data-nav="admin"' not in html


def test_password_hashing_round_trip():
    password = "secure-password-123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_ai_review_is_resilient_to_individual_ai_failures(monkeypatch):
    from app.routes import ai as ai_routes

    class DummyResponse:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    monkeypatch.setattr(
        ai_routes,
        "explain_text",
        lambda text: DummyResponse(explanation="Meaning is clear."),
    )
    monkeypatch.setattr(
        ai_routes,
        "grammar_review",
        lambda text: (_ for _ in ()).throw(RuntimeError("grammar parsing failed")),
    )
    monkeypatch.setattr(
        ai_routes,
        "english_sentence",
        lambda word: DummyResponse(sentence="This is a natural English sentence."),
    )
    monkeypatch.setattr(
        ai_routes,
        "review_contribution",
        lambda **kwargs: DummyResponse(confidence="medium", summary="Looks acceptable."),
    )

    response = client.post(
        "/ai/review",
        json={
            "language": "English",
            "contribution_type": "translation",
            "source": "Hello",
            "translated": "Hello",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["explanation"] == "Meaning is clear."
    assert payload["grammar"] == "No correction"
    assert payload["example_sentence"] == "This is a natural English sentence."
    assert payload["review"]["confidence"] == "medium"
    assert payload["review"]["summary"] == "Looks acceptable."


def test_gemma_wrapper_recovers_from_fenced_json(monkeypatch):
    from app.services import gemma_service
    from app.schemas import GrammarResponse

    class FakePart:
        def __init__(self, text):
            self.text = text

    class FakeContent:
        def __init__(self, parts):
            self.parts = parts

    class FakeCandidate:
        def __init__(self, text):
            self.content = FakeContent([FakePart(text)])

    class FakeResponse:
        def __init__(self, text):
            self.parsed = None
            self.candidates = [FakeCandidate(text)]

    monkeypatch.setattr(
        gemma_service.client.models,
        "generate_content",
        lambda **kwargs: FakeResponse('```\n{"corrected_text": "Car"}\n```'),
    )

    result = gemma_service.grammar_review(text="car")

    assert isinstance(result, GrammarResponse)
    assert result.corrected_text == "Car"