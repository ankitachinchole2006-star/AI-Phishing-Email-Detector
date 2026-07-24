def classify_attack(text):

    text = text.lower()


    if any(word in text for word in [
        "password",
        "login",
        "verify account",
        "credential"
    ]):
        return (
            "Credential Theft Attack",
            "Attacker is attempting to steal login credentials."
        )


    elif any(word in text for word in [
        "bank",
        "account suspended",
        "payment",
        "invoice"
    ]):
        return (
            "Financial Scam Attack",
            "Attacker is using financial-related social engineering."
        )


    elif any(word in text for word in [
        "attachment",
        ".exe",
        "download file",
        "install"
    ]):
        return (
            "Malware Delivery Attack",
            "Email may contain malicious files or downloads."
        )


    elif any(word in text for word in [
        "urgent",
        "immediately",
        "act now"
    ]):
        return (
            "Social Engineering Attack",
            "Attacker is creating urgency to manipulate the user."
        )


    else:
        return (
            "General Phishing Attack",
            "Suspicious patterns commonly associated with phishing."
        )