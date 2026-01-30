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
