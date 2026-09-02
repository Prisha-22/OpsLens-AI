import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import streamlit as st

from python.insights.insight_engine import generate_real_insights


def show_ai_insights():

    st.title("💡 AI Insights")
    st.markdown(
        "### Real-world delivery operations intelligence and recommendations"
    )

    st.markdown("---")

    with st.spinner("🧠 Analyzing real delivery operations..."):

        insights = generate_real_insights()

    # ==========================================
    # SUMMARY
    # ==========================================

    high_count = sum(
        1 for item in insights
        if item["severity"] == "High"
    )

    medium_count = sum(
        1 for item in insights
        if item["severity"] == "Medium"
    )

    critical_count = sum(
        1 for item in insights
        if item["severity"] == "Critical"
    )

    info_count = sum(
        1 for item in insights
        if item["severity"] == "Info"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🚨 High Priority",
        high_count
    )

    col2.metric(
        "🔴 Critical",
        critical_count
    )

    col3.metric(
        "⚠️ Medium Priority",
        medium_count
    )

    col4.metric(
        "ℹ️ Informational",
        info_count
    )

    st.markdown("---")

    # ==========================================
    # INSIGHTS
    # ==========================================

    st.subheader("🧠 Real Operational Insights")

    for item in insights:

        severity = item["severity"]

        if severity == "Critical":

            st.error(
                f"🔴 {item['category']}"
            )

        elif severity == "High":

            st.warning(
                f"🚨 {item['category']}"
            )

        elif severity == "Medium":

            st.info(
                f"⚠️ {item['category']}"
            )

        else:

            st.success(
                f"ℹ️ {item['category']}"
            )

        st.markdown(
            f"**Insight:** {item['insight']}"
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
        "🔄 Refresh Real Insights",
        width="stretch"
    ):

        st.rerun()

    st.caption(
        "OpsLens AI generates these insights from the "
        "real delivery dataset containing 45,584 orders. "
        "Recommendations are analytical suggestions and "
        "should be validated before operational decisions."
    )


if __name__ == "__main__":
    show_ai_insights()