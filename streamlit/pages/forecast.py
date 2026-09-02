import os
import sys

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import streamlit as st
import plotly.graph_objects as go

from python.ml.real_forecast import generate_real_forecast


def show_forecast():

    st.title("🔮 Delivery Time Forecast")
    st.markdown("---")

    # ==========================================
    # Generate Forecast
    # ==========================================

    with st.spinner("🔮 Generating delivery-time forecast..."):

        historical, forecast = generate_real_forecast()

    # ==========================================
    # Forecast Summary
    # ==========================================

    last_actual = historical[
        "average_delivery_time"
    ].iloc[-1]

    average_forecast = forecast[
        "predicted_delivery_time"
    ].mean()

    forecast_change = (
        average_forecast - last_actual
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Latest Avg Delivery Time",
        f"{last_actual:.1f} min"
    )

    col2.metric(
        "7-Day Forecast",
        f"{average_forecast:.1f} min"
    )

    col3.metric(
        "Expected Change",
        f"{forecast_change:+.1f} min"
    )

    st.markdown("---")

    # ==========================================
    # Forecast Chart
    # ==========================================

    st.subheader("📈 Historical vs Forecasted Delivery Time")

    fig = go.Figure()

    # Historical line
    fig.add_trace(
        go.Scatter(
            x=historical["date"],
            y=historical["average_delivery_time"],
            mode="lines+markers",
            name="Historical"
        )
    )

    # Forecast line
    fig.add_trace(
        go.Scatter(
            x=forecast["date"],
            y=forecast["predicted_delivery_time"],
            mode="lines+markers",
            name="Forecast"
        )
    )

    fig.update_layout(
        xaxis_title="Operational Period",
        yaxis_title="Average Delivery Time (minutes)",
        title="7-Period Delivery Time Forecast",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("---")

    # ==========================================
    # Forecast Table
    # ==========================================

    st.subheader("📅 7-Period Forecast")

    display_forecast = forecast.copy()

    display_forecast["date"] = (
        display_forecast["date"]
        .dt.strftime("%Y-%m-%d")
    )

    display_forecast[
        "predicted_delivery_time"
    ] = display_forecast[
        "predicted_delivery_time"
    ].round(2)

    display_forecast = display_forecast.rename(
        columns={
            "date": "Forecast Period",
            "predicted_delivery_time": "Predicted Delivery Time (min)"
        }
    )

    st.dataframe(
        display_forecast,
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    # ==========================================
    # Automatic Interpretation
    # ==========================================

    st.subheader("🧠 Forecast Interpretation")

    if forecast_change > 2:

        st.error(
            f"🚨 Delivery performance is expected to worsen. "
            f"Average delivery time may increase by "
            f"{forecast_change:.1f} minutes."
        )

        st.warning(
            "Recommended action: investigate rider availability, "
            "traffic conditions and operational capacity."
        )

    elif forecast_change < -2:

        st.success(
            f"🟢 Delivery performance is expected to improve "
            f"by approximately {abs(forecast_change):.1f} minutes."
        )

    else:

        st.info(
            "🟡 Delivery performance is expected to remain "
            "relatively stable."
        )

    st.caption(
        "Forecast generated from historical operational "
        "delivery-time patterns. The source dataset does not "
        "contain timestamps, so records are grouped into "
        "sequential operational periods for forecasting."
    )


if __name__ == "__main__":
    show_forecast()