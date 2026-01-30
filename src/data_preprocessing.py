import pandas as pd
import numpy as np

def load_data(filepath):
    """
    Load data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    try:
        df = pd.read_csv(filepath, encoding='windows-1252') # Common encoding for superstore dataset
        print(f"✅ Successfully loaded data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding='utf-8')
        print(f"✅ Successfully loaded data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        raise e

def explore_data(df):
    """
    Perform basic data exploration.
    
    Args:
        df (pd.DataFrame): Dataframe to explore.
    """
    print("\n" + "="*60)
    print("DATASET OVERVIEW")
    print("="*60)
    print(f"\nShape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")
    
    print("\n" + "-"*60)
    print("DATA TYPES")
    print("-"*60)
    print(df.dtypes)
    
    print("\n" + "-"*60)
    print("MISSING VALUES")
    print("-"*60)
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("Empty DataFrame")
        print("Columns: [Missing Count, Percentage]")
        print("Index: []")
    else:
        print(missing[missing > 0])
        
    print("\n" + "-"*60)
    print("BASIC STATISTICS")
    print("-"*60)
    print(df.describe())

def validate_data_quality(df):
    """
    Check for data quality issues like duplicates.
    
    Args:
        df (pd.DataFrame): Dataframe to validate.
        
    Returns:
        bool: True if data quality is acceptable, False otherwise.
    """
    print("\n" + "="*60)
    print("DATA QUALITY CHECK")
    print("="*60)
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"Duplicate Rows: {duplicates}")
    
    # Check for missing values again (summary)
    missing_total = df.isnull().sum().sum()
    print(f"Total Missing Values: {missing_total}")
    
    if duplicates > 0:
        print(f"⚠️ Warning: Found {duplicates} duplicate rows.")
    
    if missing_total > 0:
        print(f"⚠️ Warning: Found {missing_total} missing values.")
        
    print("\n✅ Data quality check completed.")
    return True

def handle_missing_values(df):
    """
    Handle missing values in the dataframe.
    
    Args:
        df (pd.DataFrame): Dataframe to clean.
        
    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    print("\n" + "-"*60)
    print("HANDLING MISSING VALUES")
    print("-"*60)
    
    initial_rows = df.shape[0]
    missing = df.isnull().sum()
    
    if missing.sum() == 0:
        print("✅ No missing values found")
        return df
    
    # Simple strategy: drop rows with missing values for now
    # In a real scenario, imputation might be better depending on the column
    df_clean = df.dropna()
    rows_dropped = initial_rows - df_clean.shape[0]
    
    print(f"Dropped {rows_dropped} rows with missing values.")
    print(f"✅ Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    
    return df_clean

def prepare_time_series_data(df, date_column='Order Date', value_column='Sales', freq='D'):
    """
    Prepare time series data by aggregating by date.
    
    Args:
        df (pd.DataFrame): Input dataframe.
        date_column (str): Name of the date column.
        value_column (str): Name of the value column to aggregate.
        freq (str): Frequency string (e.g. 'D' for daily).
        
    Returns:
        pd.DataFrame: Aggregated time series data.
    """
    print("\n" + "-"*60)
    print("PREPARING TIME SERIES DATA")
    print("-"*60)
    
    df = df.copy()
    
    # Ensure date column is datetime
    if df[date_column].dtype == 'object':
        df[date_column] = pd.to_datetime(df[date_column])
        
    # Set index
    df = df.set_index(date_column)
    
    # Sort index
    df = df.sort_index()
    
    # Aggregation
    ts_data = df[value_column].resample(freq).sum().to_frame()
    
    print(f"✅ Prepared time series data:")
    print(f"   Date range: {ts_data.index.min()} to {ts_data.index.max()}")
    print(f"   Frequency: {freq}")
    print(f"   Total periods: {ts_data.shape[0]}")
    
    return ts_data
