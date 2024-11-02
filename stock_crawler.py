import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 可換成其他支援中文的字體
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示問題

# 設定股票代號
tickers = ["TSLA", "AAPL", "GOOGL", "MSFT"]
combined_data = pd.DataFrame()

# 收集數據
for ticker in tickers:
    data = yf.Ticker(ticker).history(start='2011-01-01', end='2024-01-01')
    data.columns = [f"{ticker}_{col}" for col in data.columns]
    combined_data = pd.concat([combined_data, data], axis=1)
    
    # 計算移動平均線和每日回報
    combined_data[f'{ticker}_30MA'] = combined_data[f'{ticker}_Close'].rolling(window=30).mean()
    combined_data[f'{ticker}_90MA'] = combined_data[f'{ticker}_Close'].rolling(window=90).mean()
    combined_data[f'{ticker}_Returns'] = combined_data[f'{ticker}_Close'].pct_change()
    
# 將數據保存為CSV檔案
combined_data.to_csv('stock_data.csv')

# 處理缺失值
combined_data = combined_data.ffill()

# 清洗數據，移除離群值
numeric_data = combined_data.select_dtypes(include='number')
z_scores = stats.zscore(numeric_data)
filtered_entries = (abs(z_scores) < 3).all(axis=1)
cleaned_data = combined_data[filtered_entries]

# 繪製股票價格走勢
plt.figure(figsize=(14, 7))
for ticker in tickers:
    plt.plot(combined_data[f'{ticker}_Close'], label=ticker)
plt.title('股票價格走勢')
plt.xlabel('日期')
plt.ylabel('價格')
plt.legend()
plt.show()

# 計算相關係數矩陣並繪製熱圖
close_data = combined_data[[f'{ticker}_Close' for ticker in tickers]]
correlation_matrix = close_data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('相關係數矩陣')
plt.show()

# 獲取P/E比率
for ticker in tickers:
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info.get("trailingPE")
    if pe_ratio is not None:
        print(f"{ticker} P/E 比率: {pe_ratio}")
    else:
        print(f"{ticker} 的 P/E 比率資料不可用")

# 計算波動性（Volatility）
plt.figure(figsize=(14, 7))
for ticker in tickers:
    volatility = combined_data[f'{ticker}_Returns'].rolling(window=30).std()
    plt.plot(volatility, label=f'{ticker} 波動性 (30日)')
plt.title('股票波動性')
plt.xlabel('日期')
plt.ylabel('波動性')
plt.legend()
plt.show()

# 計算動能指標（Momentum Indicator）
plt.figure(figsize=(14, 7))
for ticker in tickers:
    momentum = combined_data[f'{ticker}_Close'] - combined_data[f'{ticker}_Close'].shift(10)
    plt.plot(momentum, label=f'{ticker} 動能 (10日)')
plt.title('股票動能指標')
plt.xlabel('日期')
plt.ylabel('動能')
plt.legend()
plt.show()

# 趨勢識別（Trend Identification）使用均線交叉策略
plt.figure(figsize=(14, 7))
for ticker in tickers:
    plt.plot(combined_data[f'{ticker}_30MA'], label=f'{ticker} 30日均線')
    plt.plot(combined_data[f'{ticker}_90MA'], label=f'{ticker} 90日均線')
plt.title('均線趨勢識別')
plt.xlabel('日期')
plt.ylabel('價格')
plt.legend()
plt.show()

# 季節性模式（Seasonal Patterns）分析
combined_data['Month'] = combined_data.index.month
monthly_returns = combined_data.groupby('Month')[[f'{ticker}_Returns' for ticker in tickers]].mean()

plt.figure(figsize=(12, 6))
for i, ticker in enumerate(tickers, 1):
    plt.plot(monthly_returns.index, monthly_returns[f'{ticker}_Returns'], label=f'{ticker}')
plt.title('股票月度回報（季節性模式）')
plt.xlabel('月份')
plt.ylabel('平均回報')
plt.legend()
plt.show()
