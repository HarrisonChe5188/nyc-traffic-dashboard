from pathlib import Path
import sqlite3

import pandas as pd


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
DATA_PATH = BASE_DIR / "data" / "North_Manhattan_Cleaned.csv"
DB_PATH = BASE_DIR / "database" / "traffic.db"


def load_data():
    """Load raw traffic data from CSV."""

    df = pd.read_csv(DATA_PATH)

    return df

def clean_data(df):

    df["tt_median_timestamp"] = pd.to_datetime(
        df["tt_median_timestamp"]
    )

    df["hour_interval"] = pd.to_datetime(
        df["hour_interval"]
    )

    df["hour"] = df["hour_interval"].dt.hour

    df = df.dropna(
        subset=["spd_mph"]
    )

    df = df.rename(
        columns={
            "tt_median_timestamp": "timestamp",
            "tt_median_sec": "travel_time_sec",
            "spd_mph": "speed_mph",
            "tt_median_sample_size": "sample_size"
        }
    )

    return df


def create_connection():
    """Create SQLite database connection."""

    return sqlite3.connect(DB_PATH)


def load_to_database(df):
    """Load cleaned data into SQLite."""

    conn = create_connection()

    df.to_sql(
        "traffic_speed",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()


def initialize_database():
    """Load, clean, and store the traffic data."""

    df = load_data()

    df = clean_data(df)

    load_to_database(df)

    return df