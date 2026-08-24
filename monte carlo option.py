import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('seaborn-v0_8')

def monte_carlo_option_price(S, K, T, r, sigma, n_sims=100000, option_type='call', seed=42):
    """Price European option using Monte Carlo"""
    np.random.seed(seed)

    Z = np.random.normal(0, 1, n_sims)
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == 'call':
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)

    discounted = np.exp(-r * T) * payoffs
    option_price = discounted.mean()
    std_error = discounted.std() / np.sqrt(n_sims)

    print(f"Monte Carlo Option Pricing ({n_sims:,} simulations)")
    print(f"{option_type.upper()} Option: S=${S:.2f}, K=${K:.2f}, T={T:.2f}, r={r:.2%}, σ={sigma:.2%}")
    print(f"\nResults:")
    print(f"  Option Price: ${option_price:.4f}")
    print(f"  Std Error: ${std_error:.6f}")
    print(f"  95% CI: (${option_price - 1.96*std_error:.4f}, ${option_price + 1.96*std_error:.4f})")
    print(f"  Probability ITM: {np.mean(payoffs > 0):.2%}")

    return {'price': option_price, 'std_error': std_error}, S_T, discounted

def convergence_analysis(S, K, T, r, sigma, max_sims=50000, step=1000, seed=42):
    """Analyze convergence"""
    np.random.seed(seed)

    n_range = range(step, max_sims + 1, step)
    prices, std_errors = [], []

    for n in n_range:
        Z = np.random.normal(0, 1, n)
        S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
        payoffs = np.maximum(S_T - K, 0)
        discounted = np.exp(-r * T) * payoffs

        prices.append(discounted.mean())
        std_errors.append(discounted.std() / np.sqrt(n))

    return pd.DataFrame({'n_simulations': list(n_range), 'price': prices, 'std_error': std_errors})

def plot_mc(results, S_T, discounted, conv_df, save_path='results/monte_carlo_paths.png'):
    """Plot Monte Carlo results"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Terminal distribution
    axes[0, 0].hist(S_T, bins=60, density=True, alpha=0.7, color='steelblue')
    axes[0, 0].axvline(x=S_T.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${S_T.mean():.2f}')
    axes[0, 0].set_xlabel('Terminal Price ($)')
    axes[0, 0].set_ylabel('Density')
    axes[0, 0].set_title('Terminal Stock Price Distribution')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Payoff distribution
    nonzero = discounted[discounted > 0]
    axes[0, 1].hist(nonzero, bins=60, density=True, alpha=0.7, color='darkorange')
    axes[0, 1].axvline(x=discounted.mean(), color='red', linestyle='--', linewidth=2)
    axes[0, 1].set_xlabel('Discounted Payoff ($)')
    axes[0, 1].set_ylabel('Density')
    axes[0, 1].set_title('Discounted Payoff Distribution')
    axes[0, 1].grid(True, alpha=0.3)

    # Convergence
    axes[1, 0].plot(conv_df['n_simulations'], conv_df['price'], linewidth=1.5, label='Price')
    axes[1, 0].fill_between(conv_df['n_simulations'],
                            conv_df['price'] - 1.96*conv_df['std_error'],
                            conv_df['price'] + 1.96*conv_df['std_error'], alpha=0.3)
    axes[1, 0].axhline(y=results['price'], color='red', linestyle='--', linewidth=2, label=f'Final: ${results["price"]:.4f}')
    axes[1, 0].set_xlabel('Simulations')
    axes[1, 0].set_ylabel('Option Price ($)')
    axes[1, 0].set_title('Convergence')
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(True, alpha=0.3)

    # Std error
    axes[1, 1].plot(conv_df['n_simulations'], conv_df['std_error'], linewidth=1.5, color='darkgreen')
    axes[1, 1].set_xlabel('Simulations')
    axes[1, 1].set_ylabel('Standard Error ($)')
    axes[1, 1].set_title('Standard Error Convergence')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    S, K, T, r, sigma = 175.0, 180.0, 0.25, 0.05, 0.25

    print("=" * 60)
    call_results, S_T, call_payoffs = monte_carlo_option_price(S, K, T, r, sigma, option_type='call')
    print()
    put_results, _, put_payoffs = monte_carlo_option_price(S, K, T, r, sigma, option_type='put')

    print("\nRunning convergence analysis...")
    conv_df = convergence_analysis(S, K, T, r, sigma)

    plot_mc(call_results, S_T, call_payoffs, conv_df)

    pd.DataFrame({'Terminal_Price': S_T, 'Call_Payoff': call_payoffs, 'Put_Payoff': put_payoffs}).to_csv('data/mc_option_results.csv', index=False)
    conv_df.to_csv('data/mc_convergence.csv', index=False)
    print(f"\nSaved results")
