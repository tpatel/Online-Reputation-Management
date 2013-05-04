import math
from tweet_loader import TweetSet
from main_analysis import MainAnalysis

class Statistics:
    """This class represents a set of statistics extracted from a TweetSet"""
    def __init__(self, tweetSet, f):
        a = MainAnalysis(f)
        a.learn()
        self.tweets = a.classify(a.datas.tweets)
        #self.tweets = [t for t in tweetSet.tweets if not t.retweeted]

    def computeStatistics(self):
        # Tweet popularity
        for t in self.tweets:
            t.popularity = math.log(t.followers+1) + t.retweetCount + t.favoriteCount
        self.tweets = sorted([t for t in self.tweets if not t.retweeted], key=lambda tweet: -tweet.popularity)

    def __str__(self):
        s = ''
        for t in self.tweets[0:10]:
            s += '[author:@'+t.userName+', Followers:'+str(t.followers)+', RT:'+str(t.retweetCount)+', Favorites:'+str(t.favoriteCount)+', popularity:'+str(t.popularity)+', polarity:'+str(t.polarity)+']\n\t' + t.text + '\n'
        return s


if __name__ == '__main__':
    fileSource = "../tweets/disney.7403.json"
    tweets = TweetSet(fileSource)
    stats = Statistics(tweets, fileSource)
    stats.computeStatistics()
    print stats
