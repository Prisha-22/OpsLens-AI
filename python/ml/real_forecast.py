import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import pandas as pd
import numpy as np

from python.database import get_connection
from sklearn.linear_model import LinearRegression


def generate_real_forecast():

    # ==========================================
    # LOAD REAL DELIVERY DATA
    # ==========================================

    conn = get_connection()

    query = """
    SELECT
        actual_delivery_minutes
    FROM real_delivery_orders
    WHERE actual_delivery_minutes IS NOT NULL;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ==========================================
    # CREATE DAILY DELIVERY DATA
    # ==========================================

    # Real dataset does not contain order_time,
    # so use the available delivery records directly.
    # The dataset is ordered as operational observations.

    df["record_number"] = np.arange(len(df))

    # Create sequential operational periods
    # using groups of approximately 1000 deliveries.
    df["period"] = (
        df["record_number"] // 1000
    )

    daily = (
        df.groupby("period")["actual_delivery_minutes"]
        .mean()
        .reset_index()
    )

    daily.columns = [
        "period",
        "average_delivery_time"
    ]

    daily["date"] = pd.date_range(
        start="2026-01-01",
        periods=len(daily),
        freq="D"
    )

    daily["day_number"] = np.arange(
        len(daily)
    )

    # ==========================================
    # TRAIN FORECAST MODEL
    # ==========================================

    X = daily[["day_number"]]

    y = daily[
        "average_delivery_time"
    ]

    model = LinearRegression()

    model.fit(X, y)

    # ==========================================
    # GENERATE 7-DAY FORECAST
    # ==========================================

    forecast_days = 7

    last_day_number = daily[
        "day_number"
    ].max()

    future_day_numbers = np.arange(
        last_day_number + 1,
        last_day_number + 1 + forecast_days
    )

    future_predictions = model.predict(
        future_day_numbers.reshape(-1, 1)
    )

    # Prevent unrealistic negative predictions
    future_predictions = np.maximum(
        future_predictions,
        0
    )

    # ==========================================
    # FORECAST DATES
    # ==========================================

    last_date = daily["date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=forecast_days,
        freq="D"
    )

    forecast = pd.DataFrame({
        "date": future_dates,
        "predicted_delivery_time": future_predictions
    })

    # ==========================================
    # RETURN RESULTS
    # ==========================================

    return daily, forecast


if __name__ == "__main__":

    historical, forecast = generate_real_forecast()

    print("=" * 60)
    print("OPSLENS AI - REAL DELIVERY TIME FORECAST")
    print("=" * 60)

    print("\nHistorical Data:")
    print(
        historical[
            [
                "date",
                "average_delivery_time"
            ]
        ].tail(10)
    )

    print("\n7-Day Forecast:")

    print(
        forecast.to_string(
            index=False
        )
    )

    print("\nForecast completed successfully!")