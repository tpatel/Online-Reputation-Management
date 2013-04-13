#!/usr/bin/python2.7

from sklearn import svm
from svm_tweet import Tweet

class SVMLearner:
    """The class learns from a set of positive and negative tweets,
       then can predict the polarity of tweets"""

    def __init__(self):
        self.svm = svm.SVC()
        self.unigrams = set()

    def learn_from_tweets(self, tweets):
        """Learn from tweets (list of instances of Tweet class)"""

        #Get unigrams
        self.unigrams = set()
        for t in tweets:
            self.unigrams = self.unigrams.union(t.get_unigrams())

        features = []
        polarities = []
        for t in tweets:
            t.set_unigrams(self.unigrams)
            features.append(t.get_features_representation())
            polarities.append(t.polarity)
        print polarities

        self.svm.fit(features, polarities)

    def predict_from_tweet(self, tweet):
        """Predict the polarity of a tweet"""
        tweet.set_unigrams(self.unigrams)
        return self.svm.predict([tweet.get_features_representation()])[0]


if __name__ == '__main__':
    l = SVMLearner()
    test = open("test_tweets.txt")
    a = []
    i = 0
    for tweet in test:
        polarity = -1 if (i<1) else 1 if (i==1) else 0
        a.append(Tweet(i, tweet, polarity))
        i += 1
    l.learn_from_tweets(a)
    for tweet in a:
        print "Features for tweet %d: %s"%(tweet.tweet_id, tweet.get_features_representation())

    print "\nNow trying to classify a now tweet:"
    t = Tweet(4, "Fuck you Microsoft, you suck")
    print l.predict_from_tweet(t)
    t = Tweet(5, "Microsoft is great, I love you")
    print l.predict_from_tweet(t)
    t = Tweet(6, "Great offsite yesterday with the dream talent team at Microsoft. Some great presentations and ideas discussed. Roll on FY14!")
    print l.predict_from_tweet(t)

