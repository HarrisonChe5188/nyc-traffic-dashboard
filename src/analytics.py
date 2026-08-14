import streamlit as st

from src.data import create_connection

import pandas as pd


def run_query(query, params=None):
    """Execute a SQL query and return the results as a DataFrame."""

    conn = create_connection()

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result


@st.cache_data
def get_corridors():
    """Get all available traffic corridors."""

    query = """
        SELECT DISTINCT
            link_name
        FROM traffic_speed
        ORDER BY link_name;
    """

    return run_query(query)


@st.cache_data
def hourly_speed(corridor):
    """Calculate average speed by hour for a corridor."""

    query = """
        SELECT
            hour,
            ROUND(AVG(speed_mph), 2) AS avg_speed,
            COUNT(*) AS observations
        FROM traffic_speed
        WHERE link_name = ?
        GROUP BY hour
        ORDER BY hour;
    """

    return run_query(
        query,
        [corridor]
    )


@st.cache_data
def corridor_speed():
    """Compare average speed across corridors."""

    query = """
        SELECT
            link_name,
            ROUND(AVG(speed_mph), 2) AS avg_speed,
            COUNT(*) AS observations
        FROM traffic_speed
        GROUP BY link_name
        ORDER BY avg_speed ASC;
    """

    return run_query(query)


@st.cache_data
def daily_speed(corridor):
    """Calculate average speed by calendar date for a corridor."""

    query = """
        SELECT
            DATE(timestamp) AS date,
            ROUND(AVG(speed_mph), 2) AS avg_speed,
            COUNT(*) AS observations
        FROM traffic_speed
        WHERE link_name = ?
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp);
    """

    return run_query(
        query,
        [corridor]
    )


@st.cache_data
def slowest_hours():
    """Find the five slowest corridor-hour combinations."""

    query = """
        SELECT
            link_name,
            hour,
            ROUND(AVG(speed_mph), 2) AS avg_speed,
            COUNT(*) AS observations
        FROM traffic_speed
        GROUP BY link_name, hour
        ORDER BY avg_speed ASC
        LIMIT 5;
    """

    return run_query(query)


@st.cache_data
def fastest_hours():
    """Find the five fastest corridor-hour combinations."""

    query = """
        SELECT
            link_name,
            hour,
            ROUND(AVG(speed_mph), 2) AS avg_speed,
            COUNT(*) AS observations
        FROM traffic_speed
        GROUP BY link_name, hour
        ORDER BY avg_speed DESC
        LIMIT 5;
    """

    return run_query(query)