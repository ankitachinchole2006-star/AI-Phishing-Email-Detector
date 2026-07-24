def generate_explanation(email_text, indicators):

    explanations = []

    if indicators:
        explanations.append(
            "This email contains multiple phishing indicators such as suspicious keywords."
        )

    if "password" in email_text.lower():
        explanations.append(
            "The email requests sensitive information, which is a common credential theft technique."
        )

    if "click" in email_text.lower():
        explanations.append(
            "The email uses urgency and click-based actions to manipulate the user."
        )

    if not explanations:
        explanations.append(
            "No major security risks detected."
        )

    return explanations