from textblob import TextBlob


def extract_sentiment(text):
    """
    Classify sentiment polarity and subjectivity parameters for given text fragment
    :param text:
    :return:
    """
    # text blob to
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity
