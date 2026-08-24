import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('seaborn-v0_8')

def monte_carlo_var(portfolio_value, mu, sigma, T=1/252, n_sims=10000, seed=42):
    """Calculate Value at Risk using Monte Carlo"""
    np.random.seed(seed)

    terminal_returns = np.random.normal(mu * T, sigma * np.sqrt(T), n_sims)
    terminal_values = portfolio_value * np.exp(terminal_returns)
    losses = portfolio_value - terminal_values

    var_95 = np.percentile(losses, 95)
    var_99 = np.percentile(losses, 99)
    es_95 = losses[losses >= var_95].mean()
    es_99 = losses[losses >= var_99].mean()

    print(f"Monte Carlo Risk Analysis ({n_sims:,} simulations)")
    print(f"Portfolio Value: ${portfolio_value:,.2f}")
    print(f"\nValue at Risk:")
    print(f"  95% VaR: ${var_95:,.2f}")
    print(f"  99% VaR: ${var_99:,.2f}")
    print(f"\nExpected Shortfall:")
    print(f"  95% ES: ${es_95:,.2f}")
    print(f"  99% ES: ${es_99:,.2f}")

    return {'var_95': var_95, 'var_99': var_99, 'es_95': es_95, 'es_99': es_99}, losses, terminal_values

def plot_risk(losses, terminal_values, portfolio_value, risk_metrics,
              save_path='results/monte_carlo_paths.png'):
    """Plot Monte Carlo risk analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Loss distribution
    axes[0, 0].hist(losses, bins=60, density=True, alpha=0.7, color='steelblue')
    axes[0, 0].axvline(x=risk_metrics['var_95'], color='red', linestyle='--', linewidth=2, label='95% VaR')
    axes[0, 0].axvline(x=risk_metrics['var_99'], color='darkred', linestyle='--', linewidth=2, label='99% VaR')
    axes[0, 0].set_xlabel('Loss ($)')
    axes[0, 0].set_ylabel('Density')
    axes[0, 0].set_title('Loss Distribution')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Terminal values
    axes[0, 1].hist(terminal_values, bins=60, density=True, alpha=0.7, color='darkgreen')
    axes[0, 1].axvline(x=np.percentile(terminal_values, 5), color='red', linestyle='--', linewidth=2)
    axes[0, 1].axvline(x=portfolio_value, color='blue', linestyle=':', linewidth=2, label='Initial')
    axes[0, 1].set_xlabel('Terminal Value ($)')
    axes[0, 1].set_ylabel('Density')
    axes[0, 1].set_title('Terminal Value Distribution')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Cumulative
    sorted_losses = np.sort(losses)
    cum_prob = np.arange(1, len(sorted_losses) + 1) / len(sorted_losses)
    axes[1, 0].plot(sorted_losses, cum_prob, linewidth=2, color='steelblue')
    axes[1, 0].axvline(x=risk_metrics['var_95'], color='red', linestyle='--', linewidth=2)
    axes[1, 0].axhline(y=0.95, color='red', linestyle='--', linewidth=1, alpha=0.7)
    axes[1, 0].set_xlabel('Loss ($)')
    axes[1, 0].set_ylabel('Cumulative Probability')
    axes[1, 0].set_title('Cumulative Loss Distribution')
    axes[1, 0].grid(True, alpha=0.3)

    # VaR sensitivity
    horizons = [1, 5, 10, 21]
    var_list = []
    for h in horizons:
        T = h / 252
        sim_returns = np.random.normal(0, 0.02 * np.sqrt(T), 10000)
        sim_losses = portfolio_value * (1 - np.exp(sim_returns))
        var_list.append(np.percentile(sim_losses, 95))

    axes[1, 1].bar([str(h) for h in horizons], var_list, color='steelblue', alpha=0.8)
    axes[1, 1].set_xlabel('Time Horizon (days)')
    axes[1, 1].set_ylabel('95% VaR ($)')
    axes[1, 1].set_title('VaR vs Time Horizon')
    axes[1, 1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    print("Loading AAPL data...")
    df = pd.read_csv('data/aapl_with_returns.csv')

    returns = df['Log_Return'].dropna()
    daily_mu, daily_sigma = returns.mean(), returns.std()

    portfolio_value = 100000
    risk_metrics, losses, terminal_values = monte_carlo_var(portfolio_value, daily_mu, daily_sigma)
    plot_risk(losses, terminal_values, portfolio_value, risk_metrics)

    pd.DataFrame({'Loss': losses, 'Terminal_Value': terminal_values}).to_csv('data/monte_carlo_risk.csv', index=False)
    print(f"\nSaved to: data/monte_carlo_risk.csv")
