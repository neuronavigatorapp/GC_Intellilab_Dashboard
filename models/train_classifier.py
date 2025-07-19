# models/train_classifier.py

import os
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from feature_extractor import extract_features

LABELS_CSV = "data/training_labels.csv"
UPLOAD_DIR = "data/chromatograms"
MODEL_PATH = "models/gc_fault_classifier.pkl"


def train_model():
    if not os.path.exists(LABELS_CSV):
        print("No labels found.")
        return

    labels_df = pd.read_csv(LABELS_CSV)
    features = []
    targets = []

    for _, row in labels_df.iterrows():
        file_path = os.path.join(UPLOAD_DIR, row["filename"])
        if os.path.exists(file_path):
            try:
                feat = extract_features(file_path)
                features.append(feat)
                targets.append(row["label"])
            except Exception as e:
                print(f"Failed on {row['filename']}: {e}")

    if not features:
        print("No usable data for training.")
        return

    X = pd.DataFrame(features)
    y = targets

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = GradientBoostingClassifier()
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))

    joblib.dump(clf, MODEL_PATH)
    print(f"Model trained and saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
