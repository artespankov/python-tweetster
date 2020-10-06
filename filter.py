import tweepy
import datetime
import json

from sentiment.blob import extract_sentiment
from storage import TweetStore
from config.settings import TRACKED_BRANDS_LIST, RETWEET_STATUS_MARKER

storage = TweetStore()


# Override the stream listener "on status" & "on error" methods
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        # Avoid retweets as we're only interested in original opinion
        if RETWEET_STATUS_MARKER not in status.text:

            # classify tweet by polarity (negative/neutral/positive)
            polarity, subjectivity = extract_sentiment(status.text)

            tweet_item = {
                'id_str': status.id_str,
                'text': status.text,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'username': status.user.screen_name,
                'name': status.user.name,
                'profile_image_url': status.user.profile_image_url,
                'receiver_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            storage.push(tweet_item)
            print(f"Pushed to Redis: {tweet_item}")

    def on_error(self, status_code):
        # Shut down the stream if we get rate limit error
        if status_code == 420:
            print("Rate Limit error")
            return False


# Get API Auth tokens
config_path = 'config/api.json'
with open(config_path) as config_file:
    twitter_api = json.loads(config_file.read())
consumer_key = twitter_api["consumer_key"]
consumer_secret = twitter_api["consumer_secret"]
access_token = twitter_api["access_token"]
access_token_secret = twitter_api["access_token_secret"]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
stream = tweepy.Stream(auth=api.auth, listener=StreamListener())
stream.filter(track=TRACKED_BRANDS_LIST)
