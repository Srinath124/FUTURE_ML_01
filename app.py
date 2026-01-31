import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

# Page configuration
st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, premium styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Header styling */
    h1, h2, h3 {
        background: linear-gradient(120deg, #00f5ff 0%, #00d4ff 50%, #0099ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(0, 245, 255, 0.2);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00f5ff;
    }
    
    /* Metric cards with glassmorphism */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(120deg, #00f5ff 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 0.85rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(120deg, #00f5ff 0%, #0099ff 100%);
        color: #0f0c29;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 245, 255, 0.5);
        background: linear-gradient(120deg, #00d4ff 0%, #0077ff 100%);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(120deg, #00f5ff 0%, #0099ff 100%);
        color: #0f0c29;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 245, 255, 0.5);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.02);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #b0b0b0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, rgba(0, 245, 255, 0.2) 0%, rgba(0, 153, 255, 0.2) 100%);
        border-color: rgba(0, 245, 255, 0.5);
        color: #00f5ff;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 245, 255, 0.1);
        border-color: rgba(0, 245, 255, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(0, 245, 255, 0.2);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 245, 255, 0.1);
        border-color: rgba(0, 245, 255, 0.4);
    }
    
    /* Divider */
    hr {
        border-color: rgba(0, 245, 255, 0.2);
        margin: 2rem 0;
    }
    
    /* Custom animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
@st.cache_data
def load_data():
    """Load all necessary data files"""
    data_dir = Path(__file__).parent / 'data'
    outputs_dir = Path(__file__).parent / 'outputs'
    
    # Load processed data
    daily_simple = pd.read_csv(data_dir / 'processed' / 'daily_sales_simple.csv', parse_dates=['Order Date'])
    daily_features = pd.read_csv(data_dir / 'processed' / 'daily_sales_features.csv', parse_dates=['Order Date'])
    
    # Load forecasts from outputs directory
    forecasts = {}
    forecast_dir = outputs_dir / 'forecasts'
    
    # Load 90-day forecast
    if (forecast_dir / '90day_forecast.csv').exists():
        forecasts['90day'] = pd.read_csv(forecast_dir / '90day_forecast.csv', parse_dates=['Date'])
    
    # Load category forecast
    if (forecast_dir / 'category_forecast.csv').exists():
        forecasts['category'] = pd.read_csv(forecast_dir / 'category_forecast.csv')
    
    # Load monthly forecast
    if (forecast_dir / 'monthly_forecast.csv').exists():
        forecasts['monthly'] = pd.read_csv(forecast_dir / 'monthly_forecast.csv')
    
    return daily_simple, daily_features, forecasts

def create_plotly_theme():
    """Create consistent Plotly theme"""
    return {
        'paper_bgcolor': 'rgba(26, 26, 46, 0.8)',
        'plot_bgcolor': 'rgba(26, 26, 46, 0.5)',
        'font': {'color': '#ffffff', 'family': 'Inter'},
        'xaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'zerolinecolor': 'rgba(255, 255, 255, 0.2)'
        },
        'yaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'zerolinecolor': 'rgba(255, 255, 255, 0.2)'
        }
    }

# Main app
def main():
    # Header
    st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)
    st.title("📊 Sales Forecasting Dashboard")
    st.markdown("### Advanced Analytics & Future Predictions")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load data
    try:
        daily_simple, daily_features, forecasts = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure all data files are in the correct location.")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Dashboard Controls")
        st.markdown("---")
        
        # Forecast period selector
        st.markdown("### Forecast Period")
        forecast_options = ['90day', '30day', '60day']
        available_forecasts = [f for f in forecast_options if f in forecasts or f == '90day']
        
        if available_forecasts:
            selected_forecast = st.selectbox(
                "Select forecast horizon",
                available_forecasts,
                format_func=lambda x: f"{x.replace('day', ' Days')}"
            )
        else:
            st.warning("No forecast data available")
            selected_forecast = None
        
        st.markdown("---")
        
        # Date range filter
        st.markdown("### Historical Data Range")
        min_date = daily_simple['Order Date'].min()
        max_date = daily_simple['Order Date'].max()
        
        date_range = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        st.markdown("---")
        
        # Info section
        st.markdown("### 📈 About")
        st.info(
            "This dashboard provides comprehensive sales forecasting "
            "analytics using machine learning models trained on historical data."
        )
        
        st.markdown("### 🔍 Data Summary")
        st.metric("Total Records", f"{len(daily_simple):,}")
        st.metric("Date Range", f"{(max_date - min_date).days} days")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🔮 Forecasts", 
        "📈 Trends & Patterns",
        "💡 Insights"
    ])
    
    with tab1:
        st.markdown("## Sales Overview")
        
        # Filter data by date range
        if len(date_range) == 2:
            filtered_data = daily_simple[
                (daily_simple['Order Date'] >= pd.Timestamp(date_range[0])) &
                (daily_simple['Order Date'] <= pd.Timestamp(date_range[1]))
            ]
        else:
            filtered_data = daily_simple
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sales = filtered_data['Sales'].sum()
            st.metric(
                "Total Sales",
                f"${total_sales:,.0f}",
                delta=f"{len(filtered_data)} days"
            )
        
        with col2:
            avg_daily_sales = filtered_data['Sales'].mean()
            st.metric(
                "Avg Daily Sales",
                f"${avg_daily_sales:,.0f}",
                delta=f"{(avg_daily_sales / filtered_data['Sales'].median() - 1) * 100:.1f}% vs median"
            )
        
        with col3:
            max_sales = filtered_data['Sales'].max()
            st.metric(
                "Peak Sales Day",
                f"${max_sales:,.0f}",
                delta=filtered_data.loc[filtered_data['Sales'].idxmax(), 'Order Date'].strftime('%Y-%m-%d')
            )
        
        with col4:
            std_sales = filtered_data['Sales'].std()
            st.metric(
                "Volatility (Std Dev)",
                f"${std_sales:,.0f}",
                delta=f"{(std_sales / avg_daily_sales) * 100:.1f}% CV"
            )
        
        st.markdown("---")
        
        # Interactive sales trend chart with Plotly
        st.markdown("### 📈 Historical Sales Trend")
        
        fig = go.Figure()
        
        # Add main sales line
        fig.add_trace(go.Scatter(
            x=filtered_data['Order Date'],
            y=filtered_data['Sales'],
            mode='lines',
            name='Daily Sales',
            line=dict(color='#00f5ff', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 245, 255, 0.2)',
            hovertemplate='<b>Date:</b> %{x}<br><b>Sales:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # Add 7-day moving average
        filtered_data_copy = filtered_data.copy()
        filtered_data_copy['MA7'] = filtered_data_copy['Sales'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=filtered_data_copy['Order Date'],
            y=filtered_data_copy['MA7'],
            mode='lines',
            name='7-Day MA',
            line=dict(color='#ff6b6b', width=2, dash='dash'),
            hovertemplate='<b>Date:</b> %{x}<br><b>7-Day MA:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # Add 30-day moving average
        filtered_data_copy['MA30'] = filtered_data_copy['Sales'].rolling(window=30).mean()
        fig.add_trace(go.Scatter(
            x=filtered_data_copy['Order Date'],
            y=filtered_data_copy['MA30'],
            mode='lines',
            name='30-Day MA',
            line=dict(color='#4ecdc4', width=2, dash='dot'),
            hovertemplate='<b>Date:</b> %{x}<br><b>30-Day MA:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            **create_plotly_theme(),
            title='Daily Sales Over Time with Moving Averages',
            xaxis_title='Date',
            yaxis_title='Sales ($)',
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional metrics row
        st.markdown("### 📊 Performance Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            growth_rate = ((filtered_data['Sales'].iloc[-30:].mean() / filtered_data['Sales'].iloc[:30].mean()) - 1) * 100 if len(filtered_data) >= 60 else 0
            st.metric("30-Day Growth Rate", f"{growth_rate:+.2f}%")
        
        with col2:
            best_month = filtered_data.groupby(filtered_data['Order Date'].dt.to_period('M'))['Sales'].sum().idxmax()
            st.metric("Best Month", str(best_month))
        
        with col3:
            total_days = len(filtered_data)
            profitable_days = len(filtered_data[filtered_data['Sales'] > avg_daily_sales])
            st.metric("Above Average Days", f"{profitable_days}/{total_days}", delta=f"{(profitable_days/total_days)*100:.1f}%")
    
    with tab2:
        st.markdown("## 🔮 Sales Forecasts")
        
        # Create sub-tabs for different forecast types
        forecast_tab1, forecast_tab2, forecast_tab3 = st.tabs([
            "📅 90-Day Forecast",
            "🏷️ Category Breakdown",
            "📆 Monthly Forecast"
        ])
        
        with forecast_tab1:
            if '90day' in forecasts:
                forecast_df = forecasts['90day']
                
                # Forecast metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    forecast_total = forecast_df['Predicted_Sales'].sum()
                    st.metric(
                        "Forecasted Total",
                        f"${forecast_total:,.0f}",
                        delta="90 days"
                    )
                
                with col2:
                    forecast_avg = forecast_df['Predicted_Sales'].mean()
                    avg_daily_sales = daily_simple['Sales'].mean()
                    st.metric(
                        "Avg Daily Forecast",
                        f"${forecast_avg:,.0f}",
                        delta=f"{(forecast_avg / avg_daily_sales - 1) * 100:+.1f}% vs historical"
                    )
                
                with col3:
                    forecast_peak = forecast_df['Predicted_Sales'].max()
                    st.metric(
                        "Peak Forecast Day",
                        f"${forecast_peak:,.0f}",
                        delta=forecast_df.loc[forecast_df['Predicted_Sales'].idxmax(), 'Date'].strftime('%Y-%m-%d')
                    )
                
                with col4:
                    forecast_min = forecast_df['Predicted_Sales'].min()
                    st.metric(
                        "Min Forecast Day",
                        f"${forecast_min:,.0f}",
                        delta=f"Range: ${forecast_peak - forecast_min:,.0f}"
                    )
                
                st.markdown("---")
                
                # Interactive forecast visualization
                st.markdown("### 📊 90-Day Forecast Visualization")
                
                fig = go.Figure()
                
                # Plot historical (last 90 days)
                recent_data = daily_simple.tail(90)
                fig.add_trace(go.Scatter(
                    x=recent_data['Order Date'],
                    y=recent_data['Sales'],
                    mode='lines',
                    name='Historical',
                    line=dict(color='#00f5ff', width=2),
                    hovertemplate='<b>Date:</b> %{x}<br><b>Sales:</b> $%{y:,.2f}<extra></extra>'
                ))
                
                # Plot forecast
                fig.add_trace(go.Scatter(
                    x=forecast_df['Date'],
                    y=forecast_df['Predicted_Sales'],
                    mode='lines',
                    name='Forecast',
                    line=dict(color='#ff6b6b', width=2, dash='dash'),
                    hovertemplate='<b>Date:</b> %{x}<br><b>Forecast:</b> $%{y:,.2f}<extra></extra>'
                ))
                
                # Add confidence interval if available
                if 'Lower_Bound' in forecast_df.columns and 'Upper_Bound' in forecast_df.columns:
                    fig.add_trace(go.Scatter(
                        x=forecast_df['Date'],
                        y=forecast_df['Upper_Bound'],
                        mode='lines',
                        name='Upper Bound',
                        line=dict(width=0),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    fig.add_trace(go.Scatter(
                        x=forecast_df['Date'],
                        y=forecast_df['Lower_Bound'],
                        mode='lines',
                        name='Confidence Interval',
                        line=dict(width=0),
                        fillcolor='rgba(255, 107, 107, 0.2)',
                        fill='tonexty',
                        hovertemplate='<b>Range:</b> $%{y:,.2f}<extra></extra>'
                    ))
                
                fig.update_layout(
                    **create_plotly_theme(),
                    title='90-Day Sales Forecast',
                    xaxis_title='Date',
                    yaxis_title='Sales ($)',
                    hovermode='x unified',
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Download button
                csv = forecast_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download 90-Day Forecast",
                    data=csv,
                    file_name="90day_forecast.csv",
                    mime="text/csv"
                )
                
                # Forecast data table
                with st.expander("📋 View Detailed Forecast Data"):
                    st.dataframe(
                        forecast_df.style.format({
                            'Predicted_Sales': '${:,.2f}'
                        }),
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ No 90-day forecast data available.")
                st.info("Run notebooks/03_forecasting_models.ipynb to generate forecasts.")
        
        with forecast_tab2:
            if 'category' in forecasts:
                category_df = forecasts['category']
                
                st.markdown("### 🏷️ Category-wise Forecast Breakdown")
                
                # Display metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    # Pie chart
                    fig = go.Figure(data=[go.Pie(
                        labels=category_df['Category'],
                        values=category_df['Total Forecast'],
                        hole=0.4,
                        marker=dict(colors=['#00f5ff', '#ff6b6b', '#4ecdc4']),
                        hovertemplate='<b>%{label}</b><br>Forecast: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
                    )])
                    
                    fig.update_layout(
                        **create_plotly_theme(),
                        title='Forecast Distribution by Category',
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Bar chart
                    fig = go.Figure(data=[go.Bar(
                        x=category_df['Category'],
                        y=category_df['Total Forecast'],
                        marker=dict(
                            color=category_df['Total Forecast'],
                            colorscale='Turbo',
                            showscale=True
                        ),
                        hovertemplate='<b>%{x}</b><br>Total Forecast: $%{y:,.2f}<extra></extra>'
                    )])
                    
                    fig.update_layout(
                        **create_plotly_theme(),
                        title='Total Forecast by Category',
                        xaxis_title='Category',
                        yaxis_title='Total Forecast ($)',
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Category metrics
                st.markdown("### 📊 Category Performance Metrics")
                
                cols = st.columns(len(category_df))
                for idx, (_, row) in enumerate(category_df.iterrows()):
                    with cols[idx]:
                        st.metric(
                            row['Category'],
                            f"${row['Total Forecast']:,.0f}",
                            delta=f"{row['Proportion']:.1f}%"
                        )
                
                # Download button
                csv = category_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Category Forecast",
                    data=csv,
                    file_name="category_forecast.csv",
                    mime="text/csv"
                )
                
                # Detailed table
                with st.expander("📋 View Detailed Category Data"):
                    st.dataframe(
                        category_df.style.format({
                            'Total Forecast': '${:,.2f}',
                            'Avg Daily Sales': '${:,.2f}',
                            'Proportion': '{:.2f}%'
                        }),
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ No category forecast data available.")
                st.info("Run notebooks/04_category_forecasting.ipynb to generate category forecasts.")
        
        with forecast_tab3:
            if 'monthly' in forecasts:
                monthly_df = forecasts['monthly']
                
                st.markdown("### 📆 Monthly Forecast Overview")
                
                # Monthly metrics
                cols = st.columns(len(monthly_df))
                for idx, (_, row) in enumerate(monthly_df.iterrows()):
                    with cols[idx]:
                        st.metric(
                            row['Month'],
                            f"${row['Predicted Sales']:,.0f}",
                            delta=f"{row['Days']} days"
                        )
                
                st.markdown("---")
                
                # Interactive bar chart
                fig = go.Figure(data=[go.Bar(
                    x=monthly_df['Month'],
                    y=monthly_df['Predicted Sales'],
                    marker=dict(
                        color=monthly_df['Predicted Sales'],
                        colorscale='Blues',
                        showscale=True,
                        colorbar=dict(title="Sales ($)")
                    ),
                    text=monthly_df['Predicted Sales'].apply(lambda x: f'${x:,.0f}'),
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Predicted Sales: $%{y:,.2f}<br>Days: %{customdata}<extra></extra>',
                    customdata=monthly_df['Days']
                )])
                
                fig.update_layout(
                    **create_plotly_theme(),
                    title='Monthly Sales Forecast',
                    xaxis_title='Month',
                    yaxis_title='Predicted Sales ($)',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Average daily sales comparison
                st.markdown("### 📊 Average Daily Sales by Month")
                
                fig = go.Figure(data=[go.Bar(
                    x=monthly_df['Month'],
                    y=monthly_df['Avg Daily Sales'],
                    marker=dict(color='#00f5ff'),
                    text=monthly_df['Avg Daily Sales'].apply(lambda x: f'${x:,.0f}'),
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Avg Daily Sales: $%{y:,.2f}<extra></extra>'
                )])
                
                fig.update_layout(
                    **create_plotly_theme(),
                    title='Average Daily Sales Forecast by Month',
                    xaxis_title='Month',
                    yaxis_title='Avg Daily Sales ($)',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Download button
                csv = monthly_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Monthly Forecast",
                    data=csv,
                    file_name="monthly_forecast.csv",
                    mime="text/csv"
                )
                
                # Detailed table
                with st.expander("📋 View Detailed Monthly Data"):
                    st.dataframe(
                        monthly_df.style.format({
                            'Predicted Sales': '${:,.2f}',
                            'Avg Daily Sales': '${:,.2f}'
                        }),
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ No monthly forecast data available.")
                st.info("Run notebooks/05_monthly_forecasting.ipynb to generate monthly forecasts.")
    
    with tab3:
        st.markdown("## 📈 Trends & Patterns")
        
        # Monthly aggregation
        st.markdown("### 📅 Monthly Sales Trend")
        monthly_data = daily_simple.copy()
        monthly_data['Month'] = monthly_data['Order Date'].dt.to_period('M')
        monthly_sales = monthly_data.groupby('Month')['Sales'].sum().reset_index()
        monthly_sales['Month'] = monthly_sales['Month'].astype(str)
        
        fig = go.Figure(data=[go.Bar(
            x=monthly_sales['Month'],
            y=monthly_sales['Sales'],
            marker=dict(
                color=monthly_sales['Sales'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Sales ($)")
            ),
            text=monthly_sales['Sales'].apply(lambda x: f'${x/1000:.0f}K'),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Total Sales: $%{y:,.2f}<extra></extra>'
        )])
        
        fig.update_layout(
            **create_plotly_theme(),
            title='Monthly Sales Performance',
            xaxis_title='Month',
            yaxis_title='Sales ($)',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Day of week analysis
        st.markdown("### 📊 Day of Week Analysis")
        
        daily_simple_copy = daily_simple.copy()
        daily_simple_copy['DayOfWeek'] = daily_simple_copy['Order Date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_sales = daily_simple_copy.groupby('DayOfWeek')['Sales'].agg(['mean', 'sum', 'count']).reindex(day_order)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[go.Bar(
                x=dow_sales.index,
                y=dow_sales['mean'],
                marker=dict(color='#00f5ff'),
                text=dow_sales['mean'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Avg Sales: $%{y:,.2f}<extra></extra>'
            )])
            
            fig.update_layout(
                **create_plotly_theme(),
                title='Average Sales by Day of Week',
                xaxis_title='Day',
                yaxis_title='Average Sales ($)',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(data=[go.Bar(
                x=dow_sales.index,
                y=dow_sales['sum'],
                marker=dict(color='#ff6b6b'),
                text=dow_sales['sum'].apply(lambda x: f'${x/1000:.0f}K'),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Total Sales: $%{y:,.2f}<extra></extra>'
            )])
            
            fig.update_layout(
                **create_plotly_theme(),
                title='Total Sales by Day of Week',
                xaxis_title='Day',
                yaxis_title='Total Sales ($)',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Distribution analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Sales Distribution")
            
            fig = go.Figure(data=[go.Histogram(
                x=daily_simple['Sales'],
                nbinsx=50,
                marker=dict(color='#00f5ff', line=dict(color='white', width=1)),
                hovertemplate='Sales Range: $%{x}<br>Count: %{y}<extra></extra>'
            )])
            
            fig.update_layout(
                **create_plotly_theme(),
                title='Sales Distribution',
                xaxis_title='Sales ($)',
                yaxis_title='Frequency',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Sales Statistics")
            stats_df = pd.DataFrame({
                'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Q1', 'Q3'],
                'Value': [
                    f"${daily_simple['Sales'].mean():,.2f}",
                    f"${daily_simple['Sales'].median():,.2f}",
                    f"${daily_simple['Sales'].std():,.2f}",
                    f"${daily_simple['Sales'].min():,.2f}",
                    f"${daily_simple['Sales'].max():,.2f}",
                    f"${daily_simple['Sales'].quantile(0.25):,.2f}",
                    f"${daily_simple['Sales'].quantile(0.75):,.2f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True, height=320)
        
        st.markdown("---")
        
        # Quarterly analysis
        st.markdown("### 📊 Quarterly Performance")
        
        quarterly_data = daily_simple.copy()
        quarterly_data['Quarter'] = quarterly_data['Order Date'].dt.to_period('Q')
        quarterly_sales = quarterly_data.groupby('Quarter')['Sales'].agg(['sum', 'mean', 'count']).reset_index()
        quarterly_sales['Quarter'] = quarterly_sales['Quarter'].astype(str)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Total Sales by Quarter', 'Average Daily Sales by Quarter')
        )
        
        fig.add_trace(
            go.Bar(
                x=quarterly_sales['Quarter'],
                y=quarterly_sales['sum'],
                marker=dict(color='#4ecdc4'),
                name='Total Sales',
                hovertemplate='<b>%{x}</b><br>Total: $%{y:,.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=quarterly_sales['Quarter'],
                y=quarterly_sales['mean'],
                marker=dict(color='#ff6b6b'),
                name='Avg Daily Sales',
                hovertemplate='<b>%{x}</b><br>Average: $%{y:,.2f}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            **create_plotly_theme(),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("## 💡 Business Insights")
        
        # Key insights
        st.markdown("### 🎯 Key Findings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("**📈 Growth Trends**")
            st.markdown("""
            - Historical average daily sales: **${:,.0f}**
            - Peak sales day: **${:,.0f}**
            - Sales volatility: **{:.1f}%**
            - Total revenue: **${:,.0f}**
            """.format(
                daily_simple['Sales'].mean(),
                daily_simple['Sales'].max(),
                (daily_simple['Sales'].std() / daily_simple['Sales'].mean()) * 100,
                daily_simple['Sales'].sum()
            ))
        
        with col2:
            st.info("**🔮 Forecast Insights**")
            if '90day' in forecasts:
                forecast_df = forecasts['90day']
                st.markdown("""
                - Forecasted average: **${:,.0f}**
                - Expected peak: **${:,.0f}**
                - Forecast horizon: **90 days**
                - Total forecast: **${:,.0f}**
                """.format(
                    forecast_df['Predicted_Sales'].mean(),
                    forecast_df['Predicted_Sales'].max(),
                    forecast_df['Predicted_Sales'].sum()
                ))
            else:
                st.markdown("*Run forecasting models to see predictions*")
        
        st.markdown("---")
        
        # Comparison visualization
        st.markdown("### 📊 Historical vs Forecast Comparison")
        
        if '90day' in forecasts:
            col1, col2, col3 = st.columns(3)
            
            forecast_df = forecasts['90day']
            historical_avg = daily_simple['Sales'].mean()
            forecast_avg = forecast_df['Predicted_Sales'].mean()
            difference = forecast_avg - historical_avg
            percent_change = (difference / historical_avg) * 100
            
            with col1:
                st.metric(
                    "Historical Avg",
                    f"${historical_avg:,.0f}",
                    delta="Baseline"
                )
            
            with col2:
                st.metric(
                    "Forecast Avg",
                    f"${forecast_avg:,.0f}",
                    delta=f"{percent_change:+.1f}%"
                )
            
            with col3:
                st.metric(
                    "Difference",
                    f"${abs(difference):,.0f}",
                    delta="Higher" if difference > 0 else "Lower"
                )
            
            # Comparison chart
            comparison_data = pd.DataFrame({
                'Category': ['Historical Average', 'Forecast Average'],
                'Value': [historical_avg, forecast_avg]
            })
            
            fig = go.Figure(data=[go.Bar(
                x=comparison_data['Category'],
                y=comparison_data['Value'],
                marker=dict(color=['#00f5ff', '#ff6b6b']),
                text=comparison_data['Value'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Value: $%{y:,.2f}<extra></extra>'
            )])
            
            fig.update_layout(
                **create_plotly_theme(),
                title='Historical vs Forecast Average Comparison',
                yaxis_title='Average Daily Sales ($)',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Category insights
        if 'category' in forecasts:
            st.markdown("### 🏷️ Category Performance Insights")
            
            category_df = forecasts['category']
            top_category = category_df.loc[category_df['Total Forecast'].idxmax()]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Top Category",
                    top_category['Category'],
                    delta=f"${top_category['Total Forecast']:,.0f}"
                )
            
            with col2:
                st.metric(
                    "Market Share",
                    f"{top_category['Proportion']:.1f}%",
                    delta="of total forecast"
                )
            
            with col3:
                st.metric(
                    "Daily Average",
                    f"${top_category['Avg Daily Sales']:,.0f}",
                    delta=f"{top_category['Category']}"
                )
        
        st.markdown("---")
        
        # Recommendations
        st.markdown("### 📋 Recommendations")
        
        st.warning("**⚠️ Action Items**")
        st.markdown("""
        1. **Inventory Planning**: Prepare for peak sales periods based on forecast
        2. **Resource Allocation**: Adjust staffing for high-demand days
        3. **Cash Flow Management**: Plan budget based on predicted revenue
        4. **Marketing Strategy**: Focus campaigns during forecasted growth periods
        5. **Category Focus**: Invest in top-performing categories
        """)
        
        st.markdown("---")
        
        # Model information
        with st.expander("🤖 Model Information"):
            st.markdown("""
            ### Forecasting Models Used
            
            - **Linear Regression**: Best performer (R² = 0.237)
            - **Random Forest**: Non-linear pattern detection
            - **ARIMA**: Time series statistical model
            - **SARIMA**: Seasonal time series model
            
            ### Data Features
            
            - Historical sales data
            - Time-based features (day, month, quarter)
            - Lag features (previous period sales)
            - Rolling statistics (moving averages)
            
            ### Evaluation Metrics
            
            - RMSE (Root Mean Square Error)
            - MAE (Mean Absolute Error)
            - MAPE (Mean Absolute Percentage Error)
            - R² Score
            """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #b0b0b0; padding: 2rem;'>"
        "📊 Sales Forecasting Dashboard | Built with Streamlit & Plotly | "
        "Data-driven insights for better business decisions"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
