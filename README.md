AAPL Quantitative Finance Analysis
A Quantitative Framework for Market Behaviour, Volatility, Risk, and Options Analysis
Prepared by: Sia Luthra | Date: August 2026
1. Project Overview
This project is an independent quantitative finance analysis of Apple Inc. (AAPL) common stock, built
entirely in Python. It applies statistical analysis, stochastic price simulation, volatility modelling, portfolio
risk estimation, and options pricing to approximately two years of historical AAPL market data. The work
is exploratory and academic in nature — it is a modelling and analysis exercise rather than a live trading,
forecasting, or investment-advisory system.
2. Objective
The objective of the project was to build a structured, end-to-end quantitative pipeline that could take
raw historical stock data and progressively answer a series of increasingly advanced questions:
• How has AAPL's stock price behaved historically, and how are its daily returns distributed?
• What range of future price paths is plausible, given AAPL's historical drift and volatility?
• Does AAPL's volatility remain constant over time, or does it cluster into calm and turbulent periods?
• For a hypothetical portfolio, how much capital could realistically be at risk under adverse
conditions?
• How can an AAPL-linked option be valued, and how sensitive is that value to changes in market
conditions?
3. Methodology
The analysis followed a sequential, modular pipeline, with each stage building on the outputs of the
previous one:
• Data collection and cleaning — sourcing and preparing historical AAPL price and volume data.
• Return-distribution analysis — computing daily log returns and testing their statistical properties.
• Price-path simulation — modelling possible future price trajectories using Geometric Brownian
Motion (GBM).
• Volatility modelling — estimating how volatility evolves over time using a GARCH(1,1) model.
• Portfolio risk estimation — running Monte Carlo simulations to estimate potential portfolio losses.
• Options analysis — pricing a representative European option using the Black–Scholes formula and
Monte Carlo simulation, and calculating its sensitivity measures (the Option Greeks).
4. Tools and Technologies
The project was implemented as a Python-based codebase comprising 8 modules and over 2,000 lines of
code. Key libraries used include:
Category Tools / Libraries
Programming language Python
Numerical computing NumPy, SciPy
Data handling Pandas
Volatility modelling ARCH
Visualization Matplotlib, Seaborn
Data source Yahoo Finance
5. Analysis, Models, and Methods Applied
5.1 Data and Return Distribution Analysis
Approximately two years of daily AAPL data — 499 trading days, from 26 August 2024 to 21 August 2026
— was collected from Yahoo Finance, covering opening price, closing price, high, low, and trading volume.
Daily log returns were calculated and their statistical distribution was analysed to understand how AAPL's
price typically moves.
The analysis found that AAPL's returns exhibit fat tails: most trading days show relatively small price
movements, but occasional large moves occur more frequently than a standard (normal) distribution
would predict. This has a direct implication for risk management, since it means extreme events cannot
be treated as negligibly rare.
5.2 Price Simulation — Geometric Brownian Motion (GBM)
GBM was used to generate 1,000 simulated possible future price paths for AAPL over a one-year horizon,
based on the stock's estimated annualized drift and volatility. Rather than producing a single predicted
price, this approach produces a distribution of plausible outcomes, ranging from strong upward paths to
declines and periods of high volatility.
5.3 Volatility Modelling — GARCH(1,1)
A GARCH(1,1) model was applied to test whether AAPL's volatility is constant or clusters over time. The
results showed clear evidence of volatility clustering — periods of high volatility tend to be followed by
further high volatility, and calm periods tend to persist as well — with an estimated volatility persistence
of approximately 90%. This indicates that risk levels for AAPL are not static and should be reassessed
dynamically rather than assumed constant.
5.4 Portfolio Risk Estimation — Monte Carlo, VaR, and Expected Shortfall
To translate the return and volatility findings into a practical risk measure, 10,000 Monte Carlo simulations
were run for a hypothetical $100,000 portfolio. Two standard risk metrics were estimated:
• Value at Risk (VaR) — a threshold loss level that is not expected to be exceeded at a given
confidence level over one day.
• Expected Shortfall (ES) — the average loss expected in the scenarios where losses exceed the VaR
threshold.
5.5 Options Analysis — Black–Scholes, Monte Carlo Pricing, and the Greeks
The project also analysed a representative European option using both the Black–Scholes analytical
formula and a 100,000-path Monte Carlo simulation. It is worth noting that this option example used
illustrative parameters (a stock price of $175 and strike price of $180) rather than the simulated AAPL
price levels used in the GBM analysis; it should be read as a separate, self-contained demonstration of
options-pricing methodology rather than a live valuation of an AAPL option at current price levels.
In addition to pricing the option, the Option Greeks — Delta, Gamma, Vega, Theta, and Rho — were
calculated to assess how the option's value would respond to changes in the underlying stock price,
volatility, time to expiry, and interest rates respectively.
6. Key Results and Findings
6.1 Return Distribution Statistics
Metric Value
Average daily return 0.0637%
Daily volatility 1.81%
Kurtosis 10.23
Normality test result p < 0.001 (significant deviation from normal
distribution)
Minimum daily return −9.70%
Maximum daily return +14.26%
6.2 GBM Simulation Parameters
Parameter Value
Starting price $309.35
Annualized drift 15.89%
Annualized volatility 28.76%
Parameter Number of simulated paths Simulation horizon Value
1,000
1 year
6.3 GARCH(1,1) Volatility Parameters
Parameter Value
α (alpha) 0.10
β (beta) 0.80
Volatility persistence (α + β) ≈ 0.90
Metric 1-Day Estimate
95% Value at Risk (VaR) $188.42
99% Value at Risk (VaR) $264.22
95% Expected Shortfall (ES) $236.30
99% Expected Shortfall (ES) $307.03
6.4 Portfolio Risk Metrics (Monte Carlo, $100,000 portfolio)
These figures should be read as model-based estimates under the specified assumptions and simulation parameters,
not as guarantees of maximum possible loss.
6.5 Option Pricing Results (Illustrative Example)
Input parameters: stock price $175, strike price $180, time to expiry 0.25 years, risk-free rate 5%, volatility
25%.
Option Type Monte Carlo Estimated Price Probability of Finishing In-the-
Money
Call option $7.4973 42.54%
Put option $10.2378 57.46%
The Option Greeks (Delta, Gamma, Vega, Theta, Rho) were also calculated for this example to characterise
the option's sensitivity to the underlying price, volatility, time decay, and interest rates. Specific Greek
values were not finalised in the source material and are therefore not reported numerically here.
7. Practical and Real-World Relevance
While the project does not forecast AAPL's future price, the techniques and outputs are directly relevant
to several finance-related roles and functions:
• Portfolio managers — assessing asset volatility, plausible return scenarios, and overall risk exposure.
• Risk management teams — quantifying potential losses using VaR, Expected Shortfall, and volatility
modelling.
• Quantitative analysts — combining mathematics, statistics, finance, and programming to analyse
market behaviour.
• Quantitative researchers — testing whether mathematical models can meaningfully represent real
market behaviour.
• Derivatives and options teams — applying Black–Scholes and Monte Carlo methods to price options
and assess sensitivity to market changes.
8. My Specific Contribution
I independently designed and built the full analytical pipeline described in this document. This included:
• Sourcing, cleaning, and preparing approximately two years of daily AAPL market data from Yahoo
Finance.
• Conducting return-distribution analysis, including calculation of volatility, kurtosis, and normality
diagnostics.
• Implementing Geometric Brownian Motion simulation to generate 1,000 possible future price paths.
• Implementing a GARCH(1,1) model to estimate and interpret volatility clustering and persistence.
• Running Monte Carlo simulations to estimate portfolio-level Value at Risk and Expected Shortfall.
• Implementing Black–Scholes and Monte Carlo option pricing, and calculating the associated Option
Greeks.
• Writing the full codebase (8 Python modules, 2,000+ lines) using NumPy, Pandas, SciPy, ARCH,
Matplotlib, and Seaborn.
9. Limitations
• The analysis is based on approximately two years of historical daily data and does not incorporate
intraday data, macroeconomic indicators, or company-specific fundamental data.
• GBM and GARCH are established quantitative models but rely on simplifying assumptions (e.g.,
constant drift in GBM) that may not hold under all market conditions.
• VaR and Expected Shortfall are model-based estimates under stated assumptions; actual losses in
adverse market conditions could differ from these estimates.
• The options-pricing example uses illustrative input parameters that are independent of the
simulated AAPL price levels used elsewhere in the project, and should not be interpreted as a live
or current option valuation.
• The project is an academic and analytical exercise; it is not a predictive, automated, or production-
deployed trading or investment system.

10. Conclusion
This project demonstrates the application of core quantitative finance techniques — return-distribution
analysis, stochastic price simulation, volatility modelling, Monte Carlo risk estimation, and options pricing
to two years of real AAPL market data. Rather than predicting a single future price, the analysis
characterises the range of plausible outcomes, quantifies how AAPL's volatility evolves over time,
estimates potential portfolio losses under a defined set of assumptions, and values a representative
options contract along with its market sensitivities. Together, these components illustrate the use of
mathematics, statistics, and programming to analyse market uncertainty and risk in a manner relevant to
portfolio management, risk analysis, quantitative research, and derivatives valuatio
