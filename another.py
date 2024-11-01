import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 定義公司代碼列表
tickers = ["2330.TW", "AAPL", "GOOGL", "MSFT"]  # 台積電、Apple、Google、Microsoft

# 創建空的 DataFrame 來存放所有公司的日交易資料
all_data = pd.DataFrame()

# 下載每家公司的歷史資料，並合併到同一 DataFrame 中
for ticker in tickers:
    # 下載包括開盤、最高、最低和收盤價的資料
    data = yf.Ticker(ticker).history(period="max")[['Open', 'High', 'Low', 'Close']]
    # 在欄位名稱中加入公司代碼，便於區分
    data.columns = [f"{ticker}_{col}" for col in data.columns]
    # 按日期合併所有公司的資料
    all_data = pd.concat([all_data, data], axis=1)

# 檢查資料
print(all_data.head())

# 計算收盤價的移動平均線和收益率
for ticker in tickers:
    # 50日移動平均線
    all_data[f'{ticker}_30MA'] = all_data[f'{ticker}_Close'].rolling(window=30).mean()
    # 200日移動平均線
    all_data[f'{ticker}_90MA'] = all_data[f'{ticker}_Close'].rolling(window=90).mean()
    # 日收益率
    all_data[f'{ticker}_Returns'] = all_data[f'{ticker}_Close'].pct_change()
all_data.to_csv("stock_data2.csv")