import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

plt.style.use('seaborn-v0_8')

def gbm_parameters(df, price_col='Close'):
    """Estimate GBM parameters from historical data"""
    prices = df[price_col].values
    log_returns = np.log(prices[1:] / prices[:-1])

    mu = log_returns.mean() * 252
    sigma = log_returns.std() * np.sqrt(252)
    S0 = prices[-1]

    print(f"GBM Parameters (annualized):")
    print(f"Drift (μ): {mu:.4f} ({mu*100:.2f}%)")
    print(f"Volatility (σ): {sigma:.4f} ({sigma*100:.2f}%)")
    print(f"Initial Price (S₀): ${S0:.2f}")

    return mu, sigma, S0

def simulate_gbm(S0, mu, sigma, T, n_steps, n_paths, seed=42):
    """Simulate Geometric Brownian Motion paths"""
    np.random.seed(seed)
    dt = T / n_steps

    paths = np.zeros((n_steps + 1, n_paths))
    paths[0] = S0

    for t in range(1, n_steps + 1):
        dW = np.random.normal(0, np.sqrt(dt), n_paths)
        paths[t] = paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * dW)

    time_grid = np.linspace(0, T, n_steps + 1)
    return paths, time_grid

def plot_gbm(paths, time_grid, S0, T, save_path='results/gbm_paths.png'):
    """Plot GBM simulation results"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    n_paths = paths.shape[1]

    # Multiple paths
    for i in range(min(50, n_paths)):
        axes[0, 0].plot(time_grid, paths[:, i], linewidth=0.8, alpha=0.6)
    axes[0, 0].axhline(y=S0, color='red', linestyle='--', linewidth=2)
    axes[0, 0].set_xlabel('Time (years)')
    axes[0, 0].set_ylabel('Stock Price ($)')
    axes[0, 0].set_title(f'GBM Simulation ({n_paths} paths)')
    axes[0, 0].grid(True, alpha=0.3)

    # Mean and CI
    mean_path = np.mean(paths, axis=1)
    std_path = np.std(paths, axis=1)
    axes[0, 1].plot(time_grid, mean_path, 'b-', linewidth=2.5, label='Mean')
    axes[0, 1].fill_between(time_grid, mean_path - 1.96*std_path, mean_path + 1.96*std_path, alpha=0.3)
    axes[0, 1].set_xlabel('Time (years)')
    axes[0, 1].set_ylabel('Stock Price ($)')
    axes[0, 1].set_title('Mean with 95% CI')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Terminal distribution
    terminal = paths[-1, :]
    axes[1, 0].hist(terminal, bins=50, density=True, alpha=0.7, color='steelblue')
    axes[1, 0].set_xlabel('Terminal Price ($)')
    axes[1, 0].set_ylabel('Density')
    axes[1, 0].set_title(f'Terminal Distribution (T={T})')
    axes[1, 0].grid(True, alpha=0.3)

    # Quantiles
    for q, c in zip([0.1, 0.5, 0.9], ['purple', 'green', 'red']):
        axes[1, 1].plot(time_grid, np.quantile(paths, q, axis=1), linewidth=2, label=f'{int(q*100)}th %ile')
    axes[1, 1].set_xlabel('Time (years)')
    axes[1, 1].set_ylabel('Stock Price ($)')
    axes[1, 1].set_title('Quantile Paths')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    print("Loading AAPL data...")
    df = pd.read_csv('data/aapl_with_returns.csv')

    mu, sigma, S0 = gbm_parameters(df)

    T, n_steps, n_paths = 1.0, 252, 1000
    print(f"\nSimulating {n_paths} paths for {T} year...")

    paths, time_grid = simulate_gbm(S0, mu, sigma, T, n_steps, n_paths)
    plot_gbm(paths, time_grid, S0, T)

    pd.DataFrame(paths).to_csv('data/gbm_simulations.csv', index=False)
    print(f"\nSaved to: data/gbm_simulations.csv")
