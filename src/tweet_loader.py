#!/usr/bin/python2.7

import re
import string
import json

from lexicon_sentiments_analysis import LexiconSentimentsAnalysis
from svm_tweet import Tweet

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

        self.negative = sorted(self.tweets,
                key=lambda tweet: tweet.polarity)[0:20]
        self.positive = sorted(self.tweets,
                key=lambda tweet: -tweet.polarity)[0:20]
        self.neutral = sorted([tweet for tweet in self.tweets if
                tweet.polarity == 0], key=lambda tweet: -len(tweet.text))[0:20]

    def __str__(self):
        s = "%d tweets\n"%(len(self.tweets))
        s += "\n-----------------------------------------------------\n"
        s += "                 Negative Tweets                     \n"
        s += "-----------------------------------------------------\n\n"
        for t in self.negative:
            s+= "%s\n"%(t)
        s += "\n-----------------------------------------------------\n"
        s += "                 Positive Tweets                     \n"
        s += "-----------------------------------------------------\n\n"
        for t in self.positive:
            s+= "%s\n"%(t)
        s += "\n-----------------------------------------------------\n"
        s += "                 Neutral Tweets                     \n"
        s += "-----------------------------------------------------\n\n"
        for t in self.neutral:
            s+= "%s\n"%(t)
        return s


if __name__ == '__main__':
    fileSource = "../tweets/louisvuitton.2792.json"
    tweets = TweetSet(fileSource)
    print tweets

    
