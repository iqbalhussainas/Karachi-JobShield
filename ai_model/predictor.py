
from functools import lru_cache
from pathlib import Path

import joblib


# Find the AI model files
AI_FOLDER = Path(__file__).resolve().parent

MODEL_PATH = AI_FOLDER / "models" / "jobshield_model.pkl"
VECTORIZER_PATH = AI_FOLDER / "models" / "tfidf_vectorizer.pkl"


# Load the model and vectorizer only once
@lru_cache(maxsize=1)
def load_ai_components():

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    return model, vectorizer


# Predict whether a job advertisement is fraudulent
def predict_job_fraud(job_text):

    model, vectorizer = load_ai_components()

    text_vector = vectorizer.transform([job_text])

    prediction = model.predict(text_vector)[0]

    return int(prediction)
