import plotly.express as px


def hourly_speed_plot(df, corridor):
    """Plot average speed by hour of day."""

    fig = px.line(
        df,
        x="hour",
        y="avg_speed",
        markers=True,
        title=f"Average Speed by Hour — {corridor}"
    )

    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Average Speed (mph)",
        xaxis=dict(
            tickmode="linear",
            dtick=1
        )
    )

    return fig


def corridor_speed_plot(df):
    """Plot average speed by corridor."""

    fig = px.bar(
        df,
        x="link_name",
        y="avg_speed",
        title="Average Speed by Corridor"
    )

    fig.update_layout(
        xaxis_title="Corridor",
        yaxis_title="Average Speed (mph)"
    )

    return fig


def daily_speed_plot(df, corridor):
    """Plot average speed by day of week."""

    fig = px.bar(
        df,
        x="day_of_week",
        y="avg_speed",
        title=f"Average Speed by Day — {corridor}"
    )

    fig.update_layout(
        xaxis_title="Day",
        yaxis_title="Average Speed (mph)"
    )

    return fig