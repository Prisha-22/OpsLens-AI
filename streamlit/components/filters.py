import streamlit as st


def show_filters(customers, orders):

    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.selectbox(
            "🏙 City",
            ["All"] + sorted(customers["city"].unique())
        )

    with col2:
        weather = st.selectbox(
            "🌦 Weather",
            ["All"] + sorted(orders["weather"].unique())
        )

    with col3:
        status = st.selectbox(
            "📦 Status",
            ["All"] + sorted(orders["delivery_status"].unique())
        )

    return city, weather, status