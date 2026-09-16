#from duckduckgo_search import DDGS
from ddgs import DDGS

with DDGS() as ddgs:
    results = ddgs.text("AAPL stock analysis", max_results=5)
    for r in results:
        print(r["title"])
        print(r["href"])
        print(r["body"])
        print("---")

#from duckduckgo_search import DDGS


def web_search(ticker):
    results = []
    with DDGS() as ddgs:
        search_results = ddgs.text(f"{ticker} stock analysis", max_results=5)
        for r in search_results:
            results.append({
                "title": r["title"],
                "snippet": r["body"],
                "link": r["href"],
            })
    return results


if __name__ == "__main__":
    for r in web_search("AAPL"):
        print(r["title"])
        print(r["link"])
        print("---")