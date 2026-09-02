import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import streamlit as st
import plotly.express as px

from python.analytics.real_root_cause_analysis import (
    analyze_real_root_causes
)


def show_root_cause():

    st.title("🔍 Root Cause Analysis")
    st.markdown(
        "Identify operational factors associated with longer delivery times "
        "using the real delivery dataset."
    )
    st.markdown("---")

    # =====================================================
    # LOAD REAL ROOT CAUSE ANALYSIS
    # =====================================================

    with st.spinner("🔎 Analyzing real delivery operations..."):
        results = analyze_real_root_causes()

    overall_average = results["overall_average"]

    # =====================================================
    # OVERALL PERFORMANCE
    # =====================================================

    st.subheader("📊 Overall Delivery Performance")

    st.metric(
        "Average Delivery Time",
        f"{overall_average:.2f} minutes"
    )

    st.caption(
        "Baseline used to measure how strongly each operational factor "
        "is associated with longer or shorter delivery times."
    )

    st.markdown("---")

    # =====================================================
    # HELPER FUNCTION
    # =====================================================

    def show_factor_chart(
        data,
        title,
        x_title
    ):

        fig = px.bar(
            data,
            x="factor",
            y="average_delivery_time",
            title=title,
            labels={
                "factor": x_title,
                "average_delivery_time": "Delivery Time (minutes)"
            },
            hover_data=[
                "order_count",
                "impact_vs_average"
            ]
        )

        fig.add_hline(
            y=overall_average,
            line_dash="dash",
            annotation_text="Overall Average"
        )

        fig.update_layout(
            xaxis_title=x_title,
            yaxis_title="Delivery Time (minutes)"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # =====================================================
    # TRAFFIC
    # =====================================================

    st.subheader("🚦 Traffic Impact")

    traffic = results["traffic"]

    show_factor_chart(
        traffic,
        "Average Delivery Time by Traffic Level",
        "Traffic Level"
    )

    # =====================================================
    # WEATHER
    # =====================================================

    st.subheader("🌦️ Weather Impact")

    weather = results["weather"]

    show_factor_chart(
        weather,
        "Average Delivery Time by Weather",
        "Weather Condition"
    )

    # =====================================================
    # PEAK HOUR
    # =====================================================

    st.subheader("⏰ Peak Hour Impact")

    peak = results["peak"]

    show_factor_chart(
        peak,
        "Average Delivery Time by Peak Hour",
        "Peak Hour"
    )

    # =====================================================
    # DISTANCE
    # =====================================================

    st.subheader("📍 Distance Impact")

    distance = results["distance"]

    show_factor_chart(
        distance,
        "Average Delivery Time by Distance",
        "Distance Category"
    )

    # =====================================================
    # VEHICLE TYPE
    # =====================================================

    st.subheader("🏍️ Vehicle Type Impact")

    vehicle_type = results["vehicle_type"]

    show_factor_chart(
        vehicle_type,
        "Average Delivery Time by Vehicle Type",
        "Vehicle Type"
    )

    # =====================================================
    # VEHICLE CONDITION
    # =====================================================

    st.subheader("🔧 Vehicle Condition Impact")

    vehicle_condition = results["vehicle_condition"]

    show_factor_chart(
        vehicle_condition,
        "Average Delivery Time by Vehicle Condition",
        "Vehicle Condition"
    )

    # =====================================================
    # MULTIPLE DELIVERIES
    # =====================================================

    st.subheader("📦 Multiple Delivery Impact")

    multiple_deliveries = results["multiple_deliveries"]

    show_factor_chart(
        multiple_deliveries,
        "Average Delivery Time by Number of Deliveries",
        "Multiple Deliveries"
    )

    # =====================================================
    # CITY
    # =====================================================

    st.subheader("🏙️ City Impact")

    city = results["city"]

    show_factor_chart(
        city,
        "Average Delivery Time by City",
        "City Type"
    )

    # =====================================================
    # STRONGEST ROOT CAUSE
    # =====================================================

    st.markdown("---")

    st.subheader("🧠 Strongest Operational Factor")

    factors = {
        "Traffic": traffic,
        "Weather": weather,
        "Peak Hour": peak,
        "Distance": distance,
        "Vehicle Type": vehicle_type,
        "Vehicle Condition": vehicle_condition,
        "Multiple Deliveries": multiple_deliveries,
        "City": city
    }

    strongest_factor = None
    strongest_category = None
    strongest_value = float("-inf")

    for category, data in factors.items():

        if data.empty:
            continue

        row = data.loc[
            data["impact_vs_average"].idxmax()
        ]

        impact = row["impact_vs_average"]

        if impact > strongest_value:
            strongest_value = impact
            strongest_factor = row["factor"]
            strongest_category = category

    if strongest_factor is not None:

        st.warning(
            f"🚨 **Strongest operational factor:** "
            f"{strongest_category} → **{strongest_factor}** "
            f"is associated with an average delivery time "
            f"**{strongest_value:.2f} minutes above the overall average**."
        )

        st.metric(
            "Impact Above Average",
            f"+{strongest_value:.2f} minutes"
        )

    # =====================================================
    # TOP CONTRIBUTORS TABLE
    # =====================================================

    st.markdown("---")

    st.subheader("📋 Highest-Impact Operational Factors")

    top_factors = []

    for category, data in factors.items():

        if data.empty:
            continue

        row = data.loc[
            data["impact_vs_average"].idxmax()
        ]

        top_factors.append({
            "Category": category,
            "Factor": row["factor"],
            "Avg Delivery Time": round(
                row["average_delivery_time"], 2
            ),
            "Impact vs Average": round(
                row["impact_vs_average"], 2
            ),
            "Orders": int(
                row["order_count"]
            )
        })

    top_factors = sorted(
        top_factors,
        key=lambda x: x["Impact vs Average"],
        reverse=True
    )

    st.dataframe(
        top_factors,
        width="stretch",
        hide_index=True
    )

    # =====================================================
    # INTERPRETATION
    # =====================================================

    st.markdown("---")

    st.subheader("💡 Interpretation")

    st.info(
        "These results identify operational factors associated with "
        "delivery-time variation. A higher impact value means that the "
        "factor is associated with longer delivery times compared with "
        "the overall dataset average. These relationships should be "
        "investigated further before being treated as confirmed causal "
        "relationships."
    )

    st.caption(
        "OpsLens AI Root Cause Analysis uses real delivery data to "
        "identify operational contributors to delivery-time variation."
    )


if __name__ == "__main__":
    show_root_cause()