from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.translator import TamilTranslator


app = FastAPI(
    title="SLM Translator",
    description="English to Tamil Translation API",
    version="1.0"
)


class TranslationRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )


class TranslationResponse(BaseModel):

    english: str
    tamil: str


@lru_cache(maxsize=1)
def get_translator():

    return TamilTranslator()


@app.get("/health")
def health_check():

    return {
        "status": "running",
        "project": "SLM_TRANSLATOR"
    }


@app.post(
    "/translate",
    response_model=TranslationResponse
)
def translate_text(request: TranslationRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter English text."
        )

    try:

        translator = get_translator()

        tamil_text = translator.translate(text)

        return TranslationResponse(
            english=text,
            tamil=tamil_text
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(error)}"
        )


# Serve frontend
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)