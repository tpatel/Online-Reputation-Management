#!/usr/bin/python2.7

from sklearn import svm
from svm_tweet import Tweet

class SVMLearner:
    """The class learns from a set of positive and negative tweets,
       then can predict the polarity of tweets"""

    def __init__(self):
        self.svm = svm.SVC()

    def learn_from_tweets(self, tweets):
        """Learn from tweets (list of instances of Tweet class)"""
        features = []
        polarities = []
        for t in tweets:
           features.append(t.get_features_representation())
           polarities.append(t.polarity)

        self.svm.fit(features, polarities)

    def predict_from_tweet(self, tweet):
        """Predict the polarity of a tweet"""
        return self.svm.predict([tweet.get_features_representation()])[0]


if __name__ == '__main__':
    #Basic test to test the svm
    #Should return 1
    learner = SVMLearner()
    t1 = Tweet("", 0)
    t2 = Tweet("b", 1)
    learner.learn_from_tweets([t1, t2])

    t3 = Tweet("b", 1)
    print "Basic test result: %d"%(learner.predict_from_tweet(t3))
