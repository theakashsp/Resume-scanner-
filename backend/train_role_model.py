# ==============================================================================
# TECH STACK: [Scikit-Learn & Joblib] - TF-IDF Vectorization & Logistic Regression ML Classifier
# ==============================================================================
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

_BASE_DIR = Path(__file__).resolve().parent

# Baseline training dataset for ML role classification
training_data = [
    # ML Engineer
    ("python machine learning deep learning tensorflow pytorch ai data models", "Machine Learning Engineer"),
    ("neural networks nlp computer vision python ai models llm", "Machine Learning Engineer"),

    # Data Analyst
    ("excel sql data analysis power bi tableau statistics pandas visualization", "Data Analyst"),
    ("business intelligence dashboards sql reporting analytics metrics", "Data Analyst"),

    # Full Stack
    ("html css javascript react node mongodb full stack web typescript", "Full Stack Developer"),
    ("frontend backend api react express database rest microservices", "Full Stack Developer"),

    # DevOps
    ("docker kubernetes aws ci cd linux devops automation terraform", "DevOps Engineer"),
    ("cloud deployment terraform aws pipeline monitoring ansible", "DevOps Engineer"),
]

texts = [x[0] for x in training_data]
labels = [x[1] for x in training_data]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(texts)

model = LogisticRegression(random_state=42)
model.fit(X, labels)

# Save model and vectorizer with absolute paths relative to backend directory
model_path = _BASE_DIR / "role_model.pkl"
vec_path = _BASE_DIR / "role_vectorizer.pkl"

joblib.dump(model, model_path)
joblib.dump(vectorizer, vec_path)

print(f"[Role Model] Model trained and saved successfully to {model_path.name} and {vec_path.name}")
