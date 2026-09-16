from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = ddgs.text("AAPL stock analysis", max_results=5)
    for r in results:
        print(r["title"])
        print(r["href"])
        print(r["body"])
        print("---")