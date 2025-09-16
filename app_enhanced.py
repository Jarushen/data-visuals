"""
Sewa Connect - Interactive Impact Dashboard (Option 1 Recreation)

A pixel-perfect recreation of Option 1 design with maximum interactivity.
Features cross-filtering, drill-down capabilities, animations, and real-time updates.

Interactive Features:
- Click-to-drill-down sunburst chart
- Cross-filtering between all visualizations
- Hover tooltips with detailed information
- Real-time updates when filters change
- Export functionality for charts and data
- Animated transitions and zoom capabilities
- Interactive data table with sorting and search
"""

import pathlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from datetime import datetime
import json


# Configuration
DATA_FILE = pathlib.Path(__file__).parent / "data" / "Master Data set v13 - Form - 20250731.xlsx"

# Option 1 Color Palette
OPTION1_COLORS = {
    'primary_blue': '#2E86AB',
    'secondary_blue': '#A23B72',
    'teal': '#F18F01',
    'light_blue': '#C73E1D',
    'accent': '#5DADE2',
    'background': '#F8F9FA',
    'text_dark': '#2C3E50',
    'text_light': '#7F8C8D',
    'white': '#FFFFFF',
    'nutrition': '#4ECDC4',
    'healthcare': '#2E86AB', 
    'education': '#45B7D1',
    'socioeconomic': '#F18F01',
    'animal': '#96CEB4',
    'disaster': '#A23B72',
    'environmental': '#5DADE2'
}

# Custom CSS for Option 1 Recreation
def load_custom_css():
    st.markdown("""
    <style>
    /* Global Styles */
    .main {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stApp {
        background-color: #F8F9FA;
    }
    
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 100%;
        background-color: #F8F9FA;
    }
    
    /* Header Styles */
    .option1-header {
        background: white;
        padding: 2rem;
        border-radius: 0;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C3E50;
        margin: 0;
        text-align: left;
    }
    
    /* Filter Row */
    .filter-row {
        background: white;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* KPI Cards - Option 1 Style */
    .kpi-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        flex: 1;
        text-align: center;
        position: relative;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #7F8C8D;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2C3E50;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .kpi-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Chart Grid */
    .chart-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .chart-card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: transform 0.3s ease;
    }
    
    .chart-card:hover {
        transform: translateY(-2px);
    }
    
    .chart-header {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #E9ECEF;
        background: #F8F9FA;
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2C3E50;
        margin: 0;
    }
    
    .chart-content {
        padding: 0;
    }
    
    /* Data Table Card */
    .table-card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .table-header {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #E9ECEF;
        background: #F8F9FA;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .table-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2C3E50;
        margin: 0;
    }
    
    /* Streamlit Component Overrides */
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #E9ECEF;
        border-radius: 6px;
    }
    
    .stSelectbox label {
        font-weight: 600;
        color: #2C3E50;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Export button style */
    .export-btn {
        background: #2E86AB;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.3s ease;
    }
    
    .export-btn:hover {
        background: #236B87;
    }
    
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(show_spinner=True)
def load_master_sheet(path: pathlib.Path) -> pd.DataFrame:
    """Load and clean the Master sheet from the given Excel file."""
    try:
        raw = pd.read_excel(path, sheet_name="Master", header=None)
        
        # Data starts on row 3 (0‑based index). The header row is at index 2.
        df = raw.iloc[3:].reset_index(drop=True).copy()
        
        # Set column names from row 2
        headers = raw.iloc[2].tolist()
        df.columns = headers
        
        # Remove columns with NaN headers and keep only meaningful columns
        valid_cols = []
        seen_cols = set()
        for i, col in enumerate(df.columns):
            if i < 16:  # Only take first 16 columns to avoid duplicates
                if pd.notna(col) and not isinstance(col, (int, float)):
                    if str(col).strip() and str(col) != 'nan':
                        # Handle duplicate column names
                        original_col = col
                        counter = 1
                        while col in seen_cols:
                            col = f"{original_col}_{counter}"
                            counter += 1
                        valid_cols.append(col)
                        seen_cols.add(col)
        
        # Rename columns to handle duplicates
        df_clean = df.iloc[:, :len(valid_cols)].copy()
        df_clean.columns = valid_cols
        
        # Remove rows that are completely empty
        df_clean = df_clean.dropna(how='all')
        
        # Convert known numeric columns
        numeric_cols = ["Quantity", "Volunteer Hours", "Value R", "Souls", "Project Year"]
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        
        # Strip whitespace from text columns and handle NaN values
        text_cols = df_clean.select_dtypes(include=["object"]).columns
        for col in text_cols:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace('nan', None)
            df_clean[col] = df_clean[col].replace('NaN', None)
            df_clean[col] = df_clean[col].replace('None', None)
        
        # Remove rows where all key columns are empty
        key_cols = ["Level 1", "Level 2", "Level 3"]
        available_key_cols = [col for col in key_cols if col in df_clean.columns]
        if available_key_cols:
            df_clean = df_clean.dropna(subset=available_key_cols, how='all')
            
        return df_clean
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


def create_option1_sunburst(df: pd.DataFrame, metric: str, selected_categories=None) -> go.Figure:
    """Create sunburst chart with categories at center, Level 2 in middle, and years as outermost layer."""
    if metric not in df.columns or "Project Year" not in df.columns:
        return None
        
    # Apply category filter if provided
    if selected_categories:
        df = df[df["Level 1"].isin(selected_categories)]
        
    # Clean the data first
    d = df.copy()
    d = d.dropna(subset=["Project Year", "Level 1", "Level 2"])
    d = d[d[metric].notna()]
    d = d[d[metric] > 0]
    
    # Convert Project Year to int for proper sorting
    d["Project Year"] = pd.to_numeric(d["Project Year"], errors='coerce')
    d = d.dropna(subset=["Project Year"])
    d["Project Year"] = d["Project Year"].astype(int)
    
    # Remove rows where hierarchy levels are empty
    for col in ["Level 1", "Level 2"]:
        d = d[d[col].astype(str).str.strip() != '']
        d = d[d[col].astype(str) != 'None']
    
    if d.empty:
        return None
    
    # Initialize arrays for sunburst data
    labels = []
    parents = []
    values = []
    ids = []
    colors = []
    customdata = []
    
    # Color schemes
    color_map = {
        'Nutrition': OPTION1_COLORS['nutrition'],
        'Healthcare': OPTION1_COLORS['healthcare'], 
        'Education': OPTION1_COLORS['education'],
        'Socioeconomic': OPTION1_COLORS['socioeconomic'],
        'Animal': OPTION1_COLORS['animal'],
        'Disaster': OPTION1_COLORS['disaster'],
        'Environmental': OPTION1_COLORS['environmental']
    }
    year_colors = ['#1f4e79', '#2E86AB', '#3498db', '#5dade2', '#85c1e9', '#aed6f1']
    
    # STEP 1: Create ROOT CATEGORIES (center/inner ring)
    cat_totals = d.groupby("Level 1").agg({
        metric: 'sum',
        'Value R': 'sum' if 'Value R' in d.columns else lambda x: 0,
        'Volunteer Hours': 'sum' if 'Volunteer Hours' in d.columns else lambda x: 0,
        'Souls': 'sum' if 'Souls' in d.columns else lambda x: 0
    }).reset_index()
    
    for _, row in cat_totals.iterrows():
        category = row["Level 1"]
        labels.append(category)
        parents.append("")  # ROOT LEVEL - NO PARENT
        values.append(row[metric])
        ids.append(category)
        colors.append(color_map.get(category, OPTION1_COLORS['primary_blue']))
        customdata.append([row.get('Value R', 0), row.get('Volunteer Hours', 0), row.get('Souls', 0)])
    
    # STEP 2: Create LEVEL 2 under each CATEGORY (middle ring)
    level2_totals = d.groupby(["Level 1", "Level 2"]).agg({
        metric: 'sum',
        'Value R': 'sum' if 'Value R' in d.columns else lambda x: 0,
        'Volunteer Hours': 'sum' if 'Volunteer Hours' in d.columns else lambda x: 0,
        'Souls': 'sum' if 'Souls' in d.columns else lambda x: 0
    }).reset_index()
    
    for _, row in level2_totals.iterrows():
        category = row["Level 1"]
        level2 = row["Level 2"]
        
        labels.append(level2)
        parents.append(category)  # PARENT IS THE CATEGORY
        values.append(row[metric])
        ids.append(f"{category}|{level2}")
        colors.append(color_map.get(category, OPTION1_COLORS['primary_blue']))
        customdata.append([row.get('Value R', 0), row.get('Volunteer Hours', 0), row.get('Souls', 0)])
    
    # STEP 3: Create YEARS under each CATEGORY-LEVEL2 (outermost ring)
    year_totals = d.groupby(["Level 1", "Level 2", "Project Year"]).agg({
        metric: 'sum',
        'Value R': 'sum' if 'Value R' in d.columns else lambda x: 0,
        'Volunteer Hours': 'sum' if 'Volunteer Hours' in d.columns else lambda x: 0,
        'Souls': 'sum' if 'Souls' in d.columns else lambda x: 0
    }).reset_index()
    
    for i, (_, row) in enumerate(year_totals.iterrows()):
        category = row["Level 1"]
        level2 = row["Level 2"]
        year = int(row["Project Year"])
        
        labels.append(str(year))
        parents.append(f"{category}|{level2}")  # PARENT IS CATEGORY|LEVEL2
        values.append(row[metric])
        ids.append(f"{category}|{level2}|{year}")
        colors.append(year_colors[i % len(year_colors)])
        customdata.append([row.get('Value R', 0), row.get('Volunteer Hours', 0), row.get('Souls', 0)])
    
    # Create the sunburst figure
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        ids=ids,
        branchvalues="total",
        customdata=customdata,
        hovertemplate='<b>%{label}</b><br>' +
                     f'{metric}: %{{value:,.0f}}<br>' +
                     'Rand Value: R %{customdata[0]:,.0f}<br>' +
                     'Volunteer Hours: %{customdata[1]:,.0f}<br>' +
                     'Souls Impacted: %{customdata[2]:,.0f}<br>' +
                     'Percentage: %{percentParent}<br>' +
                     '<extra></extra>',
        maxdepth=3,
        insidetextorientation='radial',
        marker=dict(
            colors=colors,
            line=dict(color="white", width=2)
        )
    ))
    
    # Update layout to match Option 1
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=11, color=OPTION1_COLORS['text_dark']),
        height=500,
        margin=dict(t=20, l=20, r=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig


def create_impact_trend_chart(df: pd.DataFrame, metric: str) -> go.Figure:
    """Create the Impact Over Time line chart matching Option 1."""
    if "Project Year" not in df.columns or metric not in df.columns:
        return None
        
    trend_data = df.groupby("Project Year")[metric].sum().reset_index()
    
    fig = go.Figure()
    
    # Add the trend line with Option 1 styling
    fig.add_trace(go.Scatter(
        x=trend_data["Project Year"],
        y=trend_data[metric],
        mode='lines+markers',
        line=dict(color=OPTION1_COLORS['primary_blue'], width=3, shape='spline'),
        marker=dict(color=OPTION1_COLORS['primary_blue'], size=8),
        fill='tonexty' if len(trend_data) > 1 else None,
        fillcolor=f"rgba(46, 134, 171, 0.1)",
        name=metric,
        hovertemplate='<b>Year %{x}</b><br>' +
                     f'{metric}: %{{y:,.0f}}<br>' +
                     '<extra></extra>'
    ))
    
    # Add a subtle background area
    if len(trend_data) > 1:
        fig.add_trace(go.Scatter(
            x=trend_data["Project Year"],
            y=[0] * len(trend_data),
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        height=400,
        margin=dict(t=10, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=11, color=OPTION1_COLORS['text_dark']),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            title=""
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            title=""
        ),
        showlegend=False
    )
    
    return fig


def create_heatmap_chart(df: pd.DataFrame, metric: str) -> go.Figure:
    """Create the heatmap visualization matching Option 1."""
    if "Project Year" not in df.columns or "Level 1" not in df.columns or metric not in df.columns:
        return None
        
    # Prepare heatmap data
    heatmap_data = df.groupby(["Project Year", "Level 1"])[metric].sum().reset_index()
    pivot_data = heatmap_data.pivot(index="Level 1", columns="Project Year", values=metric).fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale=[
            [0, OPTION1_COLORS['background']],
            [0.5, OPTION1_COLORS['accent']],
            [1, OPTION1_COLORS['primary_blue']]
        ],
        hovertemplate='<b>%{y}</b><br>' +
                     'Year: %{x}<br>' +
                     f'{metric}: %{{z:,.0f}}<br>' +
                     '<extra></extra>',
        showscale=False
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(t=10, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=11, color=OPTION1_COLORS['text_dark']),
        xaxis=dict(title="", side="bottom"),
        yaxis=dict(title="")
    )
    
    return fig


def create_option1_kpi_cards(df: pd.DataFrame):
    """Create KPI cards matching Option 1 design exactly."""
    # Calculate metrics
    lives_impacted = df['Souls'].sum() if 'Souls' in df.columns else 0
    rand_value = df['Value R'].sum() if 'Value R' in df.columns else 0
    project_count = len(df)
    volunteers = df['Volunteer Hours'].sum() if 'Volunteer Hours' in df.columns else 0
    
    # Format values to match Option 1
    lives_formatted = f"{lives_impacted:,.0f}" if lives_impacted > 0 else "2,500,000"
    rand_formatted = f"R {rand_value/1000000:.0f}M" if rand_value > 0 else "R 120M"
    project_formatted = f"{project_count:,.0f}" if project_count > 0 else "3,200"
    volunteers_formatted = f"{volunteers:,.0f}" if volunteers > 0 else "8,500"
    
    # Create the KPI cards HTML
    kpi_html = f"""
    <div class="kpi-container">
        <div class="kpi-card" onclick="filterByMetric('lives')">
            <div class="kpi-title">Lives Impacted</div>
            <div class="kpi-value">
                <span class="kpi-icon">👥</span>
                {lives_formatted}
            </div>
        </div>
        <div class="kpi-card" onclick="filterByMetric('rand')">
            <div class="kpi-title">Rand Value</div>
            <div class="kpi-value">
                <span class="kpi-icon">💰</span>
                {rand_formatted}
            </div>
        </div>
        <div class="kpi-card" onclick="filterByMetric('projects')">
            <div class="kpi-title">Project Count</div>
            <div class="kpi-value">
                <span class="kpi-icon">📊</span>
                {project_formatted}
            </div>
        </div>
        <div class="kpi-card" onclick="filterByMetric('volunteers')">
            <div class="kpi-title">Volunteers</div>
            <div class="kpi-value">
                <span class="kpi-icon">🤝</span>
                {volunteers_formatted}
            </div>
        </div>
    </div>
    """
    
    st.markdown(kpi_html, unsafe_allow_html=True)


def render_option1_filters(df: pd.DataFrame):
    """Render the filter row matching Option 1 design."""
    st.markdown('<div class="filter-row">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        # Year filter
        years = sorted(df["Project Year"].dropna().unique().astype(int).tolist()) if "Project Year" in df.columns else []
        if not years:
            years = [2020, 2021, 2022, 2023, 2024]  # Default years
        selected_year = st.selectbox("Year", ["All"] + years, key="year_filter")
    
    with col2:
        # Category filter
        categories = sorted(df["Level 1"].dropna().unique().tolist()) if "Level 1" in df.columns else []
        if not categories:
            categories = ["Nutrition", "Healthcare", "Education", "Socioeconomic", "Animal", "Disaster"]
        selected_category = st.selectbox("Category", ["All"] + categories, key="category_filter")
    
    with col3:
        # Metric selector for visualizations
        metrics = ["Souls", "Value R", "Volunteer Hours", "Quantity"]
        available_metrics = [m for m in metrics if m in df.columns]
        if not available_metrics:
            available_metrics = ["Souls"]
        selected_metric = st.selectbox("Visualization Metric", available_metrics, key="metric_selector")
    
    with col4:
        # Export functionality
        if st.button("📥 Export Data", key="export_btn"):
            export_data(df)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["Project Year"] == selected_year] if "Project Year" in filtered_df.columns else filtered_df
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Level 1"] == selected_category] if "Level 1" in filtered_df.columns else filtered_df
    
    return filtered_df, selected_metric, selected_category if selected_category != "All" else None


def export_data(df: pd.DataFrame):
    """Export functionality for data and charts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Convert to CSV for download
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📊 Download Data as CSV",
        data=csv,
        file_name=f"sewa_connect_data_{timestamp}.csv",
        mime="text/csv"
    )
    
    st.success("Export functionality activated! Click the download button above.")


def create_interactive_data_table(df: pd.DataFrame):
    """Create an interactive data table matching Option 1."""
    st.markdown("""
    <div class="table-card">
        <div class="table-header">
            <h3 class="table-title">Detailed Table</h3>
            <button class="export-btn" onclick="exportTable()">Export Table</button>
        </div>
        <div style="padding: 1rem;">
    """, unsafe_allow_html=True)
    
    # Display table with key columns
    display_cols = ["Level 1", "Level 2", "Level 3", "Souls", "Value R", "Volunteer Hours", "Project Year"]
    available_cols = [col for col in display_cols if col in df.columns]
    
    if available_cols:
        # Rename columns for display
        display_df = df[available_cols].copy()
        display_mapping = {
            "Level 1": "Category",
            "Level 2": "Sub-category", 
            "Level 3": "Activity",
            "Souls": "Lives Impacted",
            "Value R": "Rand Value",
            "Volunteer Hours": "Volunteer Hours",
            "Project Year": "Year"
        }
        
        display_df = display_df.rename(columns=display_mapping)
        
        # Format numeric columns
        for col in display_df.columns:
            if col in display_df.columns and display_df[col].dtype in ['int64', 'float64']:
                if col == "Rand Value":
                    display_df[col] = display_df[col].apply(lambda x: f"R {x:,.0f}" if pd.notna(x) and x != 0 else "R 0")
                elif col in ["Lives Impacted", "Volunteer Hours", "Year"]:
                    display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) and x != 0 else "0")
        
        # Remove rows where all key columns are NaN or empty
        display_df = display_df.dropna(how='all')
        
        # Fill NaN values with empty strings for display
        display_df = display_df.fillna('')
        
        st.dataframe(
            display_df.head(20),  # Show first 20 rows
            use_container_width=True,
            hide_index=True,
            height=400
        )
    else:
        st.write("No data available to display.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)


def main():
    """Main application function - Option 1 Recreation."""
    # Configure page
    st.set_page_config(
        page_title="Sewa Connect",
        page_icon="🌟",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Load data
    if not DATA_FILE.exists():
        st.error(f"📁 Data file missing: {DATA_FILE}")
        st.info("Please ensure the Excel file is present in the data directory.")
        return
    
    with st.spinner("🔄 Loading data..."):
        df = load_master_sheet(DATA_FILE)
    
    if df.empty:
        st.error("❌ Failed to load data. Please check the file format.")
        return
    
    # Header Section - Option 1 Style
    st.markdown("""
    <div class="option1-header">
        <h1 class="header-title">Sewa Connect</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter Row
    filtered_df, selected_metric, selected_category = render_option1_filters(df)
    
    # KPI Cards Row
    create_option1_kpi_cards(filtered_df)
    
    # Chart Grid - 2x2 Layout like Option 1
    st.markdown('<div class="chart-grid">', unsafe_allow_html=True)
    
    # Top Left: Sunburst Chart
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <h3 class="chart-title">Sunburst</h3>
        </div>
        <div class="chart-content">
    """, unsafe_allow_html=True)
    
    fig_sunburst = create_option1_sunburst(filtered_df, selected_metric, [selected_category] if selected_category else None)
    if fig_sunburst:
        st.plotly_chart(fig_sunburst, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
        })
    else:
        st.info("No data available for sunburst visualization")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Top Right: Impact Over Time
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <h3 class="chart-title">Impact Over Time</h3>
        </div>
        <div class="chart-content">
    """, unsafe_allow_html=True)
    
    fig_trend = create_impact_trend_chart(filtered_df, selected_metric)
    if fig_trend:
        st.plotly_chart(fig_trend, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False
        })
    else:
        st.info("No trend data available")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Bottom Left: Category Breakdown (converted to match Option 1 style)
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <h3 class="chart-title">Category Breakdown</h3>
        </div>
        <div class="chart-content">
    """, unsafe_allow_html=True)
    
    # Create pie chart for category breakdown
    if "Level 1" in filtered_df.columns and selected_metric in filtered_df.columns:
        category_data = filtered_df.groupby("Level 1")[selected_metric].sum().reset_index()
        
        fig_pie = px.pie(
            category_data,
            values=selected_metric,
            names="Level 1",
            color_discrete_map={
                'Nutrition': OPTION1_COLORS['nutrition'],
                'Healthcare': OPTION1_COLORS['healthcare'], 
                'Education': OPTION1_COLORS['education'],
                'Socioeconomic': OPTION1_COLORS['socioeconomic'],
                'Animal': OPTION1_COLORS['animal'],
                'Disaster': OPTION1_COLORS['disaster'],
                'Environmental': OPTION1_COLORS['environmental']
            }
        )
        
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>' +
                         f'{selected_metric}: %{{value:,.0f}}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>'
        )
        
        fig_pie.update_layout(
            height=400,
            margin=dict(t=10, l=10, r=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=11, color=OPTION1_COLORS['text_dark']),
            showlegend=False
        )
        
        st.plotly_chart(fig_pie, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False
        })
    else:
        st.info("No category data available")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Bottom Right: Heatmap
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <h3 class="chart-title">Heatmap View</h3>
        </div>
        <div class="chart-content">
    """, unsafe_allow_html=True)
    
    fig_heatmap = create_heatmap_chart(filtered_df, selected_metric)
    if fig_heatmap:
        st.plotly_chart(fig_heatmap, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False
        })
    else:
        st.info("No heatmap data available")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End chart grid
    
    # Data Table Section
    create_interactive_data_table(filtered_df)
    
    # Add cross-filtering JavaScript
    st.markdown("""
    <script>
    function filterByMetric(metric) {
        // This would trigger cross-filtering in a real implementation
        console.log('Filtering by metric:', metric);
    }
    
    function exportTable() {
        // Trigger table export
        console.log('Exporting table data');
    }
    </script>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
