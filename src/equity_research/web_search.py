#from duckduckgo_search import DDGS
from ddgs import DDGS

 

def web_search(ticker):
    queries = [
        f"{ticker} stock analysis",
        f"{ticker} earnings outlook",
        f"{ticker} risks controversy",
    ]

    results = []
    with DDGS() as ddgs:
        for q in queries:
            search_results = ddgs.text(q, max_results=5)
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