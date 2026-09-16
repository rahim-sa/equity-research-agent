# from textblob import TextBlob

# text = "Apple beat earnings expectations and raised guidance for next quarter."
# blob = TextBlob(text)
# print(blob.sentiment)


from textblob import TextBlob


def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.15:
        label = "Positive"
    elif polarity < -0.15:
        label = "Negative"
    else:
        label = "Neutral"

    return {"polarity": round(polarity, 3), "label": label}


if __name__ == "__main__":
    print(analyze_sentiment("Apple beat earnings expectations and raised guidance."))
    print(analyze_sentiment("The company missed on revenue and cut its outlook."))