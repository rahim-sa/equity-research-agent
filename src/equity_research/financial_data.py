# ﻿import yfinance as yf


# def get_financial_data(ticker):
#     stock = yf.Ticker(ticker)
#     info = stock.info
#     hist = stock.history(period="1y")

#     start_price = hist["Close"].iloc[0]
#     end_price = hist["Close"].iloc[-1]
#     perf_1y = round(((end_price - start_price) / start_price) * 100, 1)

#     return f"""
# Name: {info["longName"]}
# Sector: {info["sector"]}
# Industry: {info["industry"]}
# Price: {info["currentPrice"]}
# 1-Year Performance: {perf_1y}%
# Market Cap: {info["marketCap"]}
# Trailing P/E: {info["trailingPE"]}
# Forward P/E: {info["forwardPE"]}
# Profit Margin: {info["profitMargins"]}
# Revenue Growth: {info["revenueGrowth"]}
# Debt/Equity: {info["debtToEquity"]}
# Dividend Yield: {info["dividendYield"]}
# """


# if __name__ == "__main__":
#     print(get_financial_data("AAPL"))


import yfinance as yf


def get_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
    except Exception as e:
        return f"Could not retrieve data for '{ticker}': {e}"

    if not info or info.get("longName") is None:
        return f"No financial data found for '{ticker}'. It may be an invalid ticker."

    hist = stock.history(period="1y")
    if hist.empty or len(hist) < 2:
        perf_1y = "N/A"
    else:
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]
        perf_1y = f"{round(((end_price - start_price) / start_price) * 100, 1)}%"

    return f"""
Name: {info["longName"]}
Sector: {info["sector"]}
Industry: {info["industry"]}
Price: {info["currentPrice"]}
1-Year Performance: {perf_1y}
Market Cap: {info["marketCap"]}
Trailing P/E: {info["trailingPE"]}
Forward P/E: {info["forwardPE"]}
Profit Margin: {info["profitMargins"]}
Revenue Growth: {info["revenueGrowth"]}
Debt/Equity: {info["debtToEquity"]}
Dividend Yield: {info["dividendYield"]}
"""


if __name__ == "__main__":
    print(get_financial_data("AAPL"))
    print(get_financial_data("NOTAREALTICKERXYZ"))