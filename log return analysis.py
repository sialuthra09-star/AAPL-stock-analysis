import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

plt.style.use('seaborn-v0_8')
sns.set_palette("deep")

def calculate_log_returns(df, price_col='Close'):
    """Calculate log returns from price data"""
    df = df.copy()
    df['Log_Return'] = np.log(df[price_col] / df[price_col].shift(1))
    df['Simple_Return'] = df[price_col].pct_change()
    df = df.dropna().reset_index(drop=True)

    print(f"Log returns calculated:")
    print(f"Mean: {df['Log_Return'].mean():.6f}")
    print(f"Std: {df['Log_Return'].std():.6f}")
    print(f"Min: {df['Log_Return'].min():.6f}")
    print(f"Max: {df['Log_Return'].max():.6f}")

    return df

def analyze_return_distribution(df):
    """Analyze statistical properties of log returns"""
    returns = df['Log_Return']

    stats_dict = {
        'mean': returns.mean(),
        'std': returns.std(),
        'skewness': stats.skew(returns),
        'kurtosis': stats.kurtosis(returns),
        'min': returns.min(),
        'max': returns.max(),
        'var_95': np.percentile(returns, 5),
        'var_99': np.percentile(returns, 1)
    }

    print("\nReturn Distribution Statistics:")
    for k, v in stats_dict.items():
        print(f"{k}: {v:.6f}")

    _, p_value = stats.normaltest(returns)
    print(f"\nNormality test p-value: {p_value:.4f}")

    return stats_dict

def plot_return_analysis(df, save_path='results/return_distribution.png'):
    """Create comprehensive return distribution plots"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    returns = df['Log_Return'].dropna()

    # Time series
    axes[0, 0].plot(df['Date'], returns, linewidth=0.8, alpha=0.7)
    axes[0, 0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Log Return')
    axes[0, 0].set_title('AAPL Log Returns Over Time')
    axes[0, 0].grid(True, alpha=0.3)

    # Histogram
    axes[0, 1].hist(returns, bins=50, density=True, alpha=0.7, color='steelblue')
    x = np.linspace(returns.min(), returns.max(), 100)
    axes[0, 1].plot(x, stats.norm.pdf(x, returns.mean(), returns.std()), 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Log Return')
    axes[0, 1].set_ylabel('Density')
    axes[0, 1].set_title('Return Distribution')
    axes[0, 1].grid(True, alpha=0.3)

    # Q-Q plot
    stats.probplot(returns, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title('Q-Q Plot')
    axes[1, 0].grid(True, alpha=0.3)

    # Rolling volatility
    rolling_std = returns.rolling(window=30).std()
    axes[1, 1].plot(df['Date'][30:], rolling_std[30:], linewidth=1.5, color='darkorange')
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Volatility (30-day)')
    axes[1, 1].set_title('Rolling Volatility')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    print("Loading AAPL data...")
    df = pd.read_csv('data/aapl_historical.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    df = calculate_log_returns(df)
    stats_dict = analyze_return_distribution(df)
    plot_return_analysis(df)

    df.to_csv('data/aapl_with_returns.csv', index=False)
    print(f"\nProcessed data saved to: data/aapl_with_returns.csv")
