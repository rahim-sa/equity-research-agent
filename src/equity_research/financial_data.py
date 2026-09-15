import yfinance as yf


def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    return f"""
Name: {info["longName"]}
Sector: {info["sector"]}
Price: {info["currentPrice"]}
Market Cap: {info["marketCap"]}
P/E: {info["trailingPE"]}
"""


if __name__ == "__main__":
    print(get_financial_data("AAPL"))