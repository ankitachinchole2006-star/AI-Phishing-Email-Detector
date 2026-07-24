from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def generate_pdf_report(
    result,
    confidence,
    risk_level,
    risk_score,
    attack_type,
    severity,
    indicators
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>AI-Powered Phishing Email Detector</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Prediction:</b> {result}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Confidence:</b> {confidence:.2f}%", styles["BodyText"]))
    story.append(Paragraph(f"<b>Risk Level:</b> {risk_level}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Threat Score:</b> {risk_score}/100", styles["BodyText"]))
    story.append(Paragraph(f"<b>Attack Type:</b> {attack_type}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Severity:</b> {severity}", styles["BodyText"]))

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("<b>Threat Indicators</b>", styles["Heading2"])
    )

    for item in indicators:
        story.append(
            Paragraph(f"• {item}", styles["BodyText"])
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("<b>Recommendations</b>", styles["Heading2"])
    )

    recommendations = [
        "Do not click suspicious links.",
        "Do not download unexpected attachments.",
        "Never share passwords or OTPs.",
        "Verify the sender through another channel.",
        "Report suspicious emails to your security team.",
    ]

    for rec in recommendations:
        story.append(
            Paragraph(f"• {rec}", styles["BodyText"])
        )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf