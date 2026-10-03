from nltk.corpus import movie_reviews
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from app.model import get_sentiment_model


def main():
    model = get_sentiment_model()

    texts = []
    true_labels = []

    for file_id in movie_reviews.fileids():
        words = movie_reviews.words(file_id)
        text = " ".join(words)

        label = movie_reviews.categories(file_id)[0]

        texts.append(text)
        true_labels.append(label)

    predicted_labels = []

    for text in texts:
        result = model.predict(text)

        predicted_labels.append(
            "pos" if result["sentiment"] == "positive" else
            "neg" if result["sentiment"] == "negative" else
            "neutral"
        )

    # Movie Reviews contains positive/negative labels only.
    # Neutral predictions are treated as incorrect.
    accuracy = accuracy_score(true_labels, predicted_labels)

    precision = precision_score(
        true_labels,
        predicted_labels,
        labels=["pos", "neg"],
        average="weighted",
        zero_division=0,
    )

    recall = recall_score(
        true_labels,
        predicted_labels,
        labels=["pos", "neg"],
        average="weighted",
        zero_division=0,
    )

    f1 = f1_score(
        true_labels,
        predicted_labels,
        labels=["pos", "neg"],
        average="weighted",
        zero_division=0,
    )

    print("VADER Evaluation - NLTK Movie Reviews")
    print("---------------------------------------")
    print(f"Number of documents: {len(texts)}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")


if __name__ == "__main__":
    main()