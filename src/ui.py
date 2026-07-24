import streamlit as st


def show_prediction(prediction, confidence):

    if prediction == 1:

        st.error(
            f"""
🚨 Phishing Email Detected

Confidence Score: {confidence:.2f}%
"""
        )

    else:

        st.success(
            f"""
✅ Legitimate Email

Confidence Score: {confidence:.2f}%
"""
        )