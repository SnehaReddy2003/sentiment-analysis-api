# Sentiment Analysis API

A REST API for English sentiment analysis built with **FastAPI** and **VADER SentimentIntensityAnalyzer**.

The API classifies text as **positive**, **negative**, or **neutral** and returns a confidence value between `0` and `1`.

## Features

* Positive / negative / neutral sentiment classification
* Confidence score from 0 to 1
* Single-text analysis
* Batch analysis for up to 10 texts
* Input validation for 1–500 words
* Health-check endpoint
* Interactive Swagger/OpenAPI documentation
* Automated API tests
* Docker support
* Sentiment model initialized once at application startup

## Project Structure

```text
sentiment-analysis-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── model.py
├── tests/
│   └── test_api.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── SUBMISSION_CHECKLIST.md
```

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
  VADER SentimentIntensityAnalyzer
          |
          v
 Positive / Negative / Neutral
```

## Approach

This project uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** for English sentiment analysis.

VADER provides positive, negative, neutral, and compound sentiment scores. The compound score is used to classify the text:

* Compound score >= `0.05` → `positive`
* Compound score <= `-0.05` → `negative`
* Otherwise → `neutral`

The API confidence value is calculated using the highest of VADER's positive, negative, and neutral scores.

The returned confidence is therefore always between `0` and `1`.

## API Endpoints

### 1. Root

`GET /`

Returns basic information about the API and links to the available endpoints.

Example response:

```json
{
  "message": "Sentiment Analysis API",
  "docs": "/docs",
  "health": "/api/health",
  "analyze": "POST /api/analyze",
  "batch_analyze": "POST /api/analyze/batch"
}
```

### 2. Health Check

`GET /api/health`

No request body is required.

Example response:

```json
{
  "status": "healthy",
  "model": "VADER SentimentIntensityAnalyzer"
}
```

### 3. Analyze One Text

`POST /api/analyze`

Request:

```json
{
  "text": "I absolutely love this product!"
}
```

Example response:

```json
{
  "sentiment": "positive",
  "confidence": 0.545
}
```

The exact confidence value depends on the input text.

### 4. Analyze Multiple Texts

`POST /api/analyze/batch`

The batch endpoint accepts between 1 and 10 texts.

Request:

```json
{
  "texts": [
    "I absolutely love this product!",
    "This product is terrible and I hate it.",
    "The package arrived today."
  ]
}
```

Example response:

```json
{
  "results": [
    {
      "sentiment": "positive",
      "confidence": 0.6
    },
    {
      "sentiment": "negative",
      "confidence": 0.608
    },
    {
      "sentiment": "neutral",
      "confidence": 1.0
    }
  ]
}
```

## Validation and Error Handling

The API validates incoming requests using Pydantic.

Rules:

* Single text must contain 1–500 whitespace-separated words.
* Batch requests must contain 1–10 texts.
* Every text in a batch must contain 1–500 words.
* Empty text is rejected.
* Empty batch requests are rejected.
* Invalid requests return HTTP `422 Unprocessable Entity`.
* Unexpected model inference failures return HTTP `500 Internal Server Error`.

## Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd sentiment-analysis-api
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Interactive API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

## Example curl

### Single text

Windows:

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

### Batch

```bash
curl -X POST "http://127.0.0.1:8000/api/analyze/batch" ^
  -H "Content-Type: application/json" ^
  -d "{\"texts\":[\"I love it!\",\"This is terrible.\",\"The package arrived today.\"]}"
```

## Testing

Run the automated tests with:

```bash
python -m pytest -v
```

Current test result:

```text
6 passed
```

The test suite covers:

* Health endpoint
* Single-text sentiment analysis
* Empty text validation
* More than 500 words validation
* Batch sentiment analysis
* More than 10 batch items validation

## Performance and Accuracy

This project uses the VADER rule-based sentiment analysis approach rather than training a new machine-learning classifier.

The current implementation has been tested for API functionality and validation, with all 6 automated tests passing.

No test-set accuracy number is claimed because a separate labeled evaluation dataset has not been run as part of the current implementation.

For a future benchmark, the following metrics can be measured on a labeled test dataset:

* Accuracy
* Precision
* Recall
* F1-score
* Inference latency

## Docker

Build the image:

```bash
docker build -t sentiment-api .
```

Run the container:

```bash
docker run -p 8000:8000 sentiment-api
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Production Considerations

For production deployment:

1. Pin dependency versions.
2. Add request logging and monitoring.
3. Add authentication and rate limiting if the API is public.
4. Run behind a production ASGI server configuration.
5. Add automated CI checks.
6. Add a labeled evaluation dataset and benchmark results if model performance reporting is required.

## Assignment Requirement Mapping

| Requirement               | Implementation                          |
| ------------------------- | --------------------------------------- |
| Python                    | Python 3.10+                            |
| API framework             | FastAPI                                 |
| Sentiment model           | VADER SentimentIntensityAnalyzer        |
| English input             | Supported                               |
| Sentiment classes         | Positive / Negative / Neutral           |
| Confidence                | Returned between 0 and 1                |
| Input length              | 1–500 words                             |
| `POST /api/analyze`       | Implemented                             |
| `POST /api/analyze/batch` | Implemented, maximum 10 texts           |
| `GET /api/health`         | Implemented                             |
| API documentation         | Swagger/OpenAPI + README                |
| Error handling            | Pydantic validation + HTTP 500 handling |
| Testing                   | Pytest, 6 tests passing                 |
| Docker                    | Dockerfile included                     |

## License

This project is provided for educational and assignment purposes.
