import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

from real_data_loader import load_real_data


def profile_real_data():

    df = load_real_data()

    print("=" * 65)
    print("OPSLENS AI - REAL DATA OPERATIONAL PROFILE")
    print("=" * 65)

    print(f"\nTotal Orders: {len(df):,}")

    # ==========================================
    # DELIVERY TIME
    # ==========================================

    print("\nDELIVERY TIME PERFORMANCE")

    print(
        f"Average: "
        f"{df['actual_delivery_minutes'].mean():.2f} min"
    )

    print(
        f"Median: "
        f"{df['actual_delivery_minutes'].median():.2f} min"
    )

    print(
        f"Minimum: "
        f"{df['actual_delivery_minutes'].min():.2f} min"
    )

    print(
        f"Maximum: "
        f"{df['actual_delivery_minutes'].max():.2f} min"
    )

    # ==========================================
    # DISTANCE
    # ==========================================

    print("\nDELIVERY DISTANCE")

    print(
        f"Average: "
        f"{df['distance_km'].mean():.2f} km"
    )

    print(
        f"Median: "
        f"{df['distance_km'].median():.2f} km"
    )

    print(
        f"Maximum: "
        f"{df['distance_km'].max():.2f} km"
    )

    # ==========================================
    # TRAFFIC
    # ==========================================

    print("\nAVERAGE DELIVERY TIME BY TRAFFIC")

    traffic = (
        df.groupby("traffic_level")
        ["actual_delivery_minutes"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    print(
        traffic.round(2).to_string()
    )

    # ==========================================
    # WEATHER
    # ==========================================

    print("\nAVERAGE DELIVERY TIME BY WEATHER")

    weather = (
        df.groupby("weather")
        ["actual_delivery_minutes"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    print(
        weather.round(2).to_string()
    )

    # ==========================================
    # PEAK HOUR
    # ==========================================

    print("\nAVERAGE DELIVERY TIME BY PEAK HOUR")

    peak = (
        df.groupby("peak_hour")
        ["actual_delivery_minutes"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    print(
        peak.round(2).to_string()
    )

    # ==========================================
    # WEEKEND
    # ==========================================

    print("\nAVERAGE DELIVERY TIME BY WEEKEND")

    weekend = (
        df.groupby("weekend")
        ["actual_delivery_minutes"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    print(
        weekend.round(2).to_string()
    )

    # ==========================================
    # CITY
    # ==========================================

    print("\nAVERAGE DELIVERY TIME BY CITY")

    city = (
        df.groupby("city")
        ["actual_delivery_minutes"]
        .agg(
            ["count", "mean"]
        )
        .sort_values(
            by="mean",
            ascending=False
        )
    )

    print(
        city.round(2).to_string()
    )

    # ==========================================
    # DISTANCE SEGMENTS
    # ==========================================

    df["distance_category"] = pd.cut(
        df["distance_km"],
        bins=[
            0,
            5,
            10,
            15,
            100
        ],
        labels=[
            "0-5 km",
            "5-10 km",
            "10-15 km",
            "15+ km"
        ]
    )

    print("\nAVERAGE DELIVERY TIME BY DISTANCE")

    distance = (
        df.groupby(
            "distance_category",
            observed=False
        )["actual_delivery_minutes"]
        .agg(
            ["count", "mean"]
        )
    )

    print(
        distance.round(2).to_string()
    )

    # ==========================================
    # TOP DELIVERY TIMES
    # ==========================================

    print("\nSLOWEST OPERATIONAL SEGMENTS")

    print(
        "\nTop 10 highest delivery times:"
    )

    print(
        df.nlargest(
            10,
            "actual_delivery_minutes"
        )[
            [
                "order_id",
                "distance_km",
                "weather",
                "traffic_level",
                "peak_hour",
                "actual_delivery_minutes"
            ]
        ].to_string(
            index=False
        )
    )

    print("\n" + "=" * 65)
    print("Real data profiling completed successfully!")
    print("=" * 65)


if __name__ == "__main__":

    import pandas as pd

    profile_real_data()