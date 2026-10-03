from functools import lru_cache

from transformers import pipeline


MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# This model uses LABEL_0/LABEL_1/LABEL_2 in some Transformers versions.
# The mapping follows the model's documented label order:
# 0 = negative, 1 = neutral, 2 = positive.
LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
    "0": "negative",
    "1": "neutral",
    "2": "positive",
    "negative": "negative",
    "neutral": "neutral",
    "positive": "positive",
}


class SentimentModel:
    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            truncation=True,
            max_length=512,
        )

    def predict(self, text: str) -> dict:
        predictions = self.classifier(text, top_k=None)

        # Normalize output across Transformers versions.
        if predictions and isinstance(predictions[0], dict):
            items = predictions
        elif predictions and isinstance(predictions[0], list):
            items = predictions[0]
        else:
            raise RuntimeError("Unexpected model output format")

        best = max(items, key=lambda x: x["score"])
        raw_label = str(best["label"]).lower()
        sentiment = LABEL_MAP.get(raw_label, raw_label)

        if sentiment not in {"positive", "negative", "neutral"}:
            raise RuntimeError(f"Unknown model label: {best['label']}")

        return {
            "sentiment": sentiment,
            "confidence": round(float(best["score"]), 4),
        }


@lru_cache(maxsize=1)
def get_sentiment_model() -> SentimentModel:
    return SentimentModel()
