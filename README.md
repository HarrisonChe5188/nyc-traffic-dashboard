# NYC Traffic Speed Dashboard

Interactive Streamlit dashboard for analyzing NYC traffic sensor data across major corridors.

The project uses **Python/Pandas for data cleaning**, **SQLite for storage**, and **SQL for analysis**, with Streamlit and Plotly for visualization.

## Data Pipeline

```text
Raw CSV
   ↓
Pandas Cleaning
   ↓
SQLite Database
   ↓
SQL Queries
   ↓
Pandas DataFrames
   ↓
Streamlit Dashboard
```

## Features

* Average speed by corridor
* Hourly speed analysis
* Fastest and slowest hours
* Speed by day of week
* Slowest corridor-hour combinations
* Observation counts for SQL results

## Tech Stack

* Python
* Pandas
* SQLite / SQL
* Streamlit
* Plotly

## Project Structure

```text
nyc-traffic-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── North manhattan Before study 2026.csv
│   └── North_Manhattan_Cleaned.csv
│
└── src/
    ├── analytics.py
    ├── cleaning.py
    ├── data.py
    ├── loader.py
    └── plots.py
```

### Key Components

**`cleaning.py`** — Cleans and transforms raw traffic data using Pandas.

**`data.py`** — Creates the SQLite database and manages the traffic data table.

**`analytics.py`** — Contains SQL queries for traffic analysis.

**`plots.py`** — Creates Plotly visualizations.

**`app.py`** — Streamlit dashboard and user interface.

## Example SQL

```sql
SELECT
    link_name,
    ROUND(AVG(speed_mph), 2) AS avg_speed,
    COUNT(*) AS observations
FROM traffic_speed
GROUP BY link_name
ORDER BY avg_speed ASC;
```

SQL results are returned as Pandas DataFrames using `pd.read_sql_query()` and passed to the Streamlit application for analysis and visualization.

## Run Locally

```bash
git clone https://github.com/harrisonche5188/nyc-traffic-dashboard.git
cd nyc-traffic-dashboard

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`.

## Data

The raw and cleaned CSV files are stored locally in the `data/` directory and are excluded from version control due to their size.
