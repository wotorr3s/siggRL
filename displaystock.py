import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
# Replace 'your_data.csv' with the actual file path
df = pd.read_csv(r'C:\stocks\stocks\PLROPCE00017.csv')

# Convert the 't' column to datetime
df['t'] = pd.to_datetime(df['t'], unit='s')

# Sort the DataFrame by date (if it's not already sorted)
df = df.sort_values(by='t')

# Create a line plot using 'date' on the x-axis and 'close' on the y-axis
plt.figure(figsize=(12, 6))
plt.plot(df['t'], df['o'], label='Open Price', color='g')
plt.plot(df['t'], df['c'], label='Close Price', color='r')
plt.plot(df['t'], df['h'], label='High price', color='b')
plt.plot(df['t'], df['l'], label='Low price', color='m')

# You can add more data series (open, high, low) or customize the plot as needed.

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Price Data')

# Show a legend if you have multiple data series
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
