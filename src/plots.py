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




def daily_speed_plot(df, corridor):
    """Plot average speed by date."""

    fig = px.bar(
        df,
        x="date",
        y="avg_speed",
        title=f"Average Speed by Day — {corridor}"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Average Speed (mph)"
    )

    return fig