import os
import json
from dotenv import load_dotenv
from google.genai import types
from google import genai
from app.schemas import ReviewResponse,GrammarResponse,ExampleSentenceResponse,ExplanationResponse,TranslationResponse,PronunciationResponse

load_dotenv()

GEMMA_API=os.environ['GEMMA_API_KEY']

client = genai.Client(
    api_key=GEMMA_API
)


def ask_gemma(
    system_prompt: str,
    user_prompt: str,
    response_schema=None,
    max_tokens: int = 512,
    temperature: float = 0.3,
):
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=temperature,
        top_p=0.95,
        top_k=64,
        max_output_tokens=max_tokens,
    )

    if response_schema:
        config.response_mime_type = "application/json"
        config.response_schema = response_schema

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=user_prompt,
        config=config,
    )

    return response.parsed


def explain_text(text):

    system = """
You are an expert.

Explain the likely meaning of the text.

If uncertain,
say so.

Do not invent facts.

Keep it under 100 words.
"""

    return ask_gemma(
        system,
        f"Text: {text}",
        response_schema=ExplanationResponse

    )


def pronunciation(text, language):

    system = """
You are a pronunciation assistant.

Provide an approximate Latin pronunciation.

Do not pretend certainty.

If pronunciation is unknown,
say that.
"""

    return ask_gemma(
        system,
        f"Language: {language}\ntext: {text}",
        response_schema=PronunciationResponse,
    )


def english_sentence(word):

    system = """
Generate ONE simple English sentence
naturally using the given word's meaning.

If the meaning is unknown,
say that.

Return only the sentence.
"""

    return ask_gemma(system, word, response_schema=ExampleSentenceResponse)

def suggest_translation(
    source_language,
    target_language,
    text
):

    system = f"""
You translate between
{source_language}
and
{target_language}.

If unsure,
state uncertainty.

Return only the suggested translation.
"""

    return ask_gemma(system, text, response_schema=TranslationResponse)


def grammar_review(
    text
):

    system = """
You are checking grammar.

Only identify likely grammar issues.

return the correct grammar,always return even if the grammar is right.
"""

    return ask_gemma(
        system,
        f"{text}",
        response_schema=GrammarResponse
    )

def review_contribution(
    language,
    contribution_type,
    source,
    translation
):

    system = """
You are reviewing a language dataset.

Never approve.

Never reject.

Only provide analysis.
"""

    prompt = f"""
Language:
{language}

Contribution Type:
{contribution_type}

Source:
{source}

Translation:
{translation}
"""

    return ask_gemma(system, prompt,response_schema=ReviewResponse)


