
from textblob import TextBlob


_FINBERT_PIPELINE = None
_FINBERT_WARNED = False


def _get_finbert():
    global _FINBERT_PIPELINE, _FINBERT_WARNED
    if _FINBERT_PIPELINE is not None:
        return _FINBERT_PIPELINE

    try:
        from transformers import pipeline
        _FINBERT_PIPELINE = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        return _FINBERT_PIPELINE
    except Exception:
        if not _FINBERT_WARNED:
            print("  ! FinBERT unavailable, falling back to TextBlob.")
            _FINBERT_WARNED = True
        return None


uv run python -c "
from transformers import pipeline
finbert = pipeline('sentiment-analysis', model='ProsusAI/finbert')
print(finbert('The company missed on revenue and cut its outlook.'))
print(finbert('Apple beat earnings expectations and raised guidance.'))
"


def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.15:
        label = "Positive"
    elif polarity < -0.15:
        label = "Negative"
    else:
        label = "Neutral"

    return {"polarity": round(polarity, 3), "label": label}


def summarize_sentiment(search_results):
    sentiments = [
        analyze_sentiment(f"{r['title']}. {r['snippet']}")
        for r in search_results
    ]

    avg_polarity = sum(s["polarity"] for s in sentiments) / len(sentiments)
    positive = sum(1 for s in sentiments if s["label"] == "Positive")
    negative = sum(1 for s in sentiments if s["label"] == "Negative")
    neutral = sum(1 for s in sentiments if s["label"] == "Neutral")

    if avg_polarity > 0.15:
        overall = "Positive"
    elif avg_polarity < -0.15:
        overall = "Negative"
    else:
        overall = "Neutral"

    return {
        "overall": overall,
        "avg_polarity": round(avg_polarity, 3),
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
    }


# if __name__ == "__main__":
#     fake_results = [
#         {"title": "Apple beats earnings", "snippet": "Strong quarter, raised guidance."},
#         {"title": "Apple faces lawsuit", "snippet": "Regulatory pressure mounts in EU."},
#         {"title": "Apple stock steady", "snippet": "Shares unchanged after mixed report."},
#     ]
#     print(summarize_sentiment(fake_results))

if __name__ == "__main__":
    from equity_research.web_search import web_search

    results = web_search("AAPL")
    print(summarize_sentiment(results))