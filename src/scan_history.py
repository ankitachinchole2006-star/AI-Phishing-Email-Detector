import os
import pandas as pd
from datetime import datetime

HISTORY_FOLDER = "history"
HISTORY_FILE = os.path.join(HISTORY_FOLDER, "scan_history.csv")


def save_scan(prediction, confidence):
    os.makedirs(HISTORY_FOLDER, exist_ok=True)

    new_record = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Prediction": prediction,
        "Confidence": round(confidence, 2)
    }])

    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)
        history = pd.concat([history, new_record], ignore_index=True)
    else:
        history = new_record

    history.to_csv(HISTORY_FILE, index=False)


def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)

    return pd.DataFrame(
        columns=["Timestamp", "Prediction", "Confidence"]
    )


def get_statistics():
    history = load_history()

    total_scans = len(history)

    phishing = len(
        history[history["Prediction"] == "Phishing"]
    )

    legitimate = len(
        history[history["Prediction"] == "Legitimate"]
    )

    if total_scans > 0:
        detection_rate = round(
            (phishing / total_scans) * 100,
            2
        )
    else:
        detection_rate = 0

    return {
        "total": total_scans,
        "phishing": phishing,
        "legitimate": legitimate,
        "rate": detection_rate
    }