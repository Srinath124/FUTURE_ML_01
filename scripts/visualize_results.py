import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

# Paths
BASE_DIR = r"p:\New portfolio\sales-forecasting"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "visualizations")
DATA_DIR = os.path.join(BASE_DIR, "outputs", "forecasts")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    try:
        model_comp = pd.read_csv(os.path.join(DATA_DIR, "model_comparison.csv"), index_col=0)
        daily_forecast = pd.read_csv(os.path.join(DATA_DIR, "90day_forecast.csv"))
        monthly_forecast = pd.read_csv(os.path.join(DATA_DIR, "monthly_forecast.csv"))
        test_preds = pd.read_csv(os.path.join(DATA_DIR, "test_predictions.csv"))
        return model_comp, daily_forecast, monthly_forecast, test_preds
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None

def plot_model_comparison(df):
    plt.figure(figsize=(10, 6))
    
    # We want to minimize RMSE, MAE, MSE. Maximize R2.
    # Let's plot RMSE as the primary metric for accuracy
    metric = 'RMSE'
    if metric in df.columns:
        sns.barplot(x=df.index, y=df[metric], palette="viridis")
        plt.title(f"Model Comparison - {metric} (Lower is Better)", fontsize=16)
        plt.ylabel(metric)
        plt.xlabel("Model")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "model_comparison_rmse.png"))
        plt.close()
        print("Generated model_comparison_rmse.png")
    else:
        print(f"Column {metric} not found in model comparison data.")

def plot_forecasts(daily_df, monthly_df):
    # 90 Day Forecast
    if daily_df is not None:
        plt.figure(figsize=(14, 7))
        daily_df['Date'] = pd.to_datetime(daily_df['Date'])
        sns.lineplot(data=daily_df, x='Date', y='Predicted_Sales', linewidth=2.5, color='dodgerblue')
        plt.title("90-Day Daily Sales Forecast", fontsize=16)
        plt.xlabel("Date")
        plt.ylabel("Predicted Sales")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "90day_forecast.png"))
        plt.close()
        print("Generated 90day_forecast.png")

    # Monthly Forecast
    if monthly_df is not None:
        plt.figure(figsize=(12, 6))
        # Assuming Month, Predicted Sales
        # Clean up column names if needed
        monthly_df.columns = [c.strip() for c in monthly_df.columns]
        
        if 'Month' in monthly_df.columns and 'Predicted Sales' in monthly_df.columns:
             # Convert Month to string if not already
            sns.barplot(data=monthly_df, x='Month', y='Predicted Sales', palette="magma")
            plt.title("Monthly Sales Forecast", fontsize=16)
            plt.xlabel("Month")
            plt.ylabel("Total Predicted Sales")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, "monthly_forecast.png"))
            plt.close()
            print("Generated monthly_forecast.png")

def plot_test_predictions(test_df):
    if test_df is not None:
        plt.figure(figsize=(14, 7))
        test_df['Date'] = pd.to_datetime(test_df['Date'])
        
        plt.plot(test_df['Date'], test_df['Actual'], label='Actual Sales', color='gray', alpha=0.7, linewidth=2)
        plt.plot(test_df['Date'], test_df['Predicted'], label='Predicted Sales', color='crimson', linewidth=2)
        
        plt.title("Model Reliability Check: Actual vs Predicted (Test Set)", fontsize=16)
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "prediction_vs_actual.png"))
        plt.close()
        print("Generated prediction_vs_actual.png")

def main():
    print("Starting visualization generation...")
    model_comp, daily, monthly, test_preds = load_data()
    
    if model_comp is not None:
        plot_model_comparison(model_comp)
    
    if daily is not None or monthly is not None:
        plot_forecasts(daily, monthly)
        
    if test_preds is not None:
        plot_test_predictions(test_preds)
        
    print("Visualization generation complete.")

if __name__ == "__main__":
    main()
