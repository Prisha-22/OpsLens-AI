import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import streamlit as st

from python.insights.real_recommendation_engine import (
    generate_real_recommendations
)


def show_recommendations():

    st.title("💡 Operational Recommendations")

    st.markdown(
        "### AI-driven actions for improving delivery operations"
    )

    st.markdown("---")

    with st.spinner("🧠 Analyzing real operational data..."):

        recommendations = generate_real_recommendations()

    # ==========================================
    # SUMMARY
    # ==========================================

    critical_count = sum(
        1
        for item in recommendations
        if item["priority"] == "Critical"
    )

    high_count = sum(
        1
        for item in recommendations
        if item["priority"] == "High"
    )

    medium_count = sum(
        1
        for item in recommendations
        if item["priority"] == "Medium"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🚨 Critical",
        critical_count
    )

    col2.metric(
        "🔴 High Priority",
        high_count
    )

    col3.metric(
        "⚠️ Medium Priority",
        medium_count
    )

    st.markdown("---")

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================

    st.subheader("🧠 Recommended Actions")

    if not recommendations:

        st.success(
            "🟢 No immediate operational interventions "
            "are required."
        )

    for item in recommendations:

        priority = item["priority"]

        if priority == "Critical":

            st.error(
                f"🚨 {item['area']}"
            )

        elif priority == "High":

            st.warning(
                f"🔴 {item['area']}"
            )

        else:

            st.info(
                f"⚠️ {item['area']}"
            )

        st.markdown(
            f"**🔎 Finding:** {item['finding']}"
        )

        st.markdown(
            f"**💡 Recommendation:** "
            f"{item['recommendation']}"
        )

        st.markdown("---")

    # ==========================================
    # REFRESH
    # ==========================================

    if st.button(
        "🔄 Refresh Recommendations",
        width="stretch"
    ):

        st.rerun()

    st.caption(
        "OpsLens AI generates recommendations from "
        "the real delivery operations dataset. "
        "Recommendations are analytical suggestions "
        "and should be validated before operational decisions."
    )


if __name__ == "__main__":

    show_recommendations()