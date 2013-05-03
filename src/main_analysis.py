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

    def __init__(self):
        """ initialize the SVNLearner """
        self.m_learner = SVMLearner()

#train_tweets = 'test'
#new_tweets = 'test2'

tweets_file = '../tweets/gazprom.2016.json'

if __name__ == '__main__':
    """ the main function """

    #load the tweets from file
    datas = TweetSet(tweets_file)
    print datas

    #get the training tweets and insert them into a list
    tweets = []
    for t in datas.get_positive_tweets():
        t.polarity = 10
        tweets.append(t)
    for t in datas.get_negative_tweets():
        t.polarity = -10
        tweets.append(t)
    for t in datas.get_neutral_tweets():
        t.polarity = 0
        tweets.append(t)

    #train the SVM
    a = MainAnalysis()
    a.m_learner.learn_from_tweets(tweets)

    classified = []
    #make the SVM classify all the tweets
    for t in datas.tweets:
        #use the SVM to predict the polarity
        t.polarity = a.m_learner.predict_from_tweet(t)
        #append the tweet to the list
        classified.append(t)
    #print all the tweets
    for t in classified:
        print t
            

