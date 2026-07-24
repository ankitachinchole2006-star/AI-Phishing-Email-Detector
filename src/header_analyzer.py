import re


def analyze_headers(msg):

    result = {}

    result["From"] = msg.get("From", "Unknown")
    result["To"] = msg.get("To", "Unknown")
    result["Subject"] = msg.get("Subject", "Unknown")
    result["Reply-To"] = msg.get("Reply-To", "Not Present")
    result["Return-Path"] = msg.get("Return-Path", "Not Present")

    authentication = (
        str(msg.get("Authentication-Results", "")).lower()
    )

    if "spf=pass" in authentication:
        result["SPF"] = "PASS ✅"
    else:
        result["SPF"] = "FAIL ❌"

    if "dkim=pass" in authentication:
        result["DKIM"] = "PASS ✅"
    else:
        result["DKIM"] = "FAIL ❌"

    if "dmarc=pass" in authentication:
        result["DMARC"] = "PASS ✅"
    else:
        result["DMARC"] = "FAIL ❌"

    sender = result["From"]

    match = re.search(r'@([\w\.-]+)', sender)

    if match:
        result["Domain"] = match.group(1)
    else:
        result["Domain"] = "Unknown"

    return result