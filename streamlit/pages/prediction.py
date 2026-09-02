import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import pandas as pd
import streamlit as st

from python.ml.real_prediction import predict_real_delivery_time


def show_prediction():

    st.title("🤖 Delivery Time Prediction")

    st.markdown(
        "### Predict expected delivery time for a new delivery order"
    )

    st.markdown("---")

    # ==========================================
    # INPUTS
    # ==========================================

    st.subheader("📦 Enter Delivery Details")

    col1, col2 = st.columns(2)

    with col1:

        distance = st.number_input(
            "Distance (km)",
            min_value=0.1,
            value=5.0,
            step=0.5
        )

        rider_age = st.number_input(
            "Rider Age",
            min_value=18,
            max_value=60,
            value=28,
            step=1
        )

        rider_rating = st.number_input(
            "Rider Rating",
            min_value=1.0,
            max_value=5.0,
            value=4.5,
            step=0.1
        )

        weather = st.selectbox(
            "Weather",
            [
                "Sunny",
                "Cloudy",
                "Fog",
                "Sandstorms",
                "Stormy",
                "Windy"
            ]
        )

        traffic = st.selectbox(
            "Traffic Level",
            [
                "Low",
                "Medium",
                "High",
                "Jam"
            ]
        )

        vehicle_condition = st.selectbox(
            "Vehicle Condition",
            [0, 1, 2, 3],
            index=1
        )

        vehicle_type = st.selectbox(
            "Vehicle Type",
            [
                "motorcycle",
                "scooter",
                "electric_scooter",
                "bicycle"
            ]
        )

    with col2:

        order_type = st.selectbox(
            "Order Type",
            [
                "Snack",
                "Meal",
                "Drinks",
                "Buffet"
            ]
        )

        multiple_deliveries = st.selectbox(
            "Multiple Deliveries",
            [0, 1, 2, 3],
            index=0
        )

        festival = st.selectbox(
            "Festival",
            [
                "No",
                "Yes"
            ]
        )

        city = st.selectbox(
            "City",
            [
                "Urban",
                "Metropolitian",
                "Semi-Urban"
            ]
        )

        pickup_hour = st.slider(
            "Pickup Hour",
            min_value=0,
            max_value=23,
            value=18
        )

        peak_hour = st.selectbox(
            "Peak Hour",
            [
                "No",
                "Yes"
            ]
        )

        weekend = st.selectbox(
            "Weekend",
            [
                "No",
                "Yes"
            ]
        )

    st.markdown("---")

    # ==========================================
    # PREDICTION
    # ==========================================

    if st.button(
        "🚚 Predict Delivery Time",
        width="stretch"
    ):

        with st.spinner("🤖 Predicting delivery time..."):

            prediction = predict_real_delivery_time(
                distance=distance,
                rider_age=rider_age,
                rider_rating=rider_rating,
                weather=weather,
                traffic=traffic,
                vehicle_condition=vehicle_condition,
                order_type=order_type,
                vehicle_type=vehicle_type,
                multiple_deliveries=multiple_deliveries,
                festival=festival,
                city=city,
                pickup_hour=pickup_hour,
                peak_hour=peak_hour,
                weekend=weekend
            )

        # ======================================
        # RISK LEVEL
        # ======================================

        if prediction >= 40:

            risk = "High Risk"
            risk_message = (
                "Delivery is expected to take significantly "
                "longer than normal."
            )

        elif prediction >= 30:

            risk = "Medium Risk"
            risk_message = (
                "Delivery time may require operational monitoring."
            )

        else:

            risk = "Low Risk"
            risk_message = (
                "Delivery is expected to remain within a "
                "reasonable time range."
            )

        # ======================================
        # RESULT
        # ======================================

        st.markdown("---")

        st.subheader("🎯 Prediction Result")

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            st.metric(
                "Predicted Delivery Time",
                f"{prediction:.1f} minutes"
            )

        with result_col2:

            if risk == "High Risk":

                st.error(
                    f"🚨 {risk}"
                )

            elif risk == "Medium Risk":

                st.warning(
                    f"⚠️ {risk}"
                )

            else:

                st.success(
                    f"🟢 {risk}"
                )

        st.info(risk_message)

        # ======================================
        # OPERATIONAL FACTORS
        # ======================================

        st.markdown("---")

        st.subheader("🔍 Operational Factors")

        factors = []

        if traffic == "Jam":

            factors.append(
                "🚦 Jam traffic is likely to significantly increase delivery time."
            )

        elif traffic == "High":

            factors.append(
                "🚦 High traffic may increase delivery time."
            )

        elif traffic == "Medium":

            factors.append(
                "🚦 Medium traffic may moderately affect delivery time."
            )

        if weather in ["Fog", "Stormy", "Sandstorms"]:

            factors.append(
                f"🌦️ {weather} weather conditions may slow delivery operations."
            )

        if peak_hour == "Yes":

            factors.append(
                "⏰ Peak-hour operations may increase delivery delays."
            )

        if distance >= 12:

            factors.append(
                "📍 Very long delivery distance is likely to increase delivery time."
            )

        elif distance >= 7:

            factors.append(
                "📍 Long delivery distance may increase delivery time."
            )

        if multiple_deliveries >= 2:

            factors.append(
                "📦 Multiple-order delivery assignments may significantly increase delivery time."
            )

        if vehicle_condition == 0:

            factors.append(
                "🛵 Poor vehicle condition may negatively affect delivery performance."
            )

        if city == "Semi-Urban":

            factors.append(
                "🏙️ Semi-urban operations show higher delivery times in the historical dataset."
            )

        if not factors:

            factors.append(
                "✅ No major operational risk factors detected."
            )

        for factor in factors:

            st.write(factor)

        # ======================================
        # RECOMMENDATION
        # ======================================

        st.markdown("---")

        st.subheader("💡 Operational Recommendation")

        if risk == "High Risk":

            st.error(
                "Consider assigning additional rider capacity "
                "or prioritizing this delivery for monitoring."
            )

        elif risk == "Medium Risk":

            st.warning(
                "Monitor this delivery and consider rider availability "
                "in the delivery zone."
            )

        else:

            st.success(
                "No immediate operational intervention is required."
            )

        # ======================================
        # INPUT SUMMARY
        # ======================================

        st.markdown("---")

        st.subheader("📋 Delivery Summary")

        summary = pd.DataFrame({
            "Parameter": [
                "Distance",
                "Rider Age",
                "Rider Rating",
                "Weather",
                "Traffic",
                "Vehicle Condition",
                "Vehicle Type",
                "Order Type",
                "Multiple Deliveries",
                "Festival",
                "City",
                "Pickup Hour",
                "Peak Hour",
                "Weekend"
            ],
            "Value": [
                f"{distance:.1f} km",
                f"{rider_age} years",
                f"{rider_rating:.1f}",
                weather,
                traffic,
                vehicle_condition,
                vehicle_type,
                order_type,
                multiple_deliveries,
                festival,
                city,
                f"{pickup_hour}:00",
                peak_hour,
                weekend
            ]
        })

        st.dataframe(
            summary,
            width="stretch",
            hide_index=True
        )


if __name__ == "__main__":
    show_prediction()