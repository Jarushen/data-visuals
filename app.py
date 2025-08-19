"""
Streamlit sunburst dashboard for the Master Data set v13.

This application reads the Excel file located in the ``data`` folder,
cleans the ``Master`` sheet and presents several interactive
visualisations.  Sunburst charts show how ``Level 1``, ``Level 2``
and ``Level 3`` categories break down across different metrics such
as Quantity, Volunteer Hours, Value R and Souls.  Additional bar
and line charts summarise the data by category and year.  Filters in
the sidebar allow you to drill down by year, province and top‑level
category.

To run the app locally:

1. Install dependencies from ``requirements.txt`` (preferably in a
   virtual environment).
2. Ensure the Excel file ``Master Data set v13 - Form - 20250731.xlsx``
   is present in the ``data`` directory.
3. Run ``streamlit run app.py``.
"""

import pathlib
import pandas as pd
import plotly.express as px
import streamlit as st


# Path to the Excel workbook.  The file is expected to be located in
# the ``data`` directory relative to this script.  Adjust this path
# if you move the data elsewhere.
DATA_FILE = pathlib.Path(__file__).parent / "data" / "Master Data set v13 - Form - 20250731.xlsx"


@st.cache_data(show_spinner=True)
def load_master_sheet(path: pathlib.Path) -> pd.DataFrame:
    """Load and clean the Master sheet from the given Excel file.

    The spreadsheet contains summary rows and multi‑level headers in
    the first three rows.  This function drops those rows, uses the
    fourth row as column names, removes invalid columns, and ensures
    numeric columns are converted appropriately.

    Args:
        path: Path to the Excel workbook.

    Returns:
        A cleaned pandas DataFrame.
    """
    raw = pd.read_excel(path, sheet_name="Master", header=None)
    # Data starts on row 3 (0‑based index).  The header row is at index 2.
    df = raw.iloc[3:].reset_index(drop=True).copy()
    df.columns = raw.iloc[2]
    # Drop duplicate column names
    df = df.loc[:, ~df.columns.duplicated()]
    # Remove columns with NaN or numeric header names
    valid_cols = [c for c in df.columns if pd.notna(c) and not isinstance(c, (int, float))]
    df = df[valid_cols].copy()
    # Convert known numeric columns
    for col in ["Quantity", "Volunteer Hours", "Value R", "Souls", "Project Year"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # Strip whitespace from text columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters to the dataset.

    Users can filter on Project Year, Province and Level 1 category.
    Empty selections are interpreted as 'select all'.

    Args:
        df: The full cleaned DataFrame.

    Returns:
        The filtered DataFrame.
    """
    st.sidebar.header("Filters")
    # Project Year filter
    years = sorted(df["Project Year"].dropna().unique().astype(int).tolist()) if "Project Year" in df else []
    year_sel = st.sidebar.multiselect("Project Year", years, default=years)
    # Province filter
    provinces = sorted(df["Province"].dropna().unique().tolist()) if "Province" in df else []
    prov_sel = st.sidebar.multiselect("Province", provinces, default=provinces)
    # Level 1 filter
    lvl1s = sorted(df["Level 1"].dropna().unique().tolist()) if "Level 1" in df else []
    lvl1_sel = st.sidebar.multiselect("Level 1", lvl1s, default=lvl1s)
    # Apply filters
    filtered = df.copy()
    if year_sel:
        filtered = filtered[filtered["Project Year"].isin(year_sel)]
    if prov_sel:
        filtered = filtered[filtered["Province"].isin(prov_sel)]
    if lvl1_sel:
        filtered = filtered[filtered["Level 1"].isin(lvl1_sel)]
    return filtered


def plot_sunburst(df: pd.DataFrame, metric: str) -> None:
    """Render a sunburst chart for a given metric.

    Args:
        df: Filtered DataFrame.
        metric: Column to use for segment sizes.
    """
    if metric not in df.columns:
        st.info(f"Metric '{metric}' not found in the data.")
        return
    d = df.dropna(subset=["Level 1", "Level 2", "Level 3", metric]).copy()
    d = d[d[metric] > 0]
    if d.empty:
        st.info(f"No data available for {metric}.")
        return
    fig = px.sunburst(
        d,
        path=["Level 1", "Level 2", "Level 3"],
        values=metric,
        color="Level 1",
        title=f"{metric} distribution across Levels",
        branchvalues="total",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(margin=dict(t=50, l=0, r=0, b=0), title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_bar(df: pd.DataFrame, metric: str) -> None:
    """Plot a bar chart of totals by Level 1 for the selected metric."""
    if metric not in df.columns:
        return
    g = df.groupby("Level 1")[metric].sum().reset_index().sort_values(metric, ascending=False)
    fig = px.bar(g, x="Level 1", y=metric, title=f"Total {metric} by Level 1", color="Level 1")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def plot_line(df: pd.DataFrame, metric: str) -> None:
    """Plot a line chart of totals by Project Year for the selected metric."""
    if metric not in df.columns or "Project Year" not in df.columns:
        return
    g = df.groupby("Project Year")[metric].sum().reset_index().sort_values("Project Year")
    fig = px.line(g, x="Project Year", y=metric, markers=True, title=f"{metric} over time")
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Sunburst Dashboard", layout="wide")
    st.title("Projects Sunburst Dashboard")
    # Load data
    if not DATA_FILE.exists():
        st.error(f"Data file missing: {DATA_FILE}")
        return
    df = load_master_sheet(DATA_FILE)
    filtered_df = filter_data(df)
    # Show KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Quantity", f"{filtered_df['Quantity'].sum(skipna=True):,.2f}" if 'Quantity' in filtered_df else "N/A")
    c2.metric("Volunteer Hours", f"{filtered_df['Volunteer Hours'].sum(skipna=True):,.0f}" if 'Volunteer Hours' in filtered_df else "N/A")
    c3.metric("Total Value (R)", f"{filtered_df['Value R'].sum(skipna=True):,.2f}" if 'Value R' in filtered_df else "N/A")
    c4.metric("Souls", f"{filtered_df['Souls'].sum(skipna=True):,.0f}" if 'Souls' in filtered_df else "N/A")
    # Sunburst charts for each metric
    st.subheader("Sunburst Charts")
    for metric in ["Quantity", "Volunteer Hours", "Value R", "Souls"]:
        if metric in filtered_df.columns:
            st.write(f"### {metric}")
            plot_sunburst(filtered_df, metric)
    # Aggregate charts
    st.subheader("Aggregate Views")
    metric_choice = st.selectbox(
        "Select metric for aggregates", [m for m in ["Quantity", "Volunteer Hours", "Value R", "Souls"] if m in filtered_df.columns]
    )
    bar_col, line_col = st.columns(2)
    with bar_col:
        plot_bar(filtered_df, metric_choice)
    with line_col:
        plot_line(filtered_df, metric_choice)
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(filtered_df.head(200))


if __name__ == "__main__":
    main()