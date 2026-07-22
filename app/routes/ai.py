from fastapi import APIRouter, HTTPException
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

    try:

        explanation = explain_text(
            text=request.translated
        )


        grammar = grammar_review(
            text=request.translated
        )


        sentence = english_sentence(
            word=request.translated
        )


        analysis = review_contribution(
            language=request.language,
            contribution_type=request.contribution_type,
            source=request.source,
            translation=request.translated,
        )


        return {

            "explanation": explanation.explanation,


            "grammar": grammar.corrected_text,


            "example_sentence": sentence.sentence,


            "review": {

                "confidence": analysis.confidence,

                "summary": analysis.summary

            }

        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"AI review failed: {str(e)}"
        )