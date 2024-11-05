import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import requests

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 可換成其他支援中文的字體
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示問題

# 設定股票代號
tickers = ["TSLA", "AAPL", "GOOGL", "MSFT"]
pe_ratios = {}
combined_data = pd.DataFrame()

# data collect (trading volume)
for ticker in tickers:
    data = yf.Ticker(ticker).history(start='2011-01-01', end='2024-01-01')
    data.columns = [f"{ticker}_{col}" for col in data.columns]
    combined_data = pd.concat([combined_data, data], axis=1)
    
    # moving average, daily return
    combined_data[f'{ticker}_30MA'] = combined_data[f'{ticker}_Close'].rolling(window=30).mean()
    combined_data[f'{ticker}_90MA'] = combined_data[f'{ticker}_Close'].rolling(window=90).mean()
    combined_data[f'{ticker}_Returns'] = combined_data[f'{ticker}_Close'].pct_change()

combined_data.to_csv('stock_data.csv')

# handling missing values
combined_data = combined_data.ffill()

# handling outliers
numeric_data = combined_data.select_dtypes(include='number')
z_scores = stats.zscore(numeric_data)
filtered_entries = (abs(z_scores) < 3).all(axis=1)
cleaned_data = combined_data[filtered_entries]

################################################ p/e ratio fail #################################################
# # 加入 P/E Ratio 的計算
# api_key = '3INE4PH7GN9PIBCA'  # 請替換成你的 Alpha Vantage API 金鑰
# eps_data = {}

# for ticker in tickers:
#     # Alpha Vantage API URL
#     url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}'
#     response = requests.get(url)
#     data = response.json()
    
#     if 'annualReports' in data:
#         # 取最新年度 EPS
#         report = data['annualReports'][0]
#         if 'reportedEPS' in report:
#             latest_eps = float(report['reportedEPS'])
#             print(data)
#             eps_data[ticker] = latest_eps
#         else:
#             print(f'{ticker} 年報中未找到 EPS 欄位')
#     else:
#         print(f'{ticker} 無法獲取 EPS 數據')
#         print(data)

# # 計算並加入 P/E ratio
# for ticker in tickers:
#     if ticker in eps_data:
#         combined_data[f'{ticker}_PE_Ratio'] = combined_data[f'{ticker}_Close'] / eps_data[ticker]

# # 繪製 P/E Ratio 走勢圖
# plt.figure(figsize=(14, 7))
# for ticker in tickers:
#     if f'{ticker}_PE_Ratio' in combined_data.columns:
#         plt.plot(combined_data.index, combined_data[f'{ticker}_PE_Ratio'], label=f'{ticker} P/E Ratio')
# plt.title('股票 P/E Ratio 走勢')
# plt.xlabel('日期')
# plt.ylabel('P/E Ratio')
# plt.legend()
# plt.show()
##########################################################################################################

# data price
plt.figure(figsize=(14, 7))
for ticker in tickers:
    plt.plot(combined_data[f'{ticker}_Close'], label=ticker)
plt.title('股票價格走勢')
plt.xlabel('日期')
plt.ylabel('價格')
plt.legend()
plt.show()

# identify trend
plt.figure(figsize=(14, 7))
for ticker in tickers:
    plt.plot(combined_data[f'{ticker}_30MA'], label=f'{ticker} 30日均線')
    plt.plot(combined_data[f'{ticker}_90MA'], label=f'{ticker} 90日均線')
plt.title('均線趨勢識別')
plt.xlabel('日期')
plt.ylabel('價格')
plt.legend()
plt.show()

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

# p/e ratio
for ticker in tickers:
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info.get("trailingPE")
    if pe_ratio is not None:
        pe_ratios[ticker] = pe_ratio
        print(f"{ticker} P/E 比率: {pe_ratio}")
    else:
        print(f"{ticker} 的 P/E 比率資料不可用")
if pe_ratios:
    colors = ['blue', 'orange', 'green', 'red']
    plt.figure(figsize=(6, 6))
    plt.bar(pe_ratios.keys(), pe_ratios.values(), color=colors)
    plt.title('股票 P/E 比率')
    plt.xlabel('股票代號')
    plt.ylabel('P/E 比率')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("無可用的 P/E 比率資料來繪製圖表。")
