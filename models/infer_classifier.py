# models/infer_classifier.py

import os
import joblib
from feature_extractor import extract_features  # ✅ Fixed import

MODEL_PATH = "models/gc_fault_classifier.pkl"

def classify_chromatogram(csv_path):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found. Please run train_classifier.py first.")

    clf = joblib.load(MODEL_PATH)
    features = extract_features(csv_path)
    X = [list(features.values())]
    prediction = clf.predict(X)[0]
    confidence = max(clf.predict_proba(X)[0])

    return prediction, confidence

if __name__ == "__main__":
    path = input("Enter path to chromatogram CSV: ")
    label, score = classify_chromatogram(path)
    print(f"Predicted behavior: {label} (Confidence: {score:.2f})")
