import math
from tweet_loader import TweetSet

class Statistics:
    """This class represents a set of statistics extracted from a TweetSet"""
    def __init__(self, tweetSet):
        self.tweets = [t for t in tweetSet.tweets if not t.retweeted]

    def computeStatistics(self):
        # Tweet popularity
        for t in self.tweets:
            t.popularity = math.log(t.followers+1) + t.retweetCount + t.favoriteCount
        self.tweets = sorted(self.tweets, key=lambda tweet: -tweet.popularity)

    def __str__(self):
        limit = 10
        s = ''
        for t in self.tweets:
            limit-= 1
            if limit == 0:
                break
            s += '[author:@'+t.userName+', Followers:'+str(t.followers)+', RT:'+str(t.retweetCount)+', Favorites:'+str(t.favoriteCount)+', popularity:'+str(t.popularity)+', polarity:'+str(t.polarity)+']\n\t' + t.text + '\n'
        return s


if __name__ == '__main__':
    fileSource = "../tweets/disney.7403.json"
    tweets = TweetSet(fileSource)
    stats = Statistics(tweets)
    stats.computeStatistics()
    print stats
