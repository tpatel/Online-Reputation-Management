#!/usr/bin/python2.7

'''
A little script that uses the training tweets, the un-scored tweets and the
SVM.

It loads the training tweets, prints those tweets, then trains the SVM on
them. After that the new tweets are loaded and the SVM is used to classify
them. Finally all those tweets are printed.

By: Ludwig Forsberg 2013.
'''

from sklearn import svm
from svm_tweet import Tweet
from svm_sentiments_analysis import SVMLearner

''' class that will contain the actual SVM '''
class MainAnalysis:

    ''' initialize the SVNLearner '''
    def __init__(self):
        self.m_learner = SVMLearner()

#train_tweets = 'test'
#new_tweets = 'test2'

train_tweets = '../tweets/out'
new_tweets = '../tweets/alltweets'

''' the main function '''
if __name__ == '__main__':

    #open the training tweets
    f = open(train_tweets, 'r')

    #parse the file and insert the training tweets into a list
    tweets = []
    for line in f:
        #split the string in three parts
        line = line.split(' ', 2)
        if 3 == len(line):
            #assign the polarity
            if float(line[0]) > 0:
                polarity = 10.
            if float(line[0]) < 0:
                polarity = -10.
            if float(line[0]) == 0:
                polarity = 0.
            #create a new tweet
            t = Tweet(line[1], line[2].rstrip(), polarity)
            #print the tweet
            print t
            #append the tweet to the list of training tweets
            tweets.append(t)
    #close the file
    f.close()

    ##train the SVM
    a = MainAnalysis()
    a.m_learner.learn_from_tweets(tweets)

    ##read new tweets and make the SVM classify them
    f = open(new_tweets, 'r');
    tweets = []
    for line in f:
        #split the string in two parts
        line = line.split(' ', 1)
        if 2 == len(line):
            #create a new tweet
            t = Tweet(line[0], line[1].rstrip(), 0)
            #use the SVM to predict the polarity
            t.polarity = a.m_learner.predict_from_tweet(t)
            #append the tweet to the list
            tweets.append(t)
    #print all the tweets
    for t in tweets:
        print t
            

