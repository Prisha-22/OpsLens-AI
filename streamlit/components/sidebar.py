import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.title("📊 OpsLens AI")

        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Analytics",
                "Prediction",
                "AI Insights",
                "Anomaly Detection",
                "Forecasting",
                "Root Cause Analysis",
                "Operational Recommendations"
            ],
            key="navigation"
        )

    return page