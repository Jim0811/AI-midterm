import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

tickers = ["TSLA", "AAPL", "GOOGL", "MSFT"]
combined_data = pd.DataFrame()

# collect data
for ticker in tickers:
    data = yf.Ticker(ticker).history(start='2011-01-01', end='2024-01-01')
    data.columns = [f"{ticker}_{col}" for col in data.columns]
    combined_data = pd.concat([combined_data, data], axis=1)
    #moving average,daily returns
    combined_data[f'{ticker}_30MA'] = combined_data[f'{ticker}_Close'].rolling(window=30).mean()
    combined_data[f'{ticker}_90MA'] = combined_data[f'{ticker}_Close'].rolling(window=90).mean()
    combined_data[f'{ticker}_Returns'] = combined_data[f'{ticker}_Close'].pct_change()
    

combined_data.to_csv('stock_data.csv')

# handling missing value
combined_data = combined_data.ffill()

# cleaned data? clean all data?????
numeric_data = combined_data.select_dtypes(include='number')
z_scores = stats.zscore(numeric_data)
filtered_entries = (abs(z_scores) < 3).all(axis=1)
cleaned_data = combined_data[filtered_entries]

# stock prices
plt.figure(figsize=(14, 7))
for ticker in tickers:
    plt.plot(combined_data[f'{ticker}_Close'], label=ticker)
plt.title('Stock Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# correlation
close_data = combined_data[[f'{ticker}_Close' for ticker in tickers]]
correlation_matrix = close_data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# p/e ratio unfinished
for ticker in tickers:
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info.get("trailingPE")
    if pe_ratio is not None:
        print(f"{ticker} P/E Ratio: {pe_ratio}")
    else:
        print(f"{ticker} P/E Ratio data not available")


##################################unfinished##################################
#volatility
#momentum indicator
#identify trend
#seasonal patterns

