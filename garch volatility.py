import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8')

def fit_garch_model(returns, p=1, q=1):
    """Fit GARCH(p,q) model to returns"""
    from arch import arch_model

    print(f"Fitting GARCH({p},{q}) model...")
    returns_clean = returns.dropna()

    model = arch_model(returns_clean, mean='Constant', vol='GARCH', p=p, q=q)
    results = model.fit(disp='off', show_warning=False)

    print(f"\nGARCH Model Results:")
    print(results.summary())

    return results

def plot_garch(results, returns, save_path='results/garch_volatility.png'):
    """Plot GARCH model results"""
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))

    cond_vol = results.conditional_volatility
    dates = returns.index

    # Returns
    axes[0, 0].plot(dates, returns, linewidth=0.8, alpha=0.7)
    axes[0, 0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Log Return')
    axes[0, 0].set_title('AAPL Log Returns')
    axes[0, 0].grid(True, alpha=0.3)

    # Conditional volatility
    axes[0, 1].plot(dates, cond_vol, linewidth=1.5, color='darkorange')
    axes[0, 1].axhline(y=cond_vol.mean(), color='red', linestyle='--')
    axes[0, 1].set_xlabel('Date')
    axes[0, 1].set_ylabel('Conditional Volatility')
    axes[0, 1].set_title('GARCH Conditional Volatility')
    axes[0, 1].grid(True, alpha=0.3)

    # Returns with vol bands
    axes[1, 0].plot(dates, returns, linewidth=0.8, alpha=0.6)
    axes[1, 0].plot(dates, cond_vol, 'r--', linewidth=1.5, alpha=0.8)
    axes[1, 0].plot(dates, -cond_vol, 'r--', linewidth=1.5, alpha=0.8)
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].set_ylabel('Log Return')
    axes[1, 0].set_title('Returns with Volatility Bands')
    axes[1, 0].grid(True, alpha=0.3)

    # Volatility histogram
    axes[1, 1].hist(cond_vol, bins=40, density=True, alpha=0.7, color='steelblue')
    axes[1, 1].axvline(x=cond_vol.mean(), color='red', linestyle='--', linewidth=2)
    axes[1, 1].set_xlabel('Conditional Volatility')
    axes[1, 1].set_ylabel('Density')
    axes[1, 1].set_title('Volatility Distribution')
    axes[1, 1].grid(True, alpha=0.3)

    # Standardized residuals
    axes[2, 0].plot(dates, results.std_resid, linewidth=0.8, alpha=0.7)
    axes[2, 0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    axes[2, 0].axhline(y=2, color='red', linestyle=':', linewidth=1.5)
    axes[2, 0].axhline(y=-2, color='red', linestyle=':', linewidth=1.5)
    axes[2, 0].set_xlabel('Date')
    axes[2, 0].set_ylabel('Standardized Residual')
    axes[2, 0].set_title('Standardized Residuals')
    axes[2, 0].grid(True, alpha=0.3)

    # Q-Q plot
    stats.probplot(results.std_resid.dropna(), dist="norm", plot=axes[2, 1])
    axes[2, 1].set_title('Q-Q Plot (Residuals)')
    axes[2, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    print("Loading AAPL data...")
    df = pd.read_csv('data/aapl_with_returns.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')

    returns = df['Log_Return']
    results = fit_garch_model(returns)
    plot_garch(results, returns)

    vol_df = pd.DataFrame({'Date': returns.index, 'Conditional_Volatility': results.conditional_volatility})
    vol_df.to_csv('data/garch_volatility.csv', index=False)
    print(f"\nSaved to: data/garch_volatility.csv")
