import streamlit as st

from src.data import initialize_database

from src.analytics import (
    get_corridors,
    hourly_speed,
    corridor_speed,
    daily_speed
)

from src.plots import (
    hourly_speed_plot,
    corridor_speed_plot,
    daily_speed_plot
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="NYC Traffic Dashboard",
    page_icon="🚗",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("NYC Traffic Speed Dashboard")

st.write(
    """
    Analysis of traffic sensor data across major NYC
    corridors. Explore average speeds by corridor,
    hour, and day of week.
    """
)


# --------------------------------------------------
# Initialize database
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# Corridor selection
# --------------------------------------------------

corridors = get_corridors()

corridor_list = corridors["link_name"].tolist()

selected_corridor = st.selectbox(
    "Select a corridor",
    corridor_list
)


# --------------------------------------------------
# Hourly analysis
# --------------------------------------------------

hourly_data = hourly_speed(
    selected_corridor
)


# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

average_speed = hourly_data["avg_speed"].mean()

slowest_hour = hourly_data.loc[
    hourly_data["avg_speed"].idxmin(),
    "hour"
]

fastest_hour = hourly_data.loc[
    hourly_data["avg_speed"].idxmax(),
    "hour"
]


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Speed",
        f"{average_speed:.1f} mph"
    )


with col2:

    st.metric(
        "Slowest Hour",
        f"{int(slowest_hour):02d}:00"
    )


with col3:

    st.metric(
        "Fastest Hour",
        f"{int(fastest_hour):02d}:00"
    )


# --------------------------------------------------
# Hourly speed
# --------------------------------------------------

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


# --------------------------------------------------
# Corridor comparison
# --------------------------------------------------

st.subheader("Corridor Comparison")

corridor_data = corridor_speed()

st.plotly_chart(
    corridor_speed_plot(
        corridor_data
    ),
    use_container_width=True
)


# --------------------------------------------------
# Day of week
# --------------------------------------------------

st.subheader(
    f"Speed by Day — {selected_corridor}"
)

daily_data = daily_speed(
    selected_corridor
)

st.plotly_chart(
    daily_speed_plot(
        daily_data,
        selected_corridor
    ),
    use_container_width=True
)


# --------------------------------------------------
# Raw query results
# --------------------------------------------------

with st.expander("View Hourly Data"):

    st.dataframe(
        hourly_data,
        use_container_width=True
    )