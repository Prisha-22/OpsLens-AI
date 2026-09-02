import streamlit as st
import plotly.express as px
import pandas as pd


def revenue_chart(filtered_orders):

    filtered_orders["order_time"] = pd.to_datetime(filtered_orders["order_time"])

    daily = (
        filtered_orders
        .groupby(filtered_orders["order_time"].dt.date)["order_value"]
        .sum()
        .reset_index()
    )

    daily.columns = ["Date", "Revenue"]

    fig = px.line(
        daily,
        x="Date",
        y="Revenue",
        title="Revenue Trend",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)


def delivery_status_chart(filtered_orders):

    data = (
        filtered_orders["delivery_status"]
        .value_counts()
        .reset_index()
    )

    data.columns = ["Status", "Count"]

    fig = px.bar(
        data,
        x="Status",
        y="Count",
        title="Delivery Status"
    )

    st.plotly_chart(fig, use_container_width=True)


def weather_chart(filtered_orders):

    data = (
        filtered_orders["weather"]
        .value_counts()
        .reset_index()
    )

    data.columns = ["Weather", "Orders"]

    fig = px.pie(
        data,
        names="Weather",
        values="Orders",
        title="Orders by Weather"
    )

    st.plotly_chart(fig, use_container_width=True)


def traffic_chart(filtered_orders):

    data = (
        filtered_orders["traffic_level"]
        .value_counts()
        .reset_index()
    )

    data.columns = ["Traffic", "Orders"]

    fig = px.bar(
        data,
        x="Traffic",
        y="Orders",
        title="Traffic Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)