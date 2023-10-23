import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import os

number_of_best = 1000
folder_location = 'C:\stocks\stocks'

def load_and_process_csv(stock_name):
    path = os.path.join(folder_location, stock_name + '.csv')
    df = pd.read_csv(path)

    df['d'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('d', inplace=True)

    df['c'].interpolate()

    return df

def adjust_sizes(X, Y):
        
    smaller = min(len(X), len(Y))
    X = X[-smaller:]
    Y = Y[-smaller:]
    return X, Y

pairs = pd.read_csv("pairs/sigg_pairs_ranked_by_crossings.csv")

for index, row in pairs[:number_of_best].iterrows():

    stock1, stock2, p_value, crossings = row['stock1'], row[' stock2'], row[' p_value'], row[' crossings']

    fig, axis = plt.subplots(2, 1, figsize=(12, 6))

    df1 = load_and_process_csv(stock1.strip())
    df2 = load_and_process_csv(stock2.strip())

    axis[0].plot(df1['c'], label=stock1)
    ax2 = axis[0].twiny()
    axis[0].plot(df2['c'], label=stock2)
    axis[0].legend()

    S1 = np.array(df1['c'])
    S2 = np.array(df2['c'])
    S1, S2 = adjust_sizes(S1, S2)
    model = sm.OLS(list(S2), sm.add_constant(list(S1))).fit()
    beta = model.params[1]

    Y = S1 - beta * S2
    Z_score = (Y - np.mean(Y)) / np.std(Y)

    smallerdf = df1 if len(df1['c']) < len(df2['c']) else df2

    dates = pd.to_datetime(smallerdf['t'], unit='s')
    axis[1].plot(dates, Z_score, color='green', label='Spread')
    axis[1].axhline(0, color='black')
    axis[1].set_xlabel('Date')
    axis[1].legend()

    plt.title(f"pair {str(index)}")
    plt.show()