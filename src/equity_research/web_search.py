#from duckduckgo_search import DDGS
from ddgs import DDGS

 

# def web_search(ticker):
#     queries = [
#         f"{ticker} stock analysis",
#         f"{ticker} earnings outlook",
#         f"{ticker} risks controversy",
#     ]

#     results = []
#     with DDGS() as ddgs:
#         for q in queries:
#             search_results = ddgs.text(q, max_results=5)
#             for r in search_results:
#                 results.append({
#                     "title": r["title"],
#                     "snippet": r["body"],
#                     "link": r["href"],
#                 })
#     return results


# if __name__ == "__main__":
#     for r in web_search("AAPL"):
#         print(r["title"])
#         print(r["link"])
#         print("---")

#from duckduckgo_search import DDGS

TRUSTED_DOMAINS = [
    "reuters.com", "bloomberg.com", "wsj.com", "ft.com",
    "cnbc.com", "marketwatch.com", "seekingalpha.com",
    "barrons.com", "forbes.com", "businessinsider.com",
]

LOW_QUALITY_MARKERS = ["reddit", "forum", "comment", "blog"]


def score_result(result, ticker):
    score = 0.0
    link = result["link"].lower()
    title = result["title"].lower()
    snippet = result["snippet"].lower()

    if any(domain in link for domain in TRUSTED_DOMAINS):
        score += 3.0
    else:
        score += 0.5

    if ticker.lower() in title or ticker.lower() in snippet:
        score += 1.5

    for marker in LOW_QUALITY_MARKERS:
        if marker in link or marker in title:
            score -= 1.5

    return score


def web_search(ticker):
    queries = [
        f"{ticker} stock analysis",
        f"{ticker} earnings outlook",
        f"{ticker} risks controversy",
    ]

    results = []
    # with DDGS() as ddgs:
    #     for q in queries:
    #         search_results = ddgs.text(q, max_results=5)
    #         for r in search_results:
    #             results.append({
    #                 "title": r["title"],
    #                 "snippet": r["body"],
    #                 "link": r["href"],
    #             })

    with DDGS() as ddgs:
        for q in queries:
            try:
                search_results = ddgs.text(q, max_results=5)
            except Exception as e:
                print(f"  ! search failed for query '{q}': {e}")
                continue
            for r in search_results:
                results.append({
                    "title": r["title"],
                    "snippet": r["body"],
                    "link": r["href"],
                })


    


      # with DDGS() as ddgs:
      #   for q in queries:
      #       search_results = ddgs.text(q, max_results=5)
      #       for r in search_results:
      #           results.append({
      #               "title": r["title"],
      #               "snippet": r["body"],
      #               "link": r["href"],
      #           })  

    # for r in results:
    #     r["score"] = round(score_result(r, ticker), 1)

    # results.sort(key=lambda r: r["score"], reverse=True)
    # return results

    ### New change
    for r in results:
        r["score"] = round(score_result(r, ticker), 1)

    results.sort(key=lambda r: r["score"], reverse=True)
    filtered = [r for r in results if r["score"] >= 2.0]
    return filtered[:8]



def format_search_results(results):
    if not results:
        return "No search results available."

    formatted = ""
    for r in results:
        formatted += f"[{r['score']}] {r['title']}\n"
        formatted += f"{r['snippet']}\n"
        formatted += f"Source: {r['link']}\n"
        formatted += "-" * 40 + "\n"
    return formatted


if __name__ == "__main__":
    for r in web_search("AAPL"):
        print(f"[{r['score']}] {r['title']}")
        print(r["link"])
        print("---")