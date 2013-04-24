#!/usr/bin/python2.7

import re
import string
import json

from lexicon_sentiments_analysis import LexiconSentimentsAnalysis
from svm_tweet import Tweet

NB_TRAINING_TWEETS = 20

class TweetSet:
    """This class represents a set of tweets loaded from a file"""
    def __init__(self, filename):
        self.filename = filename
        self.tweets = []
        self.positives = []
        self.negatives = []
        self.neutrals = []
        self.lexicon = LexiconSentimentsAnalysis()

        self.load_tweets()

    def load_tweets(self):
        """Loads tweets stored as a json in filename"""
        json_data = open(self.filename)
        data = json.load(json_data)
        for i in data:
            t = Tweet(i)
            t.polarity = self.lexicon.analyse_text(t.text)
            self.tweets.append(t)

        self.negatives = sorted(self.tweets, key=lambda tweet: tweet.polarity)
        self.positives = sorted(self.tweets, key=lambda tweet: -tweet.polarity)
        self.neutrals = sorted([tweet for tweet in self.tweets if
                tweet.polarity == 0], key=lambda tweet: -len(tweet.text))

    def get_positive_tweets(self):
        return self.uniq_top(self.positives, NB_TRAINING_TWEETS)

    def get_negative_tweets(self):
        return self.uniq_top(self.negatives, NB_TRAINING_TWEETS)

    def get_neutral_tweets(self):
        return self.uniq_top(self.neutrals, NB_TRAINING_TWEETS)
        
    def uniq_top(self, l, n):
        """Return the first n unique tweets in list l"""
        top = []
        i = 0
        while len(top) < n and i < len(l):
            tweet = l[i]
            uniq = True
            for t in top:
                if t.is_equal_to(tweet):
                    uniq = False
                    break
            if uniq:
                top.append(tweet)
            i += 1

        return top


    def __str__(self):
        s = "%d tweets\n"%(len(self.tweets))
        s += "\n-----------------------------------------------------\n"
        s += "                 Negative Tweets                     \n"
        s += "-----------------------------------------------------\n\n"
        for t in self.get_negative_tweets():
            s+= "%s\n"%(t)
        s += "\n-----------------------------------------------------\n"
        s += "                 Positive Tweets                     \n"
        s += "-----------------------------------------------------\n\n"
        for t in self.get_positive_tweets():
            s+= "%s\n"%(t)
        s += "\n-----------------------------------------------------\n"
        s += "                 Neutral Tweets                     \n"
        s += "-----------------------------------------------------\n\n"
        for t in self.get_neutral_tweets():
            s+= "%s\n"%(t)
        return s


if __name__ == '__main__':
    fileSource = "../tweets/gazprom.2016.json"
    tweets = TweetSet(fileSource)
    print tweets

    
