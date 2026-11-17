from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

# Small starter dataset for our student prototype.
# We will expand and evaluate it before relying on predictions.
TRAINING_TEXTS = [
    "large pothole broken road damaged street",
    "road surface cracked and vehicles struggling",
    "no water supply in the residential area",
    "drinking water pipe leaking",
    "electric pole wires sparking",
    "street light not working electricity failure",
    "garbage not collected waste overflowing",
    "dirty surroundings and sanitation problem",
    "sewage water overflowing onto the road",
    "drain blocked and flooding after rain",
    "dangerous exposed electrical wire near people",
    "person trapped in a dangerous situation",
]

TRAINING_LABELS = [
    "Roads", "Roads",
    "Water", "Water",
    "Electricity", "Electricity",
    "Sanitation", "Sanitation",
    "Drainage", "Drainage",
    "Safety", "Safety",
]


def build_model():
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LinearSVC(class_weight="balanced")),
    ])
    model.fit(TRAINING_TEXTS, TRAINING_LABELS)
    return model


model = build_model()


def predict_category(title: str, description: str) -> str:
    complaint_text = f"{title}. {description}"
    return str(model.predict([complaint_text])[0])

