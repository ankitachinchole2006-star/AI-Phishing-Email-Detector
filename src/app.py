import joblib
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from email import policy
from email.parser import BytesParser

import scan_history

from analyzer import detect_indicators
from config import APP_NAME, MODEL_PATH, VECTORIZER_PATH
from risk_engine import calculate_risk
from explanation_engine import generate_explanation
from attack_classifier import classify_attack
from severity_engine import calculate_severity
from pdf_report import generate_pdf_report
from header_analyzer import analyze_headers


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛡️",
    layout="wide"
)


# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    return model, vectorizer


model, vectorizer = load_model()


# =====================================================
# HEADER
# =====================================================

st.title("🛡️ AI-Powered Phishing Email Detector")

st.write("""
Detect phishing emails using Machine Learning and NLP.

Upload an **.eml file** or paste email content below.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("""
### 🛡 AI Detection

Machine Learning

NLP Analysis
""")

with col2:
    st.warning("""
### 🎯 Risk Engine

Threat Score

Severity Analysis
""")

with col3:
    st.success("""
### 📄 PDF Reports

Export Report

Security Summary
""")

with col4:
    st.error("""
### 📊 Analytics

Dashboard

Scan History
""")

st.divider()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("📊 Dashboard")

    history = scan_history.load_history()

    total = len(history)

    phishing = len(
        history[
            history["Prediction"] == "Phishing"
        ]
    )

    legitimate = len(
        history[
            history["Prediction"] == "Legitimate"
        ]
    )

    detection_rate = (
        round(phishing / total * 100, 2)
        if total > 0
        else 0
    )

    st.metric("📨 Total Scans", total)
    st.metric("🚨 Phishing", phishing)
    st.metric("✅ Legitimate", legitimate)
    st.metric("🎯 Detection Rate", f"{detection_rate}%")

    st.divider()

    st.success("Detection Engine Active")

    st.info("""
Model:
• Machine Learning

Capabilities:
• NLP Analysis
• Threat Detection
• Risk Scoring
• AI Explanation
• Attack Classification
• Security Reporting
""")


# =====================================================
# EMAIL INPUT
# =====================================================

st.subheader("📧 Email Scanner")

uploaded_file = st.file_uploader(
    "Upload Email (.eml)",
    type=["eml"]
)

email_text = ""

if uploaded_file:

    msg = BytesParser(
        policy=policy.default
    ).parse(uploaded_file)

    if msg.is_multipart():

        for part in msg.walk():

            if part.get_content_type() == "text/plain":

                email_text += part.get_content()

    else:

        email_text = msg.get_content()

    # =====================================
    # EMAIL HEADER ANALYSIS
    # =====================================

    st.subheader("📧 Email Header Analysis")

    header_info = analyze_headers(msg)

    col1, col2 = st.columns(2)

    with col1:

        st.write("**From**")
        st.success(header_info["From"])

        st.write("**Reply-To**")
        st.info(header_info["Reply-To"])

        st.write("**Return-Path**")
        st.info(header_info["Return-Path"])

        st.write("**Subject**")
        st.info(header_info["Subject"])

    with col2:

        st.write("**SPF**")
        st.metric("", header_info["SPF"])

        st.write("**DKIM**")
        st.metric("", header_info["DKIM"])

        st.write("**DMARC**")
        st.metric("", header_info["DMARC"])

        st.write("**Sender Domain**")
        st.warning(header_info["Domain"])


manual_text = st.text_area(
    "Paste Email Content",
    value=email_text,
    height=250
)

analyze = st.button("🔍 Analyze Email")


# =====================================================
# ANALYSIS ENGINE
# =====================================================

if analyze:

    if manual_text.strip() == "":

        st.warning("Please enter email content.")
        st.stop()

    email_vector = vectorizer.transform([manual_text])

    prediction = model.predict(email_vector)[0]

    probability = model.predict_proba(email_vector)[0]

    confidence = max(probability) * 100

    result = (
        "Phishing"
        if prediction == 1
        else "Legitimate"
    )

    scan_history.save_scan(
        result,
        confidence
    )


    st.divider()
        # =====================================================
    # THREAT INDICATORS
    # =====================================================

    st.subheader("🚨 Threat Indicators")

    indicators = detect_indicators(manual_text)

    if indicators:

        for item in indicators:
            st.warning(item)

    else:

        st.success("No suspicious indicators detected.")

    # =====================================================
    # RISK ENGINE
    # =====================================================

    risk_level, risk_score = calculate_risk(
        prediction,
        confidence,
        indicators
    )

    st.subheader("🛡️ Threat Assessment")

    col1, col2 = st.columns([1, 2])

    with col1:

        st.metric(
            "Risk Level",
            risk_level
        )

        st.metric(
            "Threat Score",
            f"{risk_score}/100"
        )

    with col2:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk_score,
                title={"text": "Security Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkred"},
                    "steps": [
                        {"range": [0, 25], "color": "#2ecc71"},
                        {"range": [25, 50], "color": "#f1c40f"},
                        {"range": [50, 75], "color": "#e67e22"},
                        {"range": [75, 100], "color": "#e74c3c"},
                    ],
                },
            )
        )

        fig.update_layout(height=320)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # AI EXPLANATION
    # =====================================================

    st.subheader("🧠 AI Security Explanation")

    explanations = generate_explanation(
        manual_text,
        indicators
    )

    for explanation in explanations:

        st.info(explanation)

    # =====================================================
    # ATTACK CLASSIFICATION
    # =====================================================

    st.subheader("🎯 Attack Classification")

    if prediction == 0:

       attack_type = "No Attack Detected"
       attack_reason = "This email does not exhibit common phishing characteristics."

    else:

       attack_type, attack_reason = classify_attack(
         manual_text
    )

    st.success(
        f"Attack Type: {attack_type}"
    )

    st.write(
        attack_reason
    )

    # =====================================================
    # SEVERITY
    # =====================================================

    severity, severity_reason = calculate_severity(
        risk_score,
        attack_type
    )

    st.subheader("🚨 Severity Assessment")

    st.metric(
        "Severity Level",
        severity
    )

    for reason in severity_reason:

        st.warning(reason)

    # =====================================================
    # PDF REPORT
    # =====================================================

    st.subheader("📄 Security Report")

    pdf = generate_pdf_report(
        result,
        confidence,
        risk_level,
        risk_score,
        attack_type,
        severity,
        indicators
    )

    st.download_button(
        label="📄 Download PDF Security Report",
        data=pdf,
        file_name="Security_Report.pdf",
        mime="application/pdf"
    )

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    st.subheader("🔐 Recommendation")

    if prediction == 1:

        st.error("""
### Possible Phishing Email

Actions:

• Do NOT click links

• Do NOT download attachments

• Do NOT share passwords

• Verify sender identity

• Report suspicious emails
""")

    else:

        st.success("""
### Email Appears Legitimate

Continue following safe email practices.
""")
        # =====================================================
# ANALYTICS DASHBOARD
# =====================================================

st.divider()

history = scan_history.load_history()

if not history.empty:

    st.subheader("📊 Security Analytics Dashboard")

    col1, col2 = st.columns(2)

    with col1:

        count = (
            history["Prediction"]
            .value_counts()
            .reset_index()
        )

        count.columns = [
            "Prediction",
            "Count"
        ]

        fig1 = px.pie(
            count,
            names="Prediction",
            values="Count",
            title="Email Classification Distribution",
            hole=0.45
        )

        fig1.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        fig2 = px.line(
            history,
            y="Confidence",
            title="Confidence Trend",
            markers=True
        )

        fig2.update_layout(
            xaxis_title="Scan Number",
            yaxis_title="Confidence (%)"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# =====================================================
# SCAN HISTORY
# =====================================================

st.divider()

st.subheader("📜 Scan History")

history = scan_history.load_history()

if history.empty:

    st.info("No scan history available.")

else:

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

    csv = history.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Scan History (CSV)",
        data=csv,
        file_name="scan_history.csv",
        mime="text/csv"
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🛡️ AI-Powered Phishing Email Detector | Built with Python, Streamlit, Machine Learning, NLP, Plotly & ReportLab"
)