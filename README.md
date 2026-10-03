# Sentiment Analysis API

A production-style REST API for English sentiment analysis built with **FastAPI** and **Hugging Face Transformers**.

## Features

- Positive / negative / neutral classification
- Confidence score from 0 to 1
- Single-text analysis
- Batch analysis for up to 10 texts
- Input validation for 1–500 words
- Health-check endpoint
- Automatic interactive Swagger documentation
- Unit/API tests
- Docker support
- Model loaded once at application startup

## Architecture

```text
Client
  |
  v
FastAPI
  |
  +--> Pydantic validation
  |
  +--> SentimentModel
          |
          v
    Hugging Face Transformers
          |
          v
cardiffnlp/twitter-roberta-base-sentiment-latest
```

### Why this model?

The assignment requires three classes: positive, negative and neutral. A model such as
`distilbert-base-uncased-finetuned-sst-2-english` only provides positive/negative labels,
so this project uses `cardiffnlp/twitter-roberta-base-sentiment-latest`, which provides
the required three-way sentiment classification.

The model is a pretrained RoBERTa-based sentiment classifier. It is particularly useful
for short informal English text and returns a probability-like score for each class.

## API

### 1. Health check

`GET /api/health`

Response:

```json
{
  "status": "healthy",
  "model": "cardiffnlp/twitter-roberta-base-sentiment-latest"
}
```

### 2. Analyze one text

`POST /api/analyze`

Request:

```json
{
  "text": "I absolutely loved the movie. The acting was excellent!"
}
```

Response:

```json
{
  "sentiment": "positive",
  "confidence": 0.9971
}
```

### 3. Analyze multiple texts

`POST /api/analyze/batch`

Request:

```json
{
  "texts": [
    "The product is excellent.",
    "I am disappointed with the service.",
    "The package arrived today."
  ]
}
```

Response:

```json
{
  "results": [
    {
      "sentiment": "positive",
      "confidence": 0.997
    },
    {
      "sentiment": "negative",
      "confidence": 0.991
    },
    {
      "sentiment": "neutral",
      "confidence": 0.812
    }
  ]
}
```

## Validation and error handling

- Single text must contain 1–500 whitespace-separated words.
- Batch requests contain 1–10 texts.
- Every batch text must contain 1–500 words.
- Empty strings are rejected with HTTP 422.
- Unexpected inference failures return HTTP 500.
- FastAPI automatically produces structured validation errors.

## Local setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd sentiment-analysis-api
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health: `http://127.0.0.1:8000/api/health`

The first startup downloads the Hugging Face model. Later runs use the local Hugging
Face cache.

## Example curl

```bash
curl -X POST "http://127.0.0.1:8000/api/analyze" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"This is an amazing application!\"}"
```

Linux/macOS:

```bash
curl -X POST "http://127.0.0.1:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text":"This is an amazing application!"}'
```

## Testing

Run:

```bash
pytest -q
```

The tests mock the model, so they do not require downloading the Hugging Face model.

## Performance and accuracy

This implementation uses a pretrained model rather than training a new classifier.
Therefore, the project does not claim a newly measured test-set accuracy.

For a submission report, benchmark the exact model/version on a held-out dataset and
record:

- Accuracy
- Precision
- Recall
- F1-score
- Inference latency
- Hardware used

A reproducible evaluation can be added with the Hugging Face `datasets` library using
a dataset with positive/neutral/negative labels. Do not report an accuracy number unless
you have actually run that evaluation.

## Production considerations

For deployment:

1. Use a CPU/GPU instance appropriate for the model.
2. Keep the model loaded globally rather than loading it for every request.
3. Add request logging and monitoring.
4. Add authentication/rate limiting if the API is public.
5. Pin dependencies and rebuild regularly for security updates.
6. Consider multiple Uvicorn/Gunicorn workers only when memory capacity allows it,
   because each worker may load its own model copy.

## Docker

Build:

```bash
docker build -t sentiment-api .
```

Run:

```bash
docker run -p 8000:8000 sentiment-api
```

Then open `http://127.0.0.1:8000/docs`.

## Deployment to Render / Railway

The included `Dockerfile` can be deployed as a Docker service.

Alternatively, use:

```text
Build command:
pip install -r requirements.txt

Start command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Make sure the deployment has enough RAM for PyTorch + the transformer model.

## Suggested GitHub submission structure

```text
sentiment-analysis-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── model.py
├── tests/
│   └── test_api.py
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## Assignment requirement mapping

| Requirement | Implementation |
|---|---|
| Pretrained/trained model | Hugging Face RoBERTa sentiment model |
| English | English sentiment model |
| 3 labels | positive / negative / neutral |
| Confidence 0–1 | Returned for every prediction |
| 1–500 words | Pydantic validation |
| POST /api/analyze | Implemented |
| POST /api/analyze/batch | Implemented, max 10 |
| GET /api/health | Implemented |
| Documentation | README + Swagger/OpenAPI |
| Error handling | Validation + inference handling |
| Code organization | app/model.py + app/main.py + tests |
| Deployment | Dockerfile + Render/Railway instructions |
