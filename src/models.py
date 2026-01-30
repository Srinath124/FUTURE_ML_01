import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

class BaselineForecaster:
    def __init__(self, method='naive'):
        self.method = method
        self.value = None

    def fit(self, y):
        if self.method == 'naive':
            self.value = y.iloc[-1]
        elif self.method == 'mean':
            self.value = y.mean()

    def predict(self, horizon):
        return pd.Series([self.value] * horizon)

class ARIMAForecaster:
    def __init__(self, order=(1, 1, 1), seasonal_order=None):
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.model_fit = None

    def fit(self, y):
        self.model = ARIMA(y, order=self.order, seasonal_order=self.seasonal_order)
        self.model_fit = self.model.fit()

    def predict(self, horizon):
        return self.model_fit.forecast(steps=horizon)

class MLForecaster:
    def __init__(self, model_type='linear_regression', **kwargs):
        self.model_type = model_type
        if model_type == 'linear_regression':
            self.model = LinearRegression(**kwargs)
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(**kwargs)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def get_feature_importance(self, feature_names):
        if self.model_type == 'random_forest':
            importances = self.model.feature_importances_
            return pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)
        else:
            raise NotImplementedError("Feature importance only available for Random Forest")

def evaluate_model(y_true, y_pred, model_name):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    
    # Avoid division by zero for MAPE
    with np.errstate(divide='ignore', invalid='ignore'):
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
    r2 = r2_score(y_true, y_pred)
    
    print(f"\n📊 {model_name} Performance:")
    print("-" * 50)
    print(f"   RMSE:  ${rmse:,.2f}")
    print(f"   MAE:   ${mae:,.2f}")
    print(f"   MAPE:  {mape:.2f}%")
    print(f"   R²:    {r2:.4f}")
    print("-" * 50 + "\n")
    
    return {'RMSE': rmse, 'MAE': mae, 'MAPE': mape, 'R2': r2}

def compare_models(results_dict):
    df = pd.DataFrame(results_dict).T
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    print(df)
    print("="*60 + "\n")
    
    best_model = df['RMSE'].idxmin()
    print(f"🏆 Best Model: {best_model}")
    print(f"   MAPE: {df.loc[best_model, 'MAPE']:.2f}%")
    
    return df
