# Sewa Connect - Interactive Impact Dashboard

A modern Streamlit dashboard inspired by professional impact visualization platforms like Sewa International's Connect dashboard. This application presents hierarchical data through interactive sunburst charts, allowing users to explore collective impact across different sectors and metrics.

## ✨ Features

- **🎯 Interactive Sunburst Visualization**: Modern, clickable sunburst charts with drill-down capability
- **📊 Real-time Filtering**: Dynamic filters for year, province, and category exploration
- **💫 Professional Design**: Modern UI/UX with gradient backgrounds and responsive layout
- **📈 Multi-metric Analysis**: Support for Quantity, Volunteer Hours, Value (R), and Souls metrics
- **📱 Responsive Layout**: Optimized for various screen sizes and devices
- **🚀 Ready for Deployment**: Configured for easy deployment on multiple platforms

## 🏗️ Directory Structure

```
data-visuals/
├── app.py                     # Original Streamlit application
├── app_enhanced.py           # ✨ Enhanced modern dashboard
├── requirements.txt          # Python dependencies
├── README.md                # This overview
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
├── context/                 # Design reference images
│   ├── Option 1.png
│   ├── Option 2.png
│   └── Option 3.png
└── data/
    └── Master Data set v13 - Form - 20250731.xlsx
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd data-visuals
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the enhanced dashboard**:
   ```bash
   streamlit run app_enhanced.py
   ```

The dashboard will open in your default web browser at `http://localhost:8501`.

## 🎨 Dashboard Features

### Interactive Sunburst Chart
- **Multi-level visualization**: Explore Level 1, Level 2, and Level 3 categories
- **Click-to-drill**: Click on any segment to focus on that category
- **Hover details**: Rich tooltips with values and percentages
- **Dynamic coloring**: Beautiful color schemes that adapt to your data

### Smart Filtering
- **📅 Year Filter**: Select specific project years
- **🌍 Province Filter**: Focus on particular geographical regions  
- **📊 Category Filter**: Drill down by Level 1 categories
- **Real-time Updates**: All visualizations update instantly

### KPI Dashboard
- **📈 Key Metrics**: Total projects, volunteer hours, value, and people reached
- **📊 Visual Cards**: Modern metric cards with icons and gradients
- **⚡ Live Updates**: Metrics update based on applied filters

## 🎯 Data Requirements

The application expects an Excel file with the following structure:

### Required Columns:
- `Level 1`: Top-level category (e.g., Health, Education)
- `Level 2`: Mid-level category  
- `Level 3`: Detailed category
- `Quantity`: Numeric metric
- `Volunteer Hours`: Numeric metric
- `Value R`: Monetary value in Rands
- `Souls`: Number of people reached
- `Project Year`: Year of the project
- `Province`: Geographical location

### Data Format:
- Headers should be in row 3 (0-indexed row 2)
- Data starts from row 4 (0-indexed row 3)
- Numeric columns will be automatically converted
- Text columns will be cleaned of whitespace

## 🚀 Deployment Options

### 1. Streamlit Community Cloud (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add enhanced Sewa Connect dashboard"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file to `app_enhanced.py`
   - Click "Deploy"

3. **Custom Domain** (Optional):
   - Configure custom domain in Streamlit Cloud settings
   - Example: `connect.yourdomain.com`

### 2. Heroku Deployment

1. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

2. **Add Procfile**:
   ```bash
   echo "web: streamlit run app_enhanced.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```

3. **Deploy**:
   ```bash
   git add Procfile
   git commit -m "Add Procfile for Heroku"
   git push heroku main
   ```

### 3. Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app_enhanced.py"]
   ```

2. **Build and run**:
   ```bash
   docker build -t sewa-connect .
   docker run -p 8501:8501 sewa-connect
   ```

## 🎨 Customization

### Color Schemes
The dashboard uses a modern gradient color palette. To customize:

1. **Edit CSS variables** in `app_enhanced.py`:
   ```python
   # Update the colors in the load_custom_css() function
   colors = ['#YOUR_COLOR_1', '#YOUR_COLOR_2', ...]
   ```

2. **Update theme** in `.streamlit/config.toml`:
   ```toml
   [theme]
   primaryColor = "#YOUR_PRIMARY_COLOR"
   backgroundColor = "#YOUR_BACKGROUND_COLOR"
   ```

### Layout Modifications
- **Metrics**: Modify the `metrics_config` in `render_kpi_dashboard()`
- **Filters**: Customize filters in the `render_filters()` function
- **Charts**: Enhance visualizations in `create_modern_sunburst()`

## 📊 Data Processing

The application includes robust data processing:

- **Automatic cleaning**: Removes invalid columns and handles missing data
- **Type conversion**: Converts numeric columns appropriately
- **Error handling**: Graceful error handling for data issues
- **Caching**: Uses Streamlit's caching for optimal performance

## 🔧 Troubleshooting

### Common Issues

1. **File not found error**:
   - Ensure the Excel file is in the `data/` directory
   - Check file name matches exactly: `Master Data set v13 - Form - 20250731.xlsx`

2. **Missing columns error**:
   - Verify your Excel file has the required column structure
   - Check that headers are in the correct row (row 3)

3. **Performance issues**:
   - Large datasets may require optimization
   - Consider data sampling for very large files

### Getting Help

- **Issues**: Open an issue on GitHub
- **Features**: Request features via GitHub issues
- **Documentation**: Check this README and code comments

## 🌟 Inspiration

This dashboard is inspired by professional impact visualization platforms, particularly:
- **Sewa International Connect Dashboard**: Modern sunburst visualizations
- **Professional Analytics Platforms**: Interactive drill-down capabilities
- **Modern Web Design**: Gradient backgrounds and clean UI/UX

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit & Plotly** | *Empowering Impact Through Data Visualization*