import yfinance as yf


def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    print("Name:", info["longName"])
    print("Sector:", info["sector"])
    print("Price:", info["currentPrice"])
    print("Market Cap:", info["marketCap"])
    print("P/E:", info["trailingPE"])


get_financial_data("AAPL")
