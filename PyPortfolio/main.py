import pandas as pd
from PyPortfolioOpt.pypfopt.efficient_frontier import EfficientFrontier
from PyPortfolioOpt.pypfopt import risk_models
from PyPortfolioOpt.pypfopt import expected_returns
import os

# Read in price data
folder_location = '../data/all/stocks/'
first_n = -1

def load_and_process_csv(file_path):
    df = pd.read_csv(file_path)

    df['d'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('d', inplace=True)

    df['c'].interpolate()

    return df
stock_files = os.listdir(folder_location)
stock_names = []
stock_dfs = []


valid_stocks = []
with open('valid_tickers.txt', 'r') as file:
    for line in file:
        clean_line = line.strip()
        valid_stocks.append(clean_line)

invalid_stocks_indices = []
for i, f in enumerate(stock_files):
    if os.path.splitext(f)[0] not in valid_stocks:
        invalid_stocks_indices.append(i)

for i in sorted(invalid_stocks_indices)[::-1]:
    del stock_files[i]

if first_n == -1: 
    first_n = len(stock_files)
    
for file in stock_files[:first_n]:
    stock_names.append(os.path.splitext(file)[0])
    stock_dfs.append(load_and_process_csv(os.path.join(folder_location, file)))

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(stock_dfs)
S = risk_models.sample_cov(stock_dfs)

# Optimize for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
ef.portfolio_performance(verbose=True)