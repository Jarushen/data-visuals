# Sunburst Dashboard

This repository contains a Streamlit application that visualises data from
the **Master Data set v13 - Form - 20250731.xlsx** spreadsheet.  The
app cleans the **Master** sheet, then renders interactive charts
including sunburst diagrams, bar charts and line charts.  Filters in
the sidebar allow you to drill down by project year, province and
top‑level category.

## Directory Structure

```
streamlit_dashboard_repo/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # This overview
├── .gitignore             # Files to ignore in version control
├── .streamlit/
│   └── config.toml        # Optional custom Streamlit theme
└── data/
    └── Master Data set v13 - Form - 20250731.xlsx
```

## Getting Started

1. **Create a virtual environment** (recommended) and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   ```

2. **Install dependencies** from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:

   ```bash
   streamlit run app.py
   ```

The dashboard will open in your default web browser.  Use the sidebar
to filter the data and explore the sunburst and summary charts.

## Deployment

You can deploy this app on various platforms.  Two simple options are:

### Streamlit Community Cloud

1. Push this repository to GitHub (make sure the `data` folder and Excel
   file are included).
2. Go to <https://streamlit.io/cloud> and create a new app.
3. Select your GitHub repository, set the main file to `app.py`, and
   deploy.

### Hugging Face Spaces

1. Create a new Space and choose **Streamlit** as the runtime.
2. Upload the repository files (including the `data` folder and Excel
   file) or connect your GitHub repo.
3. The app will build and become available at your Space’s URL.

## Notes

* The Excel file must be present in the `data/` directory or the app
  will raise an error on start‑up.
* If you change the file name or location, update the `DATA_FILE`
  constant in `app.py` accordingly.
* The `.streamlit/config.toml` defines a light theme with a custom
  primary colour.  You can modify it to customise the appearance.