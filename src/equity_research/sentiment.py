from textblob import TextBlob

text = "Apple beat earnings expectations and raised guidance for next quarter."
blob = TextBlob(text)
print(blob.sentiment)