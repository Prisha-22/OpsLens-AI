import os
import sys

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

# Add python folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import pandas as pd
import numpy as np

from database import get_connection
from sklearn.linear_model import LinearRegression


def generate_forecast():

    # ==========================================
    # LOAD ORDER DATA
    # ==========================================

    conn = get_connection()

    query = """
    SELECT
        order_time,
        actual_delivery_minutes
    FROM orders
    WHERE actual_delivery_minutes IS NOT NULL
    ORDER BY order_time;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ==========================================
    # PREPARE DAILY DATA
    # ==========================================

    df["order_time"] = pd.to_datetime(
        df["order_time"]
    )

    df["date"] = df["order_time"].dt.date

    daily = (
        df
        .groupby("date")["actual_delivery_minutes"]
        .mean()
        .reset_index()
    )

    daily.columns = [
        "date",
        "average_delivery_time"
    ]

    daily["date"] = pd.to_datetime(
        daily["date"]
    )

    # ==========================================
    # CREATE TIME INDEX
    # ==========================================

    daily["day_number"] = np.arange(
        len(daily)
    )

    # ==========================================
    # TRAIN MODEL
    # ==========================================

    X = daily[["day_number"]]

    y = daily[
        "average_delivery_time"
    ]

    model = LinearRegression()

    model.fit(X, y)

    # ==========================================
    # FUTURE DAYS
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

    # ==========================================
    # CREATE FORECAST DATAFRAME
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

    historical, forecast = generate_forecast()

    print("=" * 60)
    print("OPSLENS AI - DELIVERY TIME FORECAST")
    print("=" * 60)

    print("\nHistorical Data:")
    print(historical.tail(10))

    print("\n7-Day Forecast:")

    print(
        forecast.to_string(
            index=False
        )
    )

    print("\nForecast completed successfully!")