"""
    I have produced a cointegrated pairs file without counting the average number of crossings 
    so I am doing it here 
"""

import os
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

folder_location = 'C:\stocks\stocks'

def adjust_sizes(X, Y):
        
    smaller = min(len(X), len(Y))
    X = X[-smaller:]
    Y = Y[-smaller:]
    return X, Y

def load_stock_to_df(stockname):

    file_path = os.path.join(folder_location, stockname + '.csv')
    df = pd.read_csv(file_path)

    df['d'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('d', inplace=True)

    df['c'].interpolate()

    return df

def calculate_crossings(stock1, stock2):
    """
        relative to the `min(len(stock1), len(stock2))`
    """

    df1 = load_stock_to_df(stock1)
    df2 = load_stock_to_df(stock2)

    Y = df1['c']
    X = df2['c']

    X, Y = adjust_sizes(X, Y)
    X, Y = list(X), list(Y)

    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    beta = model.params[1]
    X, Y = np.array(X)[:, 1], np.array(Y)
    # spread = Y / (beta * X) # how would i interpret zero crossings in this scenario? 
    spread = Y - (beta * X) 

    spread = (spread - np.mean(spread)) / np.std(spread)

    crossings = 0
    prev_spread_value = spread[0]
    for spread_value in spread[1:]:
        if spread_value * prev_spread_value < 0:
            crossings += 1
        prev_spread_value = spread_value

    # print(crossings, len(X))

    return crossings / len(X)

def crossings_ranking(pairs_file):

    pairs_csv = pd.read_csv(pairs_file)

    pairs = []

    for index, row in pairs_csv.iterrows():

        # if index > 5: break

        stock1 = row['stock1'].strip()
        stock2 = row[' stock2'].strip()
        p_value = row[' p_value']

        crossings = calculate_crossings(stock1, stock2)

        pairs.append((stock1, stock2, p_value, crossings))

        print(f"{index / (pairs_csv.size / 3) * 100:.2f}%")
        
    with open('sigg_pairs_ranked_by_crossings.csv', 'w') as f:
        f.write("stock1, stock2, p_value, crossings\n")
            
        for stock1, stock2, p_value, crossings in sorted(pairs, key=lambda x: -x[3]):
            f.write(f"{stock1}, {stock2}, {p_value}, {crossings}\n")

if __name__ == '__main__':
    pairs_file = 'sigg_cointegrated_pairs.csv'
    crossings_ranking(pairs_file)
