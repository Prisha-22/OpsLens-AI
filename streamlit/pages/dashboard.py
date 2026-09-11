import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import pandas as pd
import streamlit as st

from python.database import get_connection

from python.insights.real_operational_health import (
    calculate_operational_health
)

from python.analytics.real_root_cause_analysis import (
    analyze_real_root_causes
)

from python.ml.real_anomaly_detection import (
    detect_real_anomalies
)

from python.insights.real_recommendation_engine import (
    generate_real_recommendations
)


def show_dashboard():

    # =====================================================
    # LOAD REAL DELIVERY DATA
    # =====================================================

    conn = get_connection()

    real_orders = pd.read_sql(
        """
        SELECT
            actual_delivery_minutes,
            distance_km,
            weather,
            traffic_level,
            peak_hour,
            multiple_deliveries,
            city,
            vehicle_condition
        FROM real_delivery_orders;
        """,
        conn
    )

    real_order_count = len(real_orders)

    conn.close()

    # =====================================================
    # TITLE
    # =====================================================

    st.title("📊 Executive Dashboard")

    st.markdown(
        "### Delivery Operations Intelligence"
    )

    st.markdown("---")

    # =====================================================
    # REAL OPSLENS ANALYTICS
    # =====================================================

    health = calculate_operational_health()

    root_causes = analyze_real_root_causes()

    anomalies = detect_real_anomalies()

    recommendations = generate_real_recommendations()

    # =====================================================
    # OPERATIONAL HEALTH
    # =====================================================

    st.subheader("🧠 Operational Health")

    average_delivery = health[
        "overall_average_delivery_time"
    ]

    health_score = health[
        "health_score"
    ]

    health_status = health[
        "status"
    ]

    anomaly_count = len(anomalies)

    # -----------------------------------------------------
    # Find strongest root cause
    # -----------------------------------------------------

    factor_names = {
        "traffic": "Traffic",
        "weather": "Weather",
        "peak": "Peak Hour",
        "weekend": "Weekend",
        "order_type": "Order Type",
        "vehicle_type": "Vehicle Type",
        "vehicle_condition": "Vehicle Condition",
        "multiple_deliveries": "Multiple Deliveries",
        "city": "City",
        "distance": "Delivery Distance"
    }

    strongest_factor = None
    strongest_impact = float("-inf")

    for factor_key, factor_name in factor_names.items():

        factor_df = root_causes.get(factor_key)

        if factor_df is None:
            continue

        if factor_df.empty:
            continue

        impact = factor_df["impact_vs_average"].max()

        if impact > strongest_impact:
            strongest_impact = impact
            strongest_factor = factor_name

    if strongest_factor is None:
        strongest_factor = "N/A"
        strongest_impact = 0

    # =====================================================
    # HEALTH METRICS
    # =====================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "⏱️ Avg Delivery Time",
        f"{average_delivery:.1f} min"
    )

    col2.metric(
        "🏥 Health Score",
        f"{health_score}/100"
    )

    col3.metric(
        "🚨 Anomalies",
        f"{anomaly_count:,}"
    )

    col4.metric(
        "🔍 Strongest Factor",
        strongest_factor
    )

    col5.metric(
        "⚠️ Operational Status",
        health_status
    )

    # =====================================================
    # STATUS MESSAGE
    # =====================================================

    if health_status == "Critical":

        st.error(
            "🚨 Operational performance requires immediate attention."
        )

    elif health_status == "High Risk":

        st.warning(
            "⚠️ Operations are currently at high risk. "
            "Several operational factors require attention."
        )

    elif health_status == "Moderate Risk":

        st.warning(
            "🟡 Operations are moderately healthy. "
            "Some indicators require monitoring."
        )

    else:

        st.success(
            "🟢 Operational performance is currently healthy."
        )

    # =====================================================
    # ROOT CAUSE
    # =====================================================

    st.markdown("---")

    st.subheader("🔍 Root Cause Analysis")

    root_col1, root_col2 = st.columns(2)

    with root_col1:

        st.metric(
            "Strongest Contributing Factor",
            strongest_factor
        )

    with root_col2:

        st.metric(
            "Impact on Delivery Time",
            f"{strongest_impact:+.2f} min"
        )

    st.info(
        f"🧠 Analysis indicates that **{strongest_factor}** "
        f"is currently the strongest contributing factor, "
        f"with an estimated impact of "
        f"**{strongest_impact:+.2f} minutes** on delivery time."
    )

    # =====================================================
    # OPERATIONAL INDICATORS
    # =====================================================

    st.subheader("📊 Operational Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "🚦 Jam Traffic",
        f"{health['jam_rate']:.1f}%"
    )

    col2.metric(
        "⏰ Peak Hour",
        f"{health['peak_rate']:.1f}%"
    )

    col3.metric(
        "📦 Multiple Deliveries",
        f"{health['multiple_delivery_rate']:.1f}%"
    )

    col4.metric(
        "🏍️ Poor Vehicle",
        f"{health['poor_vehicle_rate']:.1f}%"
    )

    col5.metric(
        "📍 Very Long Distance",
        f"{health['very_long_distance_rate']:.1f}%"
    )

    # =====================================================
    # AI RECOMMENDATIONS
    # =====================================================

    st.markdown("---")

    st.subheader("💡 AI Recommendations")

    critical = sum(
        1
        for r in recommendations
        if r["priority"] == "Critical"
    )

    high = sum(
        1
        for r in recommendations
        if r["priority"] == "High"
    )

    medium = sum(
        1
        for r in recommendations
        if r["priority"] == "Medium"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("🚨 Critical", critical)
    col2.metric("🔴 High", high)
    col3.metric("🟡 Medium", medium)

    for recommendation in recommendations[:3]:

        priority = recommendation["priority"]

        if priority == "Critical":
            st.error(f"🚨 {recommendation['area']}")

        elif priority == "High":
            st.warning(f"⚠️ {recommendation['area']}")

        else:
            st.info(f"ℹ️ {recommendation['area']}")

        st.markdown(
            f"**Finding:** {recommendation['finding']}"
        )

        st.markdown(
            f"**Action:** {recommendation['recommendation']}"
        )

    # =====================================================
    # KEY PERFORMANCE INDICATORS
    # =====================================================

    st.markdown("---")

    st.subheader("📈 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Total Deliveries",
        f"{real_order_count:,}"
    )

    col2.metric(
        "⏱️ Avg Delivery Time",
        f"{average_delivery:.1f} min"
    )

    col3.metric(
        "🚦 Jam Traffic",
        f"{health['jam_rate']:.1f}%"
    )

    col4.metric(
        "📦 Multiple Deliveries",
        f"{health['multiple_delivery_rate']:.1f}%"
    )

    # =====================================================
    # REAL DELIVERY OPERATIONS OVERVIEW
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Real Delivery Operations Overview")

    st.markdown("### ⏱️ Delivery Time Distribution")

    delivery_distribution = (
        real_orders["actual_delivery_minutes"]
        .value_counts()
        .sort_index()
        .head(40)
    )

    st.bar_chart(delivery_distribution)

    st.markdown("### 🚦 Average Delivery Time by Traffic")

    traffic_performance = (
        real_orders
        .groupby("traffic_level")["actual_delivery_minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(traffic_performance)

    st.markdown("### 🌦️ Average Delivery Time by Weather")

    weather_performance = (
        real_orders
        .groupby("weather")["actual_delivery_minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(weather_performance)

    # =====================================================
    # OPERATIONAL BREAKDOWN
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Operational Breakdown")

    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:

        st.markdown("### 🏙️ Average Delivery Time by City")

        city_performance = (
            real_orders
            .groupby("city")["actual_delivery_minutes"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(city_performance)

    with breakdown_col2:

        st.markdown("### 📍 Average Delivery Time by Distance")

        real_orders["distance_category"] = pd.cut(
            real_orders["distance_km"],
            bins=[-1, 3, 7, 12, float("inf")],
            labels=[
                "Short (0-3 km)",
                "Medium (3-7 km)",
                "Long (7-12 km)",
                "Very Long (12+ km)"
            ]
        )

        distance_performance = (
            real_orders
            .groupby(
                "distance_category",
                observed=True
            )["actual_delivery_minutes"]
            .mean()
        )

        st.bar_chart(distance_performance)

    st.markdown("### ⏰ Peak Hour Impact")

    peak_performance = (
        real_orders
        .groupby("peak_hour")["actual_delivery_minutes"]
        .mean()
    )

    st.bar_chart(peak_performance)

    st.markdown("### 📦 Multiple Delivery Impact")

    batch_performance = (
        real_orders
        .groupby("multiple_deliveries")["actual_delivery_minutes"]
        .mean()
        .sort_index()
    )

    st.bar_chart(batch_performance)


if __name__ == "__main__":
    show_dashboard()