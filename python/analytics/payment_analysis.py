import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from database import get_connection


def run_payment_analysis():

    conn = get_connection()

    query = """
    SELECT *
    FROM payments;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("=" * 50)
    print("PAYMENT ANALYSIS")
    print("=" * 50)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nTotal Payment Amount:")
    print(round(df["amount"].sum(), 2))

    print("\nAverage Payment Amount:")
    print(round(df["amount"].mean(), 2))

    print("\nPayment Modes:")
    print(df["payment_mode"].value_counts())

    print("\nPayment Status:")
    print(df["payment_status"].value_counts())