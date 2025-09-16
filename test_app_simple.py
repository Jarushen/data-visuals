"""
Simple test version of the Sewa Connect dashboard to verify functionality.
"""

import pathlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

# Configuration
DATA_FILE = pathlib.Path(__file__).parent / "data" / "Master Data set v13 - Form - 20250731.xlsx"

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


def create_simple_sunburst(df: pd.DataFrame, metric: str) -> go.Figure:
    """Create a simple sunburst chart."""
    if metric not in df.columns:
        st.error(f"Metric '{metric}' not found in data columns: {df.columns.tolist()}")
        return None
        
    # Clean the data
    d = df.copy()
    d = d.dropna(subset=["Level 1", "Level 2", "Level 3"])
    d = d[d[metric].notna()]
    d = d[d[metric] > 0]
    
    # Remove rows where hierarchy levels are empty strings
    for col in ["Level 1", "Level 2", "Level 3"]:
        d = d[d[col].astype(str).str.strip() != '']
        d = d[d[col].astype(str) != 'None']
    
    if d.empty:
        st.warning(f"No valid data available for {metric} after filtering.")
        return None
    
    # Create hierarchical data structure
    grouped = d.groupby(["Level 1", "Level 2", "Level 3"])[metric].sum().reset_index()
    
    # Prepare labels, parents, and values for sunburst
    labels = []
    parents = []
    values = []
    
    # Level 1 (root level)
    level1_data = grouped.groupby("Level 1")[metric].sum().reset_index()
    for _, row in level1_data.iterrows():
        labels.append(row["Level 1"])
        parents.append("")
        values.append(row[metric])
    
    # Level 2 (children of Level 1)
    level2_data = grouped.groupby(["Level 1", "Level 2"])[metric].sum().reset_index()
    for _, row in level2_data.iterrows():
        label = f"{row['Level 1']} - {row['Level 2']}"
        labels.append(label)
        parents.append(row["Level 1"])
        values.append(row[metric])
    
    # Level 3 (children of Level 2)
    for _, row in grouped.iterrows():
        label = f"{row['Level 1']} - {row['Level 2']} - {row['Level 3']}"
        parent = f"{row['Level 1']} - {row['Level 2']}"
        labels.append(label)
        parents.append(parent)
        values.append(row[metric])
    
    # Create the figure
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>' +
                     f'{metric}: %{{value:,.0f}}<br>' +
                     '<extra></extra>',
        maxdepth=3
    ))
    
    fig.update_layout(
        title=f"{metric} Distribution",
        height=600,
        margin=dict(t=80, l=20, r=20, b=20)
    )
    
    return fig


def main():
    """Main application function."""
    st.set_page_config(
        page_title="Sewa Connect - Test Dashboard",
        page_icon="🌟",
        layout="wide"
    )
    
    st.title("🌟 Sewa Connect - Test Dashboard")
    st.markdown("Testing data loading and sunburst visualization")
    
    # Load data
    if not DATA_FILE.exists():
        st.error(f"📁 Data file missing: {DATA_FILE}")
        return
    
    with st.spinner("🔄 Loading data..."):
        df = load_master_sheet(DATA_FILE)
    
    if df.empty:
        st.error("❌ Failed to load data. Please check the file format.")
        return
    
    # Display data info
    st.success(f"✅ Data loaded successfully! Shape: {df.shape}")
    
    # Show columns
    st.subheader("📊 Data Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Columns:**")
        st.write(df.columns.tolist())
    
    with col2:
        st.write("**Data Types:**")
        st.write(df.dtypes)
    
    # Show sample data
    st.subheader("📋 Sample Data")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Metric selection
    st.subheader("🎯 Sunburst Visualization")
    available_metrics = [m for m in ["Quantity", "Volunteer Hours", "Value R", "Souls"] if m in df.columns]
    selected_metric = st.selectbox("Select metric for sunburst", available_metrics)
    
    if selected_metric:
        st.write(f"Creating sunburst for: **{selected_metric}**")
        
        # Show some stats
        metric_data = df[selected_metric].dropna()
        st.write(f"- Total values: {len(metric_data)}")
        st.write(f"- Sum: {metric_data.sum():,.0f}")
        st.write(f"- Range: {metric_data.min():,.0f} - {metric_data.max():,.0f}")
        
        # Create sunburst
        fig = create_simple_sunburst(df, selected_metric)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Sunburst chart created successfully!")
        else:
            st.error("❌ Failed to create sunburst chart")


if __name__ == "__main__":
    main()
