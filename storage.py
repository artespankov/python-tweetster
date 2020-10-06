import json
import redis
from tweet import Tweet


class TweetStore:

    # Redis config
    redis_host = "localhost"
    redis_port = 6379

    redis_key = "tweets"
    num_tweets = 20

    def __init__(self):
        self.db = redis.Redis(
            host=self.redis_host,
            port=self.redis_port
        )
        self.trim_count = 0

    def push(self, data):
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        # Periodically trim the list so it doesn't grow too big
        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0

    def tweets(self, limit=10):
        tweets = []
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item)
            tweets.append(Tweet(tweet_obj))
        return tweets
