import yfinance as yf


def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1y")

    start_price = hist["Close"].iloc[0]
    end_price = hist["Close"].iloc[-1]
    perf_1y = round(((end_price - start_price) / start_price) * 100, 1)

    return f"""
Name: {info["longName"]}
Sector: {info["sector"]}
Industry: {info["industry"]}
Price: {info["currentPrice"]}
1-Year Performance: {perf_1y}%
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