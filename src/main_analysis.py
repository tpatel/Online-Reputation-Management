#!/usr/bin/python2.7

"""
A little class that uses the training tweets, the un-scored tweets and the
SVM.

It loads the training tweets, prints those tweets, then trains the SVM on
them. After that the new tweets are loaded and the SVM is used to classify
them. Finally all those tweets are printed.

By: Ludwig Forsberg 2013.
"""

from sklearn import svm
from svm_tweet import Tweet
from tweet_loader import TweetSet
from svm_sentiments_analysis import SVMLearner

class MainAnalysis:
    """ class that will contain the actual SVM """

    def __init__(self, tweets_file):
        """ initialize the SVNLearner """
        self.m_learner = SVMLearner()
        self.tweets_file = tweets_file
        self.datas = TweetSet(self.tweets_file)
        self.training_tweets = []

    def learn(self):
        """ Make the SVM learn with datas loaded"""
        #get the training tweets and insert them into a list
        self.training_tweets = []
        for t in self.datas.get_positive_tweets():
            t.polarity = 10
            self.training_tweets.append(t)
        for t in self.datas.get_negative_tweets():
            t.polarity = -10
            self.training_tweets.append(t)
        for t in self.datas.get_neutral_tweets():
            t.polarity = 0
            self.training_tweets.append(t)
        self.m_learner.learn_from_tweets(self.training_tweets)

    def classify(self, tweets):
        """Get the polarity of tweets using the SVM"""
        classified = []
        for t in tweets:
            #use the SVM to predict the polarity
            t.polarity = self.m_learner.predict_from_tweet(t)
            #append the tweet to the list
            classified.append(t)

        return classified


if __name__ == '__main__':
    tweets_file = '../tweets/coca cola.4592.json'
    #train the SVM
    a = MainAnalysis(tweets_file)
    a.learn()

    #make the SVM classify the tweets
    for t in a.classify(a.datas.tweets):
        #print all the tweets
        print t
            

