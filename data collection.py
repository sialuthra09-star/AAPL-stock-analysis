import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def download_aapl_data(start_date=None, end_date=None):
    """
    Download AAPL historical data from Yahoo Finance

    Parameters:
    -----------
    start_date : str, optional
        Start date in YYYY-MM-DD format (default: 2 years ago)
    end_date : str, optional
        End date in YYYY-MM-DD format (default: today)

    Returns:
    --------
    pd.DataFrame
        Historical stock data
    """
    # Default to last 2 years
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')

    print(f"Downloading AAPL data from {start_date} to {end_date}...")

    # Download data
    aapl = yf.download('AAPL', start=start_date, end=end_date, progress=False)

    # Clean column names (handle multi-index if present)
    if isinstance(aapl.columns, pd.MultiIndex):
        aapl.columns = aapl.columns.get_level_values(0)

    # Reset index to make Date a column
    aapl = aapl.reset_index()

    # Save to CSV
    os.makedirs('data', exist_ok=True)
    aapl.to_csv('data/aapl_historical.csv', index=False)

    print(f"Data downloaded successfully!")
    print(f"Shape: {aapl.shape}")
    print(f"Columns: {list(aapl.columns)}")
    print(f"Date range: {aapl['Date'].min()} to {aapl['Date'].max()}")
    print(f"Saved to: data/aapl_historical.csv")

    return aapl

def preprocess_data(df):
    """
    Preprocess the data: handle missing values, sort by date

    Parameters:
    -----------
    df : pd.DataFrame
        Raw stock data

    Returns:
    --------
    pd.DataFrame
        Cleaned data
    """
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)

    # Drop rows with missing values
    df = df.dropna()

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    print(f"\nPreprocessing complete:")
    print(f"Missing values removed: {df.isnull().sum().sum()}")
    print(f"Final shape: {df.shape}")

    return df

if __name__ == "__main__":
    # Download last 2 years of data
    aapl_data = download_aapl_data()

    # Preprocess
    aapl_clean = preprocess_data(aapl_data)

    # Display sample
    print("\nFirst 5 rows:")
    print(aapl_clean.head())

    print("\nLast 5 rows:")
    print(aapl_clean.tail())

    # Show date range
    print(f"\nData covers: {aapl_clean['Date'].min().strftime('%Y-%m-%d')} to {aapl_clean['Date'].max().strftime('%Y-%m-%d')}")
    print(f"Total trading days: {len(aapl_clean)}")
