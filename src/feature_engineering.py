import pandas as pd
import numpy as np

def create_time_features(df, date_column='Order Date'):
    """Creates time-based features from datetime column."""
    df = df.copy()
    
    # Handle index if it's the date column
    if date_column not in df.columns and df.index.name == date_column:
        df = df.reset_index()
    elif date_column not in df.columns and isinstance(df.index, pd.DatetimeIndex):
        df[date_column] = df.index
        
    # Ensure datetime
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Extract features
        df['year'] = df[date_column].dt.year
        df['month'] = df[date_column].dt.month
        df['day'] = df[date_column].dt.day
        df['dayofweek'] = df[date_column].dt.dayofweek
        df['quarter'] = df[date_column].dt.quarter
        df['is_month_start'] = df[date_column].dt.is_month_start.astype(int)
        df['is_month_end'] = df[date_column].dt.is_month_end.astype(int)
        
        # Seasonality (Cyclical features)
        df['month_sin'] = np.sin(2 * np.pi * df['month']/12)
        df['month_cos'] = np.cos(2 * np.pi * df['month']/12)
        df['day_sin'] = np.sin(2 * np.pi * df['dayofweek']/7)
        df['day_cos'] = np.cos(2 * np.pi * df['dayofweek']/7)
    
    return df

def create_lag_features(df, value_column='Sales', lags=[1, 7, 14, 30]):
    """Creates lag features."""
    df = df.copy()
    for lag in lags:
        df[f'lag_{lag}'] = df[value_column].shift(lag)
    return df

def create_rolling_features(df, value_column='Sales', windows=[7, 30]):
    """Creates rolling mean and std features."""
    df = df.copy()
    for window in windows:
        df[f'rolling_mean_{window}'] = df[value_column].rolling(window=window).mean()
        df[f'rolling_std_{window}'] = df[value_column].rolling(window=window).std()
    return df

def create_all_features(df, date_column='Order Date', target_column='Sales', lag_periods=[1, 7, 14, 30], rolling_windows=[7, 30]):
    """Wrapper to create all features."""
    # Ensure sorted by date
    if date_column in df.columns:
        df = df.sort_values(date_column)
    elif isinstance(df.index, pd.DatetimeIndex):
        df = df.sort_index()
        
    df = create_time_features(df, date_column)
    df = create_lag_features(df, value_column=target_column, lags=lag_periods)
    df = create_rolling_features(df, value_column=target_column, windows=rolling_windows)
    
    # Drop rows with NaN due to lags/rolling
    df = df.dropna()
    
    return df
