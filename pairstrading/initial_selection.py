"""
    It was first ran without considering GPW's ETFs and WIG20 indices
"""

import os
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

first_n = 10
p_value_threshold = 0.001
folder_location = 'C:\stocks\stocks'

def load_and_process_csv(file_path):
    df = pd.read_csv(file_path)

    df['d'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('d', inplace=True)

    df['c'].interpolate()

    return df

def adjust_sizes(X, Y):
        
    smaller = min(len(X), len(Y))
    X = X[-smaller:]
    Y = Y[-smaller:]
    return X, Y

def test_cointegration(pair):
    Y = pair[0]['c']
    X = pair[1]['c']

    X, Y = adjust_sizes(X, Y)
    X, Y = list(X), list(Y)

    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    
    p_value = sm.tsa.adfuller(model.resid)[1]
    beta = model.params[1]

    return p_value, beta

stock_files = os.listdir(folder_location)
stock_names = []
stock_dfs = []

if first_n == -1: 
    first_n = len(stock_files)

for file in stock_files[:first_n]:
    stock_names.append(os.path.splitext(file)[0])
    stock_dfs.append(load_and_process_csv(os.path.join(folder_location, file)))

cointegrated_pairs = []
betas = []

i = 0
for x, stock1 in enumerate(stock_names):
    for y, stock2 in enumerate(stock_names):
        if x >= y: continue

        p_value, beta = test_cointegration([stock_dfs[x], stock_dfs[y]])

        if p_value < p_value_threshold: 
            cointegrated_pairs.append((stock1, stock2, p_value))
            betas.append(beta)
        
        i += 1
        print(f'completed: {i / ((first_n-1) * first_n / 2) * 100:.2f}%')

    
# save the data
with open('cointegrated_pairs.csv', 'w') as f:
    f.write("stock1, stock2, p_value\n")
    i = 0
    for stock1, stock2, p_value in sorted(cointegrated_pairs, key=lambda x: x[2]):
        f.write(f"{stock1}, {stock2}, {p_value}\n")

        fig, axis = plt.subplots(2, 1, figsize=(12, 6))

        df1 = stock_dfs[stock_names.index(stock1)]
        df2 = stock_dfs[stock_names.index(stock2)]

        axis[0].plot(df1['c'], label=stock1)
        ax2 = axis[0].twiny()
        axis[0].plot(df2['c'], label=stock2)
        axis[0].legend()

        S1 = np.array(df1['c'])
        S2 = np.array(df2['c'])
        S1, S2 = adjust_sizes(S1, S2)
        beta = betas[i]

        Y = S1 - beta * S2
        Z_score = (Y - np.mean(Y)) / np.std(Y)

        smallerdf = df1 if len(df1['c']) < len(df2['c']) else df2

        dates = pd.to_datetime(smallerdf['t'], unit='s')
        axis[1].plot(dates, Z_score, color='green', label='Spread')
        axis[1].axhline(0, color='black')
        axis[1].set_xlabel('Date')
        axis[1].legend()

        # print(stock1, stock2)
        plt.show()
        plt.savefig(f'pairs/{str(i+1)}th best {stock1} and {stock2}.png')
        i += 1
