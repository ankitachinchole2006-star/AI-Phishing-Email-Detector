def calculate_severity(risk_score, attack_type):

    if risk_score >= 90:
        severity = "🔴 Critical"

    elif risk_score >= 70:
        severity = "🟠 High"

    elif risk_score >= 40:
        severity = "🟡 Medium"

    else:
        severity = "🟢 Low"


    reasons = []

    if attack_type == "Credential Theft Attack":
        reasons.append(
            "Attempts to steal user credentials."
        )

    if attack_type == "Malware Delivery Attack":
        reasons.append(
            "Potential malicious attachment or payload."
        )

    if attack_type == "Business Email Compromise":
        reasons.append(
            "Possible impersonation or fraud attempt."
        )


    if not reasons:
        reasons.append(
            "No major attack pattern detected."
        )


    return severity, reasons