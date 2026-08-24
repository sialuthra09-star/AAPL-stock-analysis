import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

plt.style.use('seaborn-v0_8')

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes option price"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

def black_scholes_vectorized(S, K, T, r, sigma, option_type='call'):
    """Vectorized Black-Scholes for arrays"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

def analyze_option_chain(S, r, sigma, T, n_strikes=21):
    """Analyze option chain across strikes"""
    strikes = np.linspace(S * 0.8, S * 1.2, n_strikes)

    call_prices = black_scholes_vectorized(S, strikes, T, r, sigma, 'call')
    put_prices = black_scholes_vectorized(S, strikes, T, r, sigma, 'put')
    call_intrinsic = np.maximum(S - strikes, 0)
    put_intrinsic = np.maximum(strikes - S, 0)

    return pd.DataFrame({
        'Strike': strikes,
        'Call_Price': call_prices,
        'Put_Price': put_prices,
        'Call_Intrinsic': call_intrinsic,
        'Put_Intrinsic': put_intrinsic,
        'Call_Time_Value': call_prices - call_intrinsic,
        'Put_Time_Value': put_prices - put_intrinsic
    })

def plot_bs(option_chain, S, K, T, r, sigma, save_path='results/option_sensitivity.png'):
    """Plot Black-Scholes analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Prices vs strike
    axes[0, 0].plot(option_chain['Strike'], option_chain['Call_Price'], 'b-', linewidth=2.5, label='Call')
    axes[0, 0].plot(option_chain['Strike'], option_chain['Put_Price'], 'r-', linewidth=2.5, label='Put')
    axes[0, 0].axvline(x=S, color='black', linestyle='--', linewidth=1.5, label=f'Spot: ${S:.2f}')
    axes[0, 0].axvline(x=K, color='green', linestyle=':', linewidth=2, label=f'Strike: ${K:.2f}')
    axes[0, 0].set_xlabel('Strike Price ($)')
    axes[0, 0].set_ylabel('Option Price ($)')
    axes[0, 0].set_title(f'Option Prices vs Strike')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Intrinsic vs time value
    axes[0, 1].plot(option_chain['Strike'], option_chain['Call_Time_Value'], 'b-', linewidth=2, label='Call Time Value')
    axes[0, 1].plot(option_chain['Strike'], option_chain['Put_Time_Value'], 'r-', linewidth=2, label='Put Time Value')
    axes[0, 1].set_xlabel('Strike Price ($)')
    axes[0, 1].set_ylabel('Value ($)')
    axes[0, 1].set_title('Time Value')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Price vs T
    T_values = np.linspace(0.01, 2.0, 100)
    axes[1, 0].plot(T_values, black_scholes_vectorized(S, K, T_values, r, sigma, 'call'), 'b-', linewidth=2.5, label='Call')
    axes[1, 0].plot(T_values, black_scholes_vectorized(S, K, T_values, r, sigma, 'put'), 'r-', linewidth=2.5, label='Put')
    axes[1, 0].axvline(x=T, color='green', linestyle='--', linewidth=2)
    axes[1, 0].set_xlabel('Time to Expiration (years)')
    axes[1, 0].set_ylabel('Option Price ($)')
    axes[1, 0].set_title('Option Price vs Time')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Price vs sigma
    sigma_values = np.linspace(0.1, 0.8, 100)
    axes[1, 1].plot(sigma_values, black_scholes_vectorized(S, K, T, r, sigma_values, 'call'), 'b-', linewidth=2.5, label='Call')
    axes[1, 1].plot(sigma_values, black_scholes_vectorized(S, K, T, r, sigma_values, 'put'), 'r-', linewidth=2.5, label='Put')
    axes[1, 1].axvline(x=sigma, color='green', linestyle='--', linewidth=2)
    axes[1, 1].set_xlabel('Volatility')
    axes[1, 1].set_ylabel('Option Price ($)')
    axes[1, 1].set_title('Option Price vs Volatility')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    S, K, T, r, sigma = 175.0, 180.0, 0.25, 0.05, 0.25

    print(f"Black-Scholes Option Pricing")
    print(f"S=${S:.2f}, K=${K:.2f}, T={T:.2f}, r={r:.2%}, σ={sigma:.2%}")

    option_chain = analyze_option_chain(S, r, sigma, T)
    plot_bs(option_chain, S, K, T, r, sigma)

    option_chain.to_csv('data/option_chain.csv', index=False)
    print(f"\nSaved to: data/option_chain.csv")
