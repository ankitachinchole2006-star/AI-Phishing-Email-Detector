import re

# Suspicious keywords
SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "password",
    "login",
    "account",
    "bank",
    "click",
    "confirm",
    "limited time",
    "suspended",
    "security alert",
    "invoice",
    "payment",
    "gift card",
    "otp",
    "reset",
    "immediately",
    "winner",
    "claim",
    "crypto"
]


def detect_indicators(text):
    """
    Detect common phishing indicators in an email.

    Returns:
        List[str]
    """

    indicators = []

    lower_text = text.lower()

    # Suspicious keywords
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in lower_text:
            indicators.append(f"⚠️ Suspicious keyword detected: '{keyword}'")

    # URLs
    urls = re.findall(r'https?://\S+|www\.\S+', text)

    if urls:
        indicators.append(f"🔗 {len(urls)} URL(s) detected")

    # Email addresses
    emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        text
    )

    if emails:
        indicators.append(f"📧 {len(emails)} Email address(es) found")

    # IP address
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    if re.search(ip_pattern, text):
        indicators.append("🌐 IP address detected")

    # Too many capital letters
    uppercase_words = re.findall(r'\b[A-Z]{4,}\b', text)

    if len(uppercase_words) >= 3:
        indicators.append("🔠 Excessive uppercase words")

    # Exclamation marks
    if text.count("!") >= 3:
        indicators.append("❗ Excessive exclamation marks")

    return indicators