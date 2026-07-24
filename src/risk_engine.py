def calculate_risk(prediction, confidence, indicators):

    risk_score = 0

    # ML prediction
    if prediction == 1:
        risk_score += 50

    # Confidence contribution
    if confidence >= 90:
        risk_score += 30
    elif confidence >= 70:
        risk_score += 20
    else:
        risk_score += 10

    # Threat indicators contribution
    risk_score += len(indicators) * 3

    # Maximum score
    if risk_score > 100:
        risk_score = 100


    # Risk category

    if risk_score >= 70:
        level = "HIGH 🔴"

    elif risk_score >= 40:
        level = "MEDIUM 🟡"

    else:
        level = "LOW 🟢"


    return level, risk_score