import yfinance as yf

stock = yf.Ticker("AAPL")
info = stock.info

print("Name:", info["longName"])
print("Sector:", info["sector"])
print("Price:", info["currentPrice"])
print("Market Cap:", info["marketCap"])
print("P/E:", info["trailingPE"])
