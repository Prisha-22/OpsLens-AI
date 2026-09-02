import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import pandas as pd
import streamlit as st
import plotly.express as px

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

from components.filters import show_filters

from components.charts import (
    revenue_chart,
    delivery_status_chart,
    weather_chart,
    traffic_chart
)


def show_dashboard():

    # =====================================================
    # DATABASE
    # =====================================================

    conn = get_connection()

    customers = pd.read_sql(
        "SELECT * FROM customers;",
        conn
    )

    orders = pd.read_sql(
        "SELECT * FROM orders;",
        conn
    )

    restaurants = pd.read_sql(
        "SELECT * FROM restaurants;",
        conn
    )

    riders = pd.read_sql(
        "SELECT * FROM riders;",
        conn
    )

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

    for factor_key in factor_names:

        factor_df = root_causes.get(
            factor_key
        )

        if factor_df is None:
            continue

        if factor_df.empty:
            continue

        impact = factor_df[
            "impact_vs_average"
        ].max()

        if impact > strongest_impact:

            strongest_impact = impact

            strongest_factor = factor_names[
                factor_key
            ]

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

    col1.metric(
        "🚨 Critical",
        critical
    )

    col2.metric(
        "🔴 High",
        high
    )

    col3.metric(
        "🟡 Medium",
        medium
    )

    # Show top 3 recommendations

    for recommendation in recommendations[:3]:

        priority = recommendation["priority"]

        if priority == "Critical":

            st.error(
                f"🚨 {recommendation['area']}"
            )

        elif priority == "High":

            st.warning(
                f"⚠️ {recommendation['area']}"
            )

        else:

            st.info(
                f"ℹ️ {recommendation['area']}"
            )

        st.markdown(
            f"**Finding:** {recommendation['finding']}"
        )

        st.markdown(
            f"**Action:** {recommendation['recommendation']}"
        )
    # =====================================================
    # FILTERS
    # =====================================================

    st.markdown("---")

    selected_city, selected_weather, selected_status = (
        show_filters(
            customers,
            orders
        )
    )

    filtered_orders = orders.copy()

    # City

    if selected_city != "All":

        customer_ids = customers[
            customers["city"] == selected_city
        ]["customer_id"]

        filtered_orders = filtered_orders[
            filtered_orders["customer_id"].isin(
                customer_ids
            )
        ]

    # Weather

    if selected_weather != "All":

        filtered_orders = filtered_orders[
            filtered_orders["weather"] == selected_weather
        ]

    # Status

    if selected_status != "All":

        filtered_orders = filtered_orders[
            filtered_orders["delivery_status"] == selected_status
        ]

    # =====================================================
    # EXISTING BUSINESS KPIs
    # =====================================================

    st.subheader("📈 Key Performance Indicators")

    conn = get_connection()

    real_order_count = pd.read_sql(
        "SELECT COUNT(*) AS count FROM real_delivery_orders;",
        conn
    ).iloc[0]["count"]

    conn.close()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Total Deliveries",
        f"{real_order_count:,}"
    )

    col2.metric(
        "⏱️ Avg Delivery Time",
        f"{health['overall_average_delivery_time']:.1f} min"
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
    # REVENUE
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Real Delivery Operations Overview")

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
            city
        FROM real_delivery_orders;
        """,
        conn
    )

    conn.close()

    # Delivery time distribution
    st.markdown("### ⏱️ Delivery Time Distribution")

    st.bar_chart(
        real_orders["actual_delivery_minutes"].value_counts().sort_index().head(40)
    )

    # Average delivery time by traffic level
    st.markdown("### 🚦 Average Delivery Time by Traffic")

    traffic_performance = (
        real_orders
        .groupby("traffic_level")["actual_delivery_minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(traffic_performance)

    # Average delivery time by weather
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

    # -----------------------------------------------------
    # Delivery Time by City
    # -----------------------------------------------------

    with breakdown_col1:

        st.markdown("### 🏙️ Average Delivery Time by City")

        city_performance = (
            real_orders
            .groupby("city")["actual_delivery_minutes"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(city_performance)


    # -----------------------------------------------------
    # Delivery Time by Distance
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Peak Hour Analysis
    # -----------------------------------------------------

    st.markdown("### ⏰ Peak Hour Impact")

    peak_performance = (
        real_orders
        .groupby("peak_hour")["actual_delivery_minutes"]
        .mean()
    )

    st.bar_chart(peak_performance)


    # -----------------------------------------------------
    # Multiple Delivery Analysis
    # -----------------------------------------------------

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