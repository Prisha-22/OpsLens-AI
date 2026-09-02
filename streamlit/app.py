import streamlit as st

from components.sidebar import show_sidebar
from pages.dashboard import show_dashboard
from pages.prediction import show_prediction
from pages.ai_insights import show_ai_insights
from pages.anomalies import show_anomalies
from pages.forecast import show_forecast
from pages.root_cause import show_root_cause
from pages.analytics import show_analytics
from pages.recommendations import show_recommendations

st.set_page_config(
    page_title="OpsLens AI",
    page_icon="📊",
    layout="wide"
)

page = show_sidebar()

if page == "Dashboard":
    show_dashboard()

elif page == "Analytics":
    show_analytics()

elif page == "Prediction":
    show_prediction()

elif page == "AI Insights":
    show_ai_insights()

elif page == "Anomaly Detection":
    show_anomalies()

elif page == "Forecasting":
    show_forecast()

elif page == "Root Cause Analysis":
    show_root_cause()

elif page == "Operational Recommendations":
    show_recommendations()