import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def show_dashboard_charts(history):

    if history.empty:
        st.info("No scan history available.")
        return

    # -----------------------------
    # Pie Chart
    # -----------------------------

    st.subheader("📊 Scan Distribution")

    prediction_col = None

    for col in history.columns:
        if col.lower() in ["prediction", "result"]:
            prediction_col = col
            break

    if prediction_col is None:
        st.warning("Prediction column not found.")
        return

    counts = history[prediction_col].value_counts()

    fig1, ax1 = plt.subplots(figsize=(5, 5))

    ax1.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax1.axis("equal")

    st.pyplot(fig1)

    # -----------------------------
    # Bar Chart
    # -----------------------------

    st.subheader("📈 Detection Counts")

    fig2, ax2 = plt.subplots(figsize=(6, 4))

    ax2.bar(counts.index, counts.values)

    ax2.set_xlabel("Prediction")
    ax2.set_ylabel("Count")

    st.pyplot(fig2)