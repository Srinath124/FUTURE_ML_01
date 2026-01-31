import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

def plot_forecast(historical, forecast, title=None, save_path=None, actuals=None):
    plt.figure(figsize=(14, 7))
    
    # Plot historical data
    if historical is not None:
        idx = historical.index if hasattr(historical, 'index') else np.arange(len(historical))
        plt.plot(idx, historical, label='Historical', color='gray', alpha=0.5)
    
    # Plot forecast
    if forecast is not None:
        idx = forecast.index if hasattr(forecast, 'index') else np.arange(len(forecast))
        if historical is not None and hasattr(historical, 'index') and not hasattr(forecast, 'index'):
             # Try to align if forecast follows historical
             pass 
        plt.plot(idx, forecast, label='Forecast', color='blue', linewidth=2)
    
    if actuals is not None:
        idx = actuals.index if hasattr(actuals, 'index') else np.arange(len(actuals))
        plt.plot(idx, actuals, label='Actual', color='green', linestyle='--')

    if title:
        plt.title(title, fontsize=16)
        
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            plt.savefig(save_path)
            print(f"Saved plot to {save_path}")
        except Exception as e:
            print(f"Error saving plot: {e}")
    
    plt.show()

def plot_error_analysis(y_true, y_pred, title=None, save_path=None):
    # Ensure y_pred is array/series
    if not isinstance(y_pred, pd.Series):
        if hasattr(y_true, 'index'):
             y_pred = pd.Series(y_pred, index=y_true.index)
        else:
             y_pred = np.array(y_pred)
    
    residuals = y_true - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Residuals over time
    if hasattr(residuals, 'index'):
        axes[0].plot(residuals.index, residuals)
        axes[0].set_xlabel('Date')
    else:
        axes[0].plot(residuals)
        axes[0].set_xlabel('Index')
        
    axes[0].axhline(y=0, color='r', linestyle='--')
    axes[0].set_title('Residuals over Time')
    axes[0].set_ylabel('Residual')
    
    # Residual distribution
    sns.histplot(residuals, kde=True, ax=axes[1])
    axes[1].set_title('Residual Distribution')
    
    if title:
        plt.suptitle(title, fontsize=16)
        
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            plt.savefig(save_path)
            print(f"Saved plot to {save_path}")
        except Exception as e:
            print(f"Error saving plot: {e}")
        
    plt.show()

def plot_model_comparison(df, metric='RMSE', title=None, save_path=None):
    plt.figure(figsize=(10, 6))
    
    if metric in df.columns:
        sns.barplot(x=df.index, y=df[metric], palette="viridis")
        if title:
            plt.title(title, fontsize=16)
        else:
            plt.title(f"Model Comparison - {metric} (Lower is Better)", fontsize=16)
        plt.ylabel(metric)
        plt.xlabel("Model")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            try:
                plt.savefig(save_path)
                print(f"Saved plot to {save_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")
            
        plt.show()
    else:
        print(f"Column {metric} not found in model comparison data.")

def create_dashboard(historical, forecast, actuals=None, comparison_df=None, save_path=None):
    """
    Creates a summary dashboard of the forecasting results.
    """
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 2)
    
    # 1. Main Forecast Plot
    ax1 = fig.add_subplot(gs[0, :])
    if historical is not None:
        idx = historical.index if hasattr(historical, 'index') else np.arange(len(historical))
        ax1.plot(idx, historical, label='Historical', color='gray', alpha=0.5)
    
    if forecast is not None:
        idx = forecast.index if hasattr(forecast, 'index') else np.arange(len(forecast))
        ax1.plot(idx, forecast, label='Forecast', color='blue', linewidth=2)
        
    if actuals is not None:
        idx = actuals.index if hasattr(actuals, 'index') else np.arange(len(actuals))
        ax1.plot(idx, actuals, label='Actual', color='green', linestyle='--')
        
    ax1.set_title('Sales Forecast Overview', fontsize=14)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sales')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 2. Model Comparison (if metrics provided)
    if comparison_df is not None:
        ax2 = fig.add_subplot(gs[1, 0])
        # Check for RMSE or similar metric
        metric = 'RMSE' if 'RMSE' in comparison_df.columns else comparison_df.columns[0]
        if metric in comparison_df.columns:
            sns.barplot(x=comparison_df.index, y=comparison_df[metric], ax=ax2, palette="viridis")
            ax2.set_title(f"Model Comparison - {metric}", fontsize=12)
            ax2.tick_params(axis='x', rotation=45)
    
    # 3. Forecast Distribution or Error (Placeholder for now)
    ax3 = fig.add_subplot(gs[1, 1])
    if forecast is not None:
        sns.histplot(forecast, kde=True, ax=ax3, color='blue')
        ax3.set_title('Forecast Distribution', fontsize=12)
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            plt.savefig(save_path)
            print(f"Saved dashboard to {save_path}")
        except Exception as e:
            print(f"Error saving dashboard: {e}")
            
    plt.show()

def plot_forecast_comparison(historical, forecasts_dict, title=None, save_path=None):
    """
    Compare multiple forecasts on the same plot.
    
    Args:
        historical: Historical data (pandas Series or array)
        forecasts_dict: Dictionary of forecasts {name: forecast_data}
        title: Plot title
        save_path: Path to save the plot
    """
    plt.figure(figsize=(14, 7))
    
    # Plot historical data
    if historical is not None:
        idx = historical.index if hasattr(historical, 'index') else np.arange(len(historical))
        plt.plot(idx, historical, label='Historical', color='gray', alpha=0.5, linewidth=2)
    
    # Plot each forecast with different colors
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    for i, (name, forecast) in enumerate(forecasts_dict.items()):
        if forecast is not None:
            idx = forecast.index if hasattr(forecast, 'index') else np.arange(len(forecast))
            color = colors[i % len(colors)]
            plt.plot(idx, forecast, label=name, color=color, linewidth=2, linestyle='--')
    
    if title:
        plt.title(title, fontsize=16)
    else:
        plt.title('Forecast Comparison', fontsize=16)
        
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            plt.savefig(save_path)
            print(f"Saved plot to {save_path}")
        except Exception as e:
            print(f"Error saving plot: {e}")
    
    plt.show()

def plot_seasonal_decomposition(data, period=7, title=None, save_path=None):
    """
    Plot seasonal decomposition of time series data.
    
    Args:
        data: Time series data (pandas Series)
        period: Seasonal period (default 7 for weekly)
        title: Plot title
        save_path: Path to save the plot
    """
    from statsmodels.tsa.seasonal import seasonal_decompose
    
    try:
        # Perform seasonal decomposition
        decomposition = seasonal_decompose(data, model='additive', period=period)
        
        fig, axes = plt.subplots(4, 1, figsize=(14, 10))
        
        # Original
        axes[0].plot(data.index if hasattr(data, 'index') else range(len(data)), 
                     data, color='blue')
        axes[0].set_ylabel('Original')
        axes[0].grid(True, alpha=0.3)
        
        # Trend
        axes[1].plot(decomposition.trend.index if hasattr(decomposition.trend, 'index') else range(len(decomposition.trend)), 
                     decomposition.trend, color='green')
        axes[1].set_ylabel('Trend')
        axes[1].grid(True, alpha=0.3)
        
        # Seasonal
        axes[2].plot(decomposition.seasonal.index if hasattr(decomposition.seasonal, 'index') else range(len(decomposition.seasonal)), 
                     decomposition.seasonal, color='orange')
        axes[2].set_ylabel('Seasonal')
        axes[2].grid(True, alpha=0.3)
        
        # Residual
        axes[3].plot(decomposition.resid.index if hasattr(decomposition.resid, 'index') else range(len(decomposition.resid)), 
                     decomposition.resid, color='red')
        axes[3].set_ylabel('Residual')
        axes[3].set_xlabel('Date')
        axes[3].grid(True, alpha=0.3)
        
        if title:
            plt.suptitle(title, fontsize=16, y=0.995)
        else:
            plt.suptitle('Seasonal Decomposition', fontsize=16, y=0.995)
            
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            try:
                plt.savefig(save_path)
                print(f"Saved plot to {save_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")
        
        plt.show()
    except Exception as e:
        print(f"Error in seasonal decomposition: {e}")
        print("Make sure data has enough observations for the specified period.")

def plot_category_forecast(data, category_col='Category', sales_col='Sales', date_col='Date', 
                           top_n=5, title=None, save_path=None):
    """
    Plot forecasts by category.
    
    Args:
        data: DataFrame with category and sales data
        category_col: Name of category column
        sales_col: Name of sales column
        date_col: Name of date column
        top_n: Number of top categories to show
        title: Plot title
        save_path: Path to save the plot
    """
    try:
        # Get top N categories by total sales
        top_categories = data.groupby(category_col)[sales_col].sum().nlargest(top_n).index
        
        plt.figure(figsize=(14, 7))
        
        for category in top_categories:
            cat_data = data[data[category_col] == category]
            if date_col in cat_data.columns:
                plt.plot(cat_data[date_col], cat_data[sales_col], label=category, linewidth=2)
            else:
                plt.plot(cat_data[sales_col], label=category, linewidth=2)
        
        if title:
            plt.title(title, fontsize=16)
        else:
            plt.title(f'Top {top_n} Categories - Sales Forecast', fontsize=16)
            
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            try:
                plt.savefig(save_path)
                print(f"Saved plot to {save_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")
        
        plt.show()
    except Exception as e:
        print(f"Error plotting category forecast: {e}")

def plot_region_forecast(data, region_col='Region', sales_col='Sales', date_col='Date', 
                        title=None, save_path=None):
    """
    Plot forecasts by region.
    
    Args:
        data: DataFrame with region and sales data
        region_col: Name of region column
        sales_col: Name of sales column
        date_col: Name of date column
        title: Plot title
        save_path: Path to save the plot
    """
    try:
        regions = data[region_col].unique()
        
        plt.figure(figsize=(14, 7))
        
        for region in regions:
            region_data = data[data[region_col] == region]
            if date_col in region_data.columns:
                plt.plot(region_data[date_col], region_data[sales_col], label=region, linewidth=2)
            else:
                plt.plot(region_data[sales_col], label=region, linewidth=2)
        
        if title:
            plt.title(title, fontsize=16)
        else:
            plt.title('Regional Sales Forecast', fontsize=16)
            
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            try:
                plt.savefig(save_path)
                print(f"Saved plot to {save_path}")
            except Exception as e:
                print(f"Error saving plot: {e}")
        
        plt.show()
    except Exception as e:
        print(f"Error plotting region forecast: {e}")
