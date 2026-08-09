import streamlit as st

from src.data import initialize_database

from src.analytics import (
    get_corridors,
    hourly_speed,
    corridor_speed,
    daily_speed,
    slowest_hours,
    fastest_hours
)

from src.plots import (
    hourly_speed_plot,
    daily_speed_plot
)


# Page configuration
st.set_page_config(
    page_title="NYC Traffic Speed Dashboard",
    layout="wide"
)


# Title
st.title("NYC Traffic Speed Analysis (6/11/2026 - 6/19/2026)")

st.write(
    """
    Analysis of traffic sensor data across major NYC
    corridors. Explore traffic speed patterns by
    corridor, hour, and day of week.
    """
)


# Init database
initialize_database()


# Corridor selection
corridors = get_corridors()
corridor_list = corridors["link_name"].tolist()

selected_corridor = st.selectbox(
    "Select a corridor",
    corridor_list
)


# Load analysis data

hourly_data = hourly_speed(
    selected_corridor
)

daily_data = daily_speed(
    selected_corridor
)


# Calculate avg, slowest, fastest hour metrics

average_speed = hourly_data["avg_speed"].mean()

slowest_row = hourly_data.loc[
    hourly_data["avg_speed"].idxmin()
]

fastest_row = hourly_data.loc[
    hourly_data["avg_speed"].idxmax()
]

slowest_hour = slowest_row["hour"]
slowest_speed = slowest_row["avg_speed"]

fastest_hour = fastest_row["hour"]
fastest_speed = fastest_row["avg_speed"]

# Cards for average speed, slowest hour, fastest hour
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Speed",
        f"{average_speed:.1f} mph"
    )

with col2:
    st.metric(
        "Slowest Hour",
        f"{int(slowest_hour):02d}:00",
        f"{slowest_speed:.1f} mph"
    )

with col3:
    st.metric(
        "Fastest Hour",
        f"{int(fastest_hour):02d}:00",
        f"{fastest_speed:.1f} mph"
    )


# Key findings
st.subheader("Key Findings")

st.write(
    f"""
    **{selected_corridor}** averaged **{average_speed:.1f} mph**
    across the observed hours.

    The slowest period was **{int(slowest_hour):02d}:00**,
    when average speed fell to **{slowest_speed:.1f} mph**.

    The fastest period was **{int(fastest_hour):02d}:00**,
    when average speed reached **{fastest_speed:.1f} mph**.
    """
)


# Hourly speed
st.subheader(
    f"Hourly Speed — {selected_corridor}"
)

st.plotly_chart(
    hourly_speed_plot(
        hourly_data,
        selected_corridor
    ),
    use_container_width=True
)


# Day-of-week analysis
st.subheader(
    f"Speed by Day — {selected_corridor}"
)

fastest_day = daily_data.loc[
    daily_data["avg_speed"].idxmax()
]

slowest_day = daily_data.loc[
    daily_data["avg_speed"].idxmin()
]

st.write(
    f"""
    Speeds were highest on **{fastest_day['day_of_week']}**
    at **{fastest_day['avg_speed']:.1f} mph**.

    Speeds were lowest on **{slowest_day['day_of_week']}**
    at **{slowest_day['avg_speed']:.1f} mph**.
    """
)

st.plotly_chart(
    daily_speed_plot(
        daily_data,
        selected_corridor
    ),
    use_container_width=True
)


# Overall dataset findings
st.subheader("Across All Corridors")

corridor_data = corridor_speed()
fastest_corridor = corridor_data.iloc[-1]
slowest_corridor = corridor_data.iloc[0]

st.write(
    f"""
    Across the analyzed corridors, **{slowest_corridor['link_name']}**
    had the lowest average speed at
    **{slowest_corridor['avg_speed']:.1f} mph**.

    **{fastest_corridor['link_name']}** had the highest average speed
    at **{fastest_corridor['avg_speed']:.1f} mph**.
    """
)


# Slowest hours across all corridors

overall_slowest = slowest_hours()

st.write(
    "The five slowest corridor-hour combinations were:"
)

for _, row in overall_slowest.iterrows():

    st.write(
        f"- **{row['link_name']}** — "
        f"{int(row['hour']):02d}:00 — "
        f"**{row['avg_speed']:.1f} mph**"
    )

# Fastest hours across all corridors

overall_fastest = fastest_hours()

st.write(
    "The five fastest corridor-hour combinations were:"
)

for _, row in overall_fastest.iterrows():

    st.write(
        f"- **{row['link_name']}** — "
        f"{int(row['hour']):02d}:00 — "
        f"**{row['avg_speed']:.1f} mph**"
    )