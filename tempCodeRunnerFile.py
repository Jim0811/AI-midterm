
# # identify trend
# plt.figure(figsize=(14, 7))
# for ticker in tickers:
#     plt.plot(combined_data[f'{ticker}_30MA'], label=f'{ticker} 30日均線')
#     plt.plot(combined_data[f'{ticker}_90MA'], label=f'{ticker} 90日均線')
# plt.title('均線趨勢識別')
# plt.xlabel('日期')
# plt.ylabel('價格')
# plt.legend()
# plt.show()

# # seasonal patterns
# combined_data['Month'] = combined_data.index.month
# monthly_returns = combined_data.groupby('Month')[[f'{ticker}_Returns' for ticker in tickers]].mean()

# plt.figure(figsize=(12, 6))
# for i, ticker in enumerate(tickers, 1):
#     plt.plot(monthly_returns.index, monthly_returns[f'{ticker}_Returns'], label=f'{ticker}')
# plt.title('股票月度回報（季節性模式）')
# plt.xlabel('月份')
# plt.ylabel('平均回報')
# plt.legend()
# plt.show()

# # correlations
# close_data = combined_data[[f'{ticker}_Close' for ticker in tickers]]
# correlation_matrix = close_data.corr()
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
# plt.title('相關係數矩陣')
# plt.show()

# # Volatility
# plt.figure(figsize=(14, 7))
# for ticker in tickers:
#     volatility = combined_data[f'{ticker}_Returns'].rolling(window=30).std()
#     plt.plot(volatility, label=f'{ticker} 波動性 (30日)')
# plt.title('股票波動性')
# plt.xlabel('日期')
# plt.ylabel('波動性')
# plt.legend()
# plt.show()

# # Momentum Indicator
# plt.figure(figsize=(14, 7))
# for ticker in tickers:
#     momentum = combined_data[f'{ticker}_Close'] - combined_data[f'{ticker}_Close'].shift(10)
#     plt.plot(momentum, label=f'{ticker} 動能 (10日)')
# plt.title('股票動能指標')
# plt.xlabel('日期')
# plt.ylabel('動能')
# plt.legend()
# plt.show()
