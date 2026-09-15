import yfinance as yf


def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    return f"""
Name: {info["longName"]}
Sector: {info["sector"]}
Industry: {info["industry"]}
Price: {info["currentPrice"]}
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