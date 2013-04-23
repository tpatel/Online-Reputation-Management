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
        self.bigrams = set()
        for t in tweets:
            self.unigrams = self.unigrams.union(t.get_unigrams())
            self.bigrams = self.bigrams.union(t.get_bigrams())

        features = []
        polarities = []
        for t in tweets:
            t.set_unigrams(self.unigrams)
            t.set_bigrams(self.bigrams)
            features.append(t.get_features_representation())
            polarities.append(t.polarity)
        print polarities

        self.svm.fit(features, polarities)

    def predict_from_tweet(self, tweet):
        """Predict the polarity of a tweet"""
        tweet.set_unigrams(self.unigrams)
        tweet.set_bigrams(self.bigrams)
        return self.svm.predict([tweet.get_features_representation()])[0]

