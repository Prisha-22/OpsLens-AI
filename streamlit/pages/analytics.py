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


def show_analytics():

    # ==========================================
    # DATABASE
    # ==========================================

    conn = get_connection()

    orders = pd.read_sql(
        "SELECT * FROM real_delivery_orders;",
        conn
    )

    conn.close()

    # ==========================================
    # TITLE
    # ==========================================

    st.title("📈 Analytics")

    st.markdown(
        "### Detailed delivery operations performance analysis"
    )

    st.markdown("---")

    # ==========================================
    # FILTERS
    # ==========================================

    st.subheader("🔍 Analysis Filters")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        traffic_options = ["All"] + sorted(
            orders["traffic_level"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_traffic = st.selectbox(
            "Traffic Level",
            traffic_options
        )

    with col2:

        weather_options = ["All"] + sorted(
            orders["weather"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_weather = st.selectbox(
            "Weather",
            weather_options
        )

    with col3:

        city_options = ["All"] + sorted(
            orders["city"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_city = st.selectbox(
            "City",
            city_options
        )

    with col4:

        vehicle_options = ["All"] + sorted(
            orders["vehicle_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_vehicle = st.selectbox(
            "Vehicle Type",
            vehicle_options
        )

    # ==========================================
    # APPLY FILTERS
    # ==========================================

    filtered = orders.copy()

    if selected_traffic != "All":

        filtered = filtered[
            filtered["traffic_level"].astype(str)
            == selected_traffic
        ]

    if selected_weather != "All":

        filtered = filtered[
            filtered["weather"].astype(str)
            == selected_weather
        ]

    if selected_city != "All":

        filtered = filtered[
            filtered["city"].astype(str)
            == selected_city
        ]

    if selected_vehicle != "All":

        filtered = filtered[
            filtered["vehicle_type"].astype(str)
            == selected_vehicle
        ]

    # ==========================================
    # KPI
    # ==========================================

    st.markdown("---")

    st.subheader("📊 Performance Overview")

    total_orders = len(filtered)

    avg_delivery = filtered[
        "actual_delivery_minutes"
    ].mean()

    median_delivery = filtered[
        "actual_delivery_minutes"
    ].median()

    avg_distance = filtered[
        "distance_km"
    ].mean()

    avg_rating = filtered[
        "rider_rating"
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Deliveries",
        f"{total_orders:,}"
    )

    col2.metric(
        "⏱️ Avg Delivery",
        f"{avg_delivery:.1f} min"
        if total_orders > 0
        else "0.0 min"
    )

    col3.metric(
        "📊 Median Delivery",
        f"{median_delivery:.1f} min"
        if total_orders > 0
        else "0.0 min"
    )

    col4.metric(
        "📍 Avg Distance",
        f"{avg_distance:.1f} km"
        if total_orders > 0
        else "0.0 km"
    )

    # ==========================================
    # DELIVERY TIME ANALYSIS
    # ==========================================

    st.markdown("---")

    st.subheader("⏱️ Delivery Time Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            filtered,
            x="actual_delivery_minutes",
            nbins=30,
            title="Delivery Time Distribution",
            labels={
                "actual_delivery_minutes":
                    "Delivery Time (minutes)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        traffic_data = (
            filtered
            .groupby("traffic_level")[
                "actual_delivery_minutes"
            ]
            .mean()
            .reset_index()
            .sort_values(
                "actual_delivery_minutes",
                ascending=False
            )
        )

        fig = px.bar(
            traffic_data,
            x="traffic_level",
            y="actual_delivery_minutes",
            title="Average Delivery Time by Traffic",
            labels={
                "traffic_level": "Traffic Level",
                "actual_delivery_minutes":
                    "Average Delivery Time (min)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ==========================================
    # ENVIRONMENTAL ANALYSIS
    # ==========================================

    st.markdown("---")

    st.subheader("🌦️ Environmental Impact")

    col1, col2 = st.columns(2)

    with col1:

        weather_data = (
            filtered
            .groupby("weather")[
                "actual_delivery_minutes"
            ]
            .mean()
            .reset_index()
            .sort_values(
                "actual_delivery_minutes",
                ascending=False
            )
        )

        fig = px.bar(
            weather_data,
            x="weather",
            y="actual_delivery_minutes",
            title="Average Delivery Time by Weather",
            labels={
                "weather": "Weather",
                "actual_delivery_minutes":
                    "Average Delivery Time (min)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        distance_data = filtered.copy()

        distance_data["distance_category"] = pd.cut(
            distance_data["distance_km"],
            bins=[
                0,
                3,
                7,
                12,
                float("inf")
            ],
            labels=[
                "Short (0-3 km)",
                "Medium (3-7 km)",
                "Long (7-12 km)",
                "Very Long (12+ km)"
            ]
        )

        distance_analysis = (
            distance_data
            .groupby(
                "distance_category",
                observed=True
            )[
                "actual_delivery_minutes"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            distance_analysis,
            x="distance_category",
            y="actual_delivery_minutes",
            title="Delivery Time by Distance",
            labels={
                "distance_category": "Distance",
                "actual_delivery_minutes":
                    "Average Delivery Time (min)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ==========================================
    # OPERATIONAL PATTERNS
    # ==========================================

    st.markdown("---")

    st.subheader("🔎 Operational Patterns")

    col1, col2 = st.columns(2)

    with col1:

        peak_data = (
            filtered
            .groupby("peak_hour")[
                "actual_delivery_minutes"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            peak_data,
            x="peak_hour",
            y="actual_delivery_minutes",
            title="Peak vs Non-Peak Delivery Time",
            labels={
                "peak_hour": "Peak Hour",
                "actual_delivery_minutes":
                    "Average Delivery Time (min)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        weekend_data = (
            filtered
            .groupby("weekend")[
                "actual_delivery_minutes"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            weekend_data,
            x="weekend",
            y="actual_delivery_minutes",
            title="Weekend vs Weekday Delivery Time",
            labels={
                "weekend": "Weekend",
                "actual_delivery_minutes":
                    "Average Delivery Time (min)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ==========================================
    # VEHICLE ANALYSIS
    # ==========================================

    st.markdown("---")

    st.subheader("🚴 Vehicle & Rider Analysis")

    col1, col2 = st.columns(2)

    with col1:

        vehicle_data = (
            filtered
            .groupby("vehicle_type")[
                "actual_delivery_minutes"
            ]
            .mean()
            .reset_index()
            .sort_values(
                "actual_delivery_minutes",
                ascending=False
            )
        )

        fig = px.bar(
            vehicle_data,
            x="vehicle_type",
            y="actual_delivery_minutes",
            title="Average Delivery Time by Vehicle",
            labels={
                "vehicle_type": "Vehicle Type",
                "actual_delivery_minutes":
                    "Average Delivery Time (min)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        condition_data = (
            filtered
            .groupby("vehicle_condition")[
                "actual_delivery_minutes"
            ]
            .mean()
            .reset_index()
            .sort_values(
                "vehicle_condition"
            )
        )

        condition_data["vehicle_condition"] = (
            condition_data["vehicle_condition"]
            .astype(str)
        )

        fig = px.bar(
            condition_data,
            x="vehicle_condition",
            y="actual_delivery_minutes",
            title="Delivery Time by Vehicle Condition",
            labels={
                "vehicle_condition":
                    "Vehicle Condition",
                "actual_delivery_minutes":
                    "Average Delivery Time (min)"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ==========================================
    # ORDER BATCHING
    # ==========================================

    st.markdown("---")

    st.subheader("📦 Multiple Delivery Impact")

    multiple_data = (
        filtered
        .groupby("multiple_deliveries")[
            "actual_delivery_minutes"
        ]
        .agg(
            average_delivery_time="mean",
            order_count="count"
        )
        .reset_index()
    )

    multiple_data["multiple_deliveries"] = (
        multiple_data["multiple_deliveries"]
        .astype(str)
    )

    fig = px.bar(
        multiple_data,
        x="multiple_deliveries",
        y="average_delivery_time",
        title="Delivery Time by Number of Assigned Deliveries",
        labels={
            "multiple_deliveries":
                "Multiple Deliveries",
            "average_delivery_time":
                "Average Delivery Time (min)"
        }
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ==========================================
    # CITY ANALYSIS
    # ==========================================

    st.markdown("---")

    st.subheader("🏙️ City Operations")

    city_data = (
        filtered
        .groupby("city")[
            "actual_delivery_minutes"
        ]
        .agg(
            average_delivery_time="mean",
            order_count="count"
        )
        .reset_index()
        .sort_values(
            "average_delivery_time",
            ascending=False
        )
    )

    fig = px.bar(
        city_data,
        x="city",
        y="average_delivery_time",
        title="Average Delivery Time by City",
        labels={
            "city": "City",
            "average_delivery_time":
                "Average Delivery Time (min)"
        }
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ==========================================
    # RIDER RATING
    # ==========================================

    st.markdown("---")

    st.subheader("⭐ Rider Performance")

    rating_data = (
        filtered
        .groupby(
            pd.cut(
                filtered["rider_rating"],
                bins=[0, 3.5, 4.0, 4.5, 5.0],
                labels=[
                    "Below 3.5",
                    "3.5 - 4.0",
                    "4.0 - 4.5",
                    "4.5 - 5.0"
                ]
            )
        )["actual_delivery_minutes"]
        .mean()
        .reset_index()
    )

    rating_data.columns = [
        "rating_range",
        "average_delivery_time"
    ]

    fig = px.bar(
        rating_data,
        x="rating_range",
        y="average_delivery_time",
        title="Delivery Time by Rider Rating",
        labels={
            "rating_range": "Rider Rating",
            "average_delivery_time":
                "Average Delivery Time (min)"
        }
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ==========================================
    # FOOTER
    # ==========================================

    st.markdown("---")

    st.caption(
        "Analytics are generated from the real delivery "
        "operations dataset stored in the OpsLens AI database."
    )


if __name__ == "__main__":
    show_analytics()