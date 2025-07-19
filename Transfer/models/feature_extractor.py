# models/feature_extractor.py

import pandas as pd
import numpy as np

def extract_features(csv_path):
    df = pd.read_csv(csv_path)
    df = df.dropna()

    if df.shape[1] < 2:
        raise ValueError("CSV must contain at least two columns: Time and Signal")

    time = df.iloc[:, 0].values
    signal = df.iloc[:, 1].values

    features = {
        "peak_count": int(np.sum((signal[1:-1] > signal[:-2]) & (signal[1:-1] > signal[2:]))),
        "signal_mean": float(np.mean(signal)),
        "signal_std": float(np.std(signal)),
        "signal_max": float(np.max(signal)),
        "baseline_drift": float(signal[-1] - signal[0]),
        "run_time": float(time[-1] - time[0])
    }

    # Symmetry approximation
    half = len(signal) // 2
    features["symmetry"] = float(np.mean(signal[:half])) / float(np.mean(signal[half:]) + 1e-6)

    return features
