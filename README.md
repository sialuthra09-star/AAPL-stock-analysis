AAPL Quantitative Finance Analysis
A comprehensive quantitative finance project analyzing Apple Inc. (AAPL) stock using modern financial modeling techniques.

Project Structure
text
AAPL-Quantitative-Finance/
│
├── README.md
├── requirements.txt
│
├── 01_data_collection.py      # Download AAPL data (last 2 years)
├── 02_log_return_analysis.py  # Log return calculations
├── 03_gbm_sde.py              # Geometric Brownian Motion
├── 04_garch_volatility.py     # GARCH volatility modeling
├── 05_monte_carlo_risk.py     # Monte Carlo VaR
├── 06_black_scholes.py        # Black-Scholes pricing
├── 07_monte_carlo_option.py   # Monte Carlo option pricing
├── 08_greeks.py               # Option Greeks
│
├── data/                      # Downloaded and processed data
└── results/                   # Output visualizations
Installation
bash
pip install -r requirements.txt
Usage
Run scripts in order:

bash
python 01_data_collection.py
python 02_log_return_analysis.py
python 03_gbm_sde.py
python 04_garch_volatility.py
python 05_monte_carlo_risk.py
python 06_black_scholes.py
python 07_monte_carlo_option.py
python 08_greeks.py
Key Features
Data Collection: Fetch historical AAPL data from Yahoo Finance

Return Analysis: Log return calculations and distribution analysis

GBM Simulation: Stock price path simulation using SDE

Volatility Modeling: GARCH(1,1) for time-varying volatility

Risk Analysis: Monte Carlo VaR and expected shortfall

Option Pricing: Black-Scholes and Monte Carlo methods

Greeks: Delta, Gamma, Vega, Theta, Rho calculations

Requirements
Python 3.8+

See requirements.txt for dependencies

Author
Sia Luthra
