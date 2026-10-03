from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from .model import get_sentiment_model


class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        description="English text containing 1 to 500 words."
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("text must not be empty")

        word_count = len(value.split())

        if word_count < 1 or word_count > 500:
            raise ValueError("text must contain between 1 and 500 words")

        return value


class BatchAnalyzeRequest(BaseModel):
    texts: List[str] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="List containing 1 to 10 English texts."
    )

    @field_validator("texts")
    @classmethod
    def validate_texts(cls, values: List[str]) -> List[str]:
        cleaned = []

        for value in values:
            value = value.strip()

            if not value:
                raise ValueError("each text must not be empty")

            word_count = len(value.split())

            if word_count < 1 or word_count > 500:
                raise ValueError(
                    "each text must contain between 1 and 500 words"
                )

            cleaned.append(value)

        return cleaned


class SentimentResult(BaseModel):
    sentiment: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class BatchAnalyzeResponse(BaseModel):
    results: List[SentimentResult]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the sentiment model once when the application starts.
    get_sentiment_model()
    yield


app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0.0",
    description=(
        "REST API for English sentiment classification using "
        "VADER SentimentIntensityAnalyzer."
    ),
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Sentiment Analysis API",
        "docs": "/docs",
        "health": "/api/health",
        "analyze": "POST /api/analyze",
        "batch_analyze": "POST /api/analyze/batch",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "model": "VADER SentimentIntensityAnalyzer",
    }


@app.post("/api/analyze", response_model=SentimentResult)
def analyze(request: AnalyzeRequest):
    try:
        return get_sentiment_model().predict(request.text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {exc}",
        ) from exc


@app.post("/api/analyze/batch", response_model=BatchAnalyzeResponse)
def analyze_batch(request: BatchAnalyzeRequest):
    try:
        model = get_sentiment_model()

        return {
            "results": [
                model.predict(text)
                for text in request.texts
            ]
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {exc}",
        ) from exc