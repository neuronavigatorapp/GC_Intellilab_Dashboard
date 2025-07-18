# 1️⃣ Imports
import pandas as pd
import numpy as np
import os

# 2️⃣ CSV File Path
CSV_PATH = os.path.join("data", "shared_files", "GC_Master_Compound_Database_with_Scaffolds.csv")

# 3️⃣ Load & Filter Compound Data
def load_compound_data(method: str = None):
    df = pd.read_csv(CSV_PATH)

    if method and method != "All":
        df = df[df["Method"] == method]

    df = df[df["BoilingPoint"].notna() & (df["BoilingPoint"] != "")]
    df["BoilingPoint"] = df["BoilingPoint"].astype(float)

    return df.sort_values("BoilingPoint").reset_index(drop=True)

# 4️⃣ Simulate Retention Times
def simulate_retention_times(df, oven_start, ramp_rate, flow_rate):
    retention_data = []
    for _, row in df.iterrows():
        bp = row["BoilingPoint"]
        rt = max((bp - oven_start) / ramp_rate * (1.1 / flow_rate), 0.1)
        retention_data.append({
            "Compound": row["Compound"],
            "RT": round(rt, 2),
            "Class": row["Class"],
            "Formula": row["Formula"]
        })
    return pd.DataFrame(retention_data)

# 5️⃣ Generate Chromatogram with Optional Issue Simulation
def generate_chromatogram(rt_df, run_time=30, resolution=1000, issue=None):
    time = np.linspace(0, run_time, resolution)
    signal = np.zeros_like(time)

    for _, row in rt_df.iterrows():
        rt = row["RT"]
        height = 1.0
        width = 0.3 + rt * 0.02

        if issue == "Tailing":
            shape = (time - rt) / width
            peak = height / ((1 + shape ** 2) ** 1.5)
        elif issue == "Fronting":
            shape = (time - rt) / width
            peak = height * np.exp(-np.abs(shape) ** 1.5)
        elif issue == "Signal Loss":
            height *= 0.4
            peak = height * np.exp(-((time - rt) ** 2) / (2 * width ** 2))
        elif issue == "Baseline Drift":
            baseline = np.linspace(0, 0.3, resolution)
            peak = height * np.exp(-((time - rt) ** 2) / (2 * width ** 2))
            signal += baseline
        elif issue == "Ghost Peaks":
            ghost_rt = rt + 1.5
            ghost_peak = 0.3 * np.exp(-((time - ghost_rt) ** 2) / (2 * width ** 2))
            peak = height * np.exp(-((time - rt) ** 2) / (2 * width ** 2))
            signal += ghost_peak
        else:
            peak = height * np.exp(-((time - rt) ** 2) / (2 * width ** 2))

        signal += peak

    return pd.DataFrame({"Time (min)": time, "Detector Response": signal})

# 6️⃣ Get Available GC Methods
def get_available_methods():
    df = pd.read_csv(CSV_PATH)
    methods = df["Method"].dropna().unique().tolist()
    return ["All"] + sorted(methods)

# 7️⃣ ASTM Method Reference Links
def get_method_reference_url(method_code):
    doc_map = {
        "D1945": "https://www.astm.org/d1945",
        "D1946": "https://www.astm.org/d1946",
        "D2163": "https://www.astm.org/d2163",
        "D2593": "https://www.astm.org/d2593",
        "D2597": "https://www.astm.org/d2597",
        "D2712": "https://www.astm.org/d2712",
        "D4815": "https://www.astm.org/d4815",
        "D5134": "https://www.astm.org/d5134",
        "D5441": "https://www.astm.org/d5441",
        "D5501": "https://www.astm.org/d5501",
        "D5504": "https://www.astm.org/d5504",
        "D5580": "https://www.astm.org/d5580",
        "D5599": "https://www.astm.org/d5599",
        "D5623": "https://www.astm.org/d5623",
        "D6550": "https://www.astm.org/d6550",
        "D6729": "https://www.astm.org/d6729",
        "D6730": "https://www.astm.org/d6730",
        "D7011": "https://www.astm.org/d7011",
        "D7423": "https://www.astm.org/d7423",
        "D7756": "https://www.astm.org/d7756",
        "D7833": "https://www.astm.org/d7833",
        "D7862": "https://www.astm.org/d7862",
        "D7994": "https://www.astm.org/d7994",
        "D8071": "https://www.astm.org/d8071"
    }

    key = method_code.replace("ASTM ", "").strip()
    return doc_map.get(key, "")
