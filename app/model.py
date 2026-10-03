from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentModel:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def predict(self, text: str) -> dict:
        scores = self.analyzer.polarity_scores(text)
        compound = scores["compound"]

        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        confidence = max(
            scores["pos"],
            scores["neg"],
            scores["neu"],
        )

        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 4),
        }


_model = None


def get_sentiment_model() -> SentimentModel:
    global _model

    if _model is None:
        _model = SentimentModel()

    return _model