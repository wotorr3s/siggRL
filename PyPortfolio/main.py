import pandas as pd
from PyPortfolioOpt.pypfopt.efficient_frontier import EfficientFrontier
from PyPortfolioOpt.pypfopt import risk_models
from PyPortfolioOpt.pypfopt import expected_returns
import os

# Read in price data
dfs={}
files = os.listdir("../data/all/stocks/")
def load_and_process_csv(file_path):
    df = pd.read_csv(file_path)

    df['d'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('d', inplace=True)

    df['c'].interpolate()
    return df

for file in files:
    print(file)
    dfs[file]=load_and_process_csv("../data/all/stocks/"+file)

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(dfs)
S = risk_models.sample_cov(dfs)

# Optimize for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
ef.portfolio_performance(verbose=True)