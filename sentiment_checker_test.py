import requests as re
import statistics as stats

def get_sentiment(tweet):
    """
    Helper function that extracts the sentiment of each tweet
    1 = positive
    0 = negative 
    """
    # Do the API request (Stanford Sentiment)
    r = re.post(
        "https://api.deepai.org/api/sentiment-analysis",
        data={
            'text': tweet,
        },
        headers={'api-key': 'ca26882d-52af-4903-b0f7-571801ebd67a'}
    )

    # Get only the output array. Each sentence has its own sentiments
    result = r.json()["output"]

    # Map strings to integers helper function
    def classify(sentiment):
        sentiment = sentiment.lower()
        if sentiment == "verynegative":
            return -2
        elif sentiment == "negative":
            return -1
        elif sentiment == "positive":
            return 1
        elif sentiment == "verypositive":
            return 2
        else:
            return 0

    # Map strings to integers helper function
    result = list( map(classify, result))

    # Calculate the entire
    result = stats.mean(result)
    
    return 1 if result >= 0 else 0





result = get_sentiment("I hate tesla so much. I hate it")
print(result)