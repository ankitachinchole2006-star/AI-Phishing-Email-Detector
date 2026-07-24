import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# Load dataset
data = pd.read_csv("data/phishing_legit_dataset_KD_10000.csv")

# Features and labels
X = data["text"]
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words="english")

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Predictions
predictions = model.predict(X_test_vec)

# Evaluation
print("=" * 50)
print("MODEL PERFORMANCE")
print("=" * 50)

print(f"Accuracy : {accuracy_score(y_test, predictions):.4f}")

print("\nClassification Report:\n")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, predictions))

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\n✅ Model saved successfully!")
