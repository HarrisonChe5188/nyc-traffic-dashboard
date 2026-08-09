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


def get_corridors():
    """Get all available traffic corridors."""

    query = """
        SELECT DISTINCT link_name
        FROM traffic_speed
        ORDER BY link_name;
    """

    return run_query(query)


def hourly_speed(corridor):

    query = """
        SELECT
            hour,
            AVG(speed_mph) AS avg_speed

        FROM traffic_speed
        WHERE link_name = ?
        GROUP BY hour
        ORDER BY hour;
    """

    return run_query(
        query,
        [corridor]
    )


def corridor_speed():
    """Calculate average speed for each corridor."""

    query = """
        SELECT link_name, AVG(speed_mph) AS avg_speed
        FROM traffic_speed
        GROUP BY link_name
        ORDER BY avg_speed ASC;
    """

    return run_query(query)


def slowest_hours():
    """Find the five slowest hours across all corridors."""

    query = """
        SELECT hour, AVG(speed_mph) AS avg_speed
        FROM traffic_speed
        GROUP BY hour
        ORDER BY avg_speed ASC
        LIMIT 5;
    """

    return run_query(query)


def daily_speed(corridor):
    """Calculate average speed by day of week."""

    query = """
        SELECT day_of_week, AVG(speed_mph) AS avg_speed
        FROM traffic_speed
        WHERE link_name = ?
        GROUP BY day_of_week
        ORDER BY avg_speed ASC;
    """

    return run_query(
        query,
        [corridor]
    )