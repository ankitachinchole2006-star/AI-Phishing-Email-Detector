import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_NAME = "AI-Powered Phishing Email Detector"

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "phishing_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vectorizer.pkl"
)