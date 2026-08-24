import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

plt.style.use('seaborn-v0_8')

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """Calculate all Greeks for European option"""
    if T <= 0 or sigma <= 0:
        return None

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    nd1 = norm.pdf(d1)

    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (-S * nd1 * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    else:
        delta = norm.cdf(d1) - 1
        theta = (-S * nd1 * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

    gamma = nd1 / (S * sigma * np.sqrt(T))
    vega = S * nd1 * np.sqrt(T) / 100
    rho = (K * T * np.exp(-r * T) * norm.cdf(d2) if option_type == 'call' else -K * T * np.exp(-r * T) * norm.cdf(-d2)) / 100

    return {'delta': delta, 'gamma': gamma, 'vega': vega, 'theta': theta, 'rho': rho}

def greeks_summary(S, K, T, r, sigma):
    """Calculate Greeks for call and put"""
    call_g = calculate_greeks(S, K, T, r, sigma, 'call')
    put_g = calculate_greeks(S, K, T, r, sigma, 'put')

    return pd.DataFrame({
        'Greek': ['Delta', 'Gamma', 'Vega', 'Theta', 'Rho'],
        'Call': [call_g['delta'], call_g['gamma'], call_g['vega'], call_g['theta'], call_g['rho']],
        'Put': [put_g['delta'], put_g['gamma'], put_g['vega'], put_g['theta'], put_g['rho']]
    })

def analyze_greeks_strikes(S, T, r, sigma, n_strikes=41):
    """Analyze Greeks across strikes"""
    strikes = np.linspace(S * 0.8, S * 1.2, n_strikes)

    data = {'Strike': strikes, 'Moneyness': strikes / S}

    for greek in ['delta', 'gamma', 'vega', 'theta', 'rho']:
        data[f'Call_{greek.capitalize()}'] = [calculate_greeks(S, K, T, r, sigma, 'call')[greek] for K in strikes]
        data[f'Put_{greek.capitalize()}'] = [calculate_greeks(S, K, T, r, sigma, 'put')[greek] for K in strikes]

    return pd.DataFrame(data)

def analyze_greeks_time(S, K, r, sigma, n_points=100):
    """Analyze Greeks across time"""
    T_values = np.linspace(0.01, 2.0, n_points)

    data = {'T': T_values}

    for greek in ['delta', 'gamma', 'vega', 'theta', 'rho']:
        data[f'Call_{greek.capitalize()}'] = [calculate_greeks(S, K, T, r, sigma, 'call')[greek] if calculate_greeks(S, K, T, r, sigma, 'call') else np.nan for T in T_values]
        data[f'Put_{greek.capitalize()}'] = [calculate_greeks(S, K, T, r, sigma, 'put')[greek] if calculate_greeks(S, K, T, r, sigma, 'put') else np.nan for T in T_values]

    return pd.DataFrame(data)

def plot_greeks(strikes_df, time_df, S, K, T, save_path='results/option_sensitivity.png'):
    """Plot Greeks analysis"""
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))

    # Delta vs Strike
    axes[0, 0].plot(strikes_df['Strike'], strikes_df['Call_Delta'], 'b-', linewidth=2.5, label='Call')
    axes[0, 0].plot(strikes_df['Strike'], strikes_df['Put_Delta'], 'r-', linewidth=2.5, label='Put')
    axes[0, 0].axvline(x=S, color='black', linestyle='--', linewidth=1.5)
    axes[0, 0].axvline(x=K, color='green', linestyle=':', linewidth=2)
    axes[0, 0].axhline(y=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    axes[0, 0].set_xlabel('Strike ($)')
    axes[0, 0].set_ylabel('Delta')
    axes[0, 0].set_title('Delta vs Strike')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Gamma vs Strike
    axes[0, 1].plot(strikes_df['Strike'], strikes_df['Call_Gamma'], 'b-', linewidth=2.5, label='Call')
    axes[0, 1].plot(strikes_df['Strike'], strikes_df['Put_Gamma'], 'r-', linewidth=2.5, label='Put')
    axes[0, 1].axvline(x=S, color='black', linestyle='--', linewidth=1.5)
    axes[0, 1].set_xlabel('Strike ($)')
    axes[0, 1].set_ylabel('Gamma')
    axes[0, 1].set_title('Gamma vs Strike')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Vega vs Strike
    axes[1, 0].plot(strikes_df['Strike'], strikes_df['Call_Vega'], 'b-', linewidth=2.5, label='Call')
    axes[1, 0].plot(strikes_df['Strike'], strikes_df['Put_Vega'], 'r-', linewidth=2.5, label='Put')
    axes[1, 0].axvline(x=S, color='black', linestyle='--', linewidth=1.5)
    axes[1, 0].set_xlabel('Strike ($)')
    axes[1, 0].set_ylabel('Vega')
    axes[1, 0].set_title('Vega vs Strike')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Theta vs Strike
    axes[1, 1].plot(strikes_df['Strike'], strikes_df['Call_Theta'], 'b-', linewidth=2.5, label='Call')
    axes[1, 1].plot(strikes_df['Strike'], strikes_df['Put_Theta'], 'r-', linewidth=2.5, label='Put')
    axes[1, 1].axvline(x=S, color='black', linestyle='--', linewidth=1.5)
    axes[1, 1].set_xlabel('Strike ($)')
    axes[1, 1].set_ylabel('Theta (daily)')
    axes[1, 1].set_title('Theta vs Strike')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    # Delta vs Time
    axes[2, 0].plot(time_df['T'], time_df['Call_Delta'], 'b-', linewidth=2.5, label='Call')
    axes[2, 0].plot(time_df['T'], time_df['Put_Delta'], 'r-', linewidth=2.5, label='Put')
    axes[2, 0].axvline(x=T, color='green', linestyle='--', linewidth=2)
    axes[2, 0].set_xlabel('Time (years)')
    axes[2, 0].set_ylabel('Delta')
    axes[2, 0].set_title('Delta vs Time')
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)

    # Vega vs Time
    axes[2, 1].plot(time_df['T'], time_df['Call_Vega'], 'b-', linewidth=2.5, label='Call')
    axes[2, 1].plot(time_df['T'], time_df['Put_Vega'], 'r-', linewidth=2.5, label='Put')
    axes[2, 1].axvline(x=T, color='green', linestyle='--', linewidth=2)
    axes[2, 1].set_xlabel('Time (years)')
    axes[2, 1].set_ylabel('Vega')
    axes[2, 1].set_title('Vega vs Time')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    S, K, T, r, sigma = 175.0, 180.0, 0.25, 0.05, 0.25

    print("=" * 60)
    print("Option Greeks Analysis")
    print(f"S=${S:.2f}, K=${K:.2f}, T={T:.2f}, r={r:.2%}, σ={sigma:.2%}")

    greeks_df = greeks_summary(S, K, T, r, sigma)
    print(f"\nGreeks Summary:")
    print(greeks_df.to_string(index=False))

    print(f"\nAnalyzing Greeks across strikes and time...")
    strikes_df = analyze_greeks_strikes(S, T, r, sigma)
    time_df = analyze_greeks_time(S, K, r, sigma)

    plot_greeks(strikes_df, time_df, S, K, T)

    strikes_df.to_csv('data/greeks_vs_strike.csv', index=False)
    time_df.to_csv('data/greeks_vs_time.csv', index=False)
    greeks_df.to_csv('data/greeks_summary.csv', index=False)
    print(f"\nSaved results")
