from fastapi import APIRouter, HTTPException
import traceback
from app.services.gemma_service import (
    explain_text,
    pronunciation,
    grammar_review,
    english_sentence,
    suggest_translation,
    review_contribution,
)

from app.schemas import (
    AnalyzeRequest,
    ReviewRequest,
)


router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)



@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    try:

        translation = suggest_translation(
            source_language=request.language,
            target_language=request.target_language,
            text=request.text,
        )


        pron = pronunciation(
            text=request.text,
            language=request.language,
        )


        return {
            "translation": translation.translation,
            "pronunciation": pron.pronunciation,
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )





@router.post("/review")
def review(request: ReviewRequest):
    explanation = None
    grammar = None
    sentence = None
    analysis = None

    try:
        explanation = explain_text(text=request.translated)
    except Exception as e:
        traceback.print_exc()
        explanation = None

    try:
        grammar = grammar_review(text=request.translated)
    except Exception as e:
        traceback.print_exc()
        grammar = None

    try:
        sentence = english_sentence(word=request.translated)
    except Exception as e:
        traceback.print_exc()
        sentence = None

    try:
        analysis = review_contribution(
            language=request.language,
            contribution_type=request.contribution_type,
            source=request.source,
            translation=request.translated,
        )
    except Exception as e:
        traceback.print_exc()
        analysis = None

    return {
        "explanation": getattr(explanation, "explanation", "Unable to generate explanation."),
        "grammar": getattr(grammar, "corrected_text", None) or "No correction",
        "example_sentence": getattr(sentence, "sentence", "Unable to generate example sentence."),
        "review": {
            "confidence": getattr(analysis, "confidence", "unknown"),
            "summary": getattr(analysis, "summary", "Unable to generate review summary."),
        },
    }