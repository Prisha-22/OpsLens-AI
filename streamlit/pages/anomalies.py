import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px

from python.ml.real_anomaly_detection import detect_real_anomalies


def show_anomalies():

    st.title("🚨 Anomaly Detection")
    st.markdown(
        "Detect unusual delivery operations and identify potential "
        "operational risks using machine learning."
    )
    st.markdown("---")

    # =====================================================
    # REAL ANOMALY DETECTION
    # =====================================================

    with st.spinner("🔍 Detecting unusual operational patterns..."):
        anomalies = detect_real_anomalies()

    # =====================================================
    # LOAD REAL DATASET
    # =====================================================

    total_orders = 45584

    anomaly_count = len(anomalies)

    anomaly_percentage = (
        anomaly_count / total_orders
    ) * 100

    # =====================================================
    # KPI CARDS
    # =====================================================

    st.subheader("📊 Anomaly Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Deliveries",
        f"{total_orders:,}"
    )

    col2.metric(
        "Detected Anomalies",
        f"{anomaly_count:,}"
    )

    col3.metric(
        "Anomaly Rate",
        f"{anomaly_percentage:.1f}%"
    )

    st.markdown("---")

    # =====================================================
    # EXPLANATION
    # =====================================================

    st.info(
        "OpsLens AI uses Isolation Forest to identify unusual "
        "combinations of operational factors such as delivery time, "
        "distance, traffic, weather, vehicle condition and multiple "
        "deliveries."
    )

    # =====================================================
    # ANOMALOUS ORDERS
    # =====================================================

    st.subheader("🚨 Anomalous Deliveries")

    display_columns = [
        "order_id",
        "distance_km",
        "actual_delivery_minutes",
        "weather",
        "traffic_level",
        "peak_hour",
        "multiple_deliveries",
        "vehicle_type",
        "vehicle_condition",
        "city"
    ]

    available_columns = [
        col for col in display_columns
        if col in anomalies.columns
    ]

    st.dataframe(
        anomalies[available_columns],
        width="stretch",
        hide_index=True
    )

    # =====================================================
    # HIGHEST DELIVERY TIME ANOMALIES
    # =====================================================

    st.markdown("---")

    st.subheader("⏱️ Highest Delivery-Time Anomalies")

    delivery_anomalies = (
        anomalies
        .sort_values(
            by="actual_delivery_minutes",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        delivery_anomalies[
            [
                col for col in [
                    "order_id",
                    "actual_delivery_minutes",
                    "distance_km",
                    "traffic_level",
                    "weather",
                    "multiple_deliveries"
                ]
                if col in anomalies.columns
            ]
        ],
        width="stretch",
        hide_index=True
    )

    # =====================================================
    # ANOMALY PATTERNS
    # =====================================================

    st.markdown("---")

    st.subheader("🔍 Anomaly Patterns")

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # TRAFFIC
    # -----------------------------------------------------

    with col1:

        st.markdown("### 🚦 Traffic")

        traffic_counts = (
            anomalies["traffic_level"]
            .value_counts()
            .reset_index()
        )

        traffic_counts.columns = [
            "Traffic Level",
            "Anomalies"
        ]

        fig_traffic = px.bar(
            traffic_counts,
            x="Traffic Level",
            y="Anomalies",
            title="Anomalies by Traffic Level"
        )

        st.plotly_chart(
            fig_traffic,
            width="stretch"
        )

    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------

    with col2:

        st.markdown("### 🌦️ Weather")

        weather_counts = (
            anomalies["weather"]
            .value_counts()
            .reset_index()
        )

        weather_counts.columns = [
            "Weather",
            "Anomalies"
        ]

        fig_weather = px.bar(
            weather_counts,
            x="Weather",
            y="Anomalies",
            title="Anomalies by Weather"
        )

        st.plotly_chart(
            fig_weather,
            width="stretch"
        )

    # =====================================================
    # MULTIPLE DELIVERY PATTERN
    # =====================================================

    st.markdown("---")

    st.subheader("📦 Multiple Delivery Anomalies")

    multiple_counts = (
        anomalies["multiple_deliveries"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    multiple_counts.columns = [
        "Multiple Deliveries",
        "Anomalies"
    ]

    fig_multiple = px.bar(
        multiple_counts,
        x="Multiple Deliveries",
        y="Anomalies",
        title="Anomalies by Multiple Delivery Count"
    )

    st.plotly_chart(
        fig_multiple,
        width="stretch"
    )

    # =====================================================
    # CITY PATTERN
    # =====================================================

    st.subheader("🏙️ City Anomaly Distribution")

    city_counts = (
        anomalies["city"]
        .value_counts()
        .reset_index()
    )

    city_counts.columns = [
        "City",
        "Anomalies"
    ]

    fig_city = px.bar(
        city_counts,
        x="City",
        y="Anomalies",
        title="Anomalies by City Type"
    )

    st.plotly_chart(
        fig_city,
        width="stretch"
    )

    # =====================================================
    # VEHICLE CONDITION
    # =====================================================

    st.subheader("🔧 Vehicle Condition Anomalies")

    vehicle_counts = (
        anomalies["vehicle_condition"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    vehicle_counts.columns = [
        "Vehicle Condition",
        "Anomalies"
    ]

    st.dataframe(
        vehicle_counts,
        width="stretch",
        hide_index=True
    )

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("---")

    st.caption(
        "Anomalies are detected automatically using Isolation Forest "
        "and should be investigated as potential operational risks."
    )


if __name__ == "__main__":
    show_anomalies()