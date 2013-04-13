#!/usr/bin/python2.7

from sklearn import svm
from svm_tweet import Tweet
from svm_sentiments_analysis import SVMLearner

class MainAnalysis:

    def __init__(self):
        self.m_learner = SVMLearner()

#train_tweets = 'test'
#new_tweets = 'test2'

train_tweets = '../tweets/out'
new_tweets = '../tweets/alltweets'

if __name__ == '__main__':
    f = open(train_tweets, 'r')
    tweets = []
    for line in f:
        line = line.split(' ', 2)
        if 3 == len(line):
            if float(line[0]) > 0:
                polarity = 10.
            if float(line[0]) < 0:
                polarity = -10.
            if float(line[0]) == 0:
                polarity = 0.
            t = Tweet(line[1], line[2].rstrip(), polarity)
            print t
            tweets.append(t)
    f.close()
    a = MainAnalysis()
    a.m_learner.learn_from_tweets(tweets)
    f = open(new_tweets, 'r');
    tweets = []
    for line in f:
        line = line.split(' ', 1)
        if 2 == len(line):
            t = Tweet(line[0], line[1].rstrip(), 0)
            t.polarity = a.m_learner.predict_from_tweet(t)
            tweets.append(t)
    for t in tweets:
        print t
            

