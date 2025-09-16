import streamlit as st
import pandas as pd
import pathlib

st.title("🔧 Test Dashboard")
st.write("Testing basic functionality...")

# Test data loading
DATA_FILE = pathlib.Path(__file__).parent / "data" / "Master Data set v13 - Form - 20250731.xlsx"

if st.button("Test Data Loading"):
    if DATA_FILE.exists():
        st.success(f"✅ Data file found: {DATA_FILE}")
        try:
            # Try to load a small sample
            df = pd.read_excel(DATA_FILE, sheet_name="Master", nrows=10)
            st.success("✅ Excel file loads successfully!")
            st.write("Sample data shape:", df.shape)
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"❌ Error loading Excel: {e}")
    else:
        st.error(f"❌ Data file not found: {DATA_FILE}")

st.write("If you see this, Streamlit is working!")
