#!/usr/bin/python2.7

import re
import string

class Tweet:
    """This class represents a tweet for the SVM with all its features"""

    def __init__(self, tweet_id, text, polarity=0):
        self.tweet = text
        self.url_pattern = re.compile("http://")
        self.tweet_id = tweet_id

        self.polarity = polarity
        self.length = len(text)
        self.nb_words = len(text.split())
        self.unigrams = {}

    def get_features_representation(self):
        """Return a list with all the features of the tweet"""
        return self.unigrams.values() + [self.length, self.nb_words]

    def get_unigrams(self):
        """Return the set of unigrams in the tweet"""
        unigrams = set()
        words = self.tweet.lower().translate(None, string.punctuation).split()
        for w in words:
            if len(w) > 2 and w[0] != "#" and not re.match(self.url_pattern, w):
                unigrams.add(w)
        return unigrams

    def set_unigrams(self, unigrams):
        self.unigrams = dict((u,0) for u in unigrams)
        words = self.tweet.lower().split()
        for w in words:
            if w in self.unigrams.keys():
                self.unigrams[w] += 1

    def __str__(self):
        s = "%s\n"%(self.tweet.rstrip())
        s += "    ID: %s\n"%(self.tweet_id)
        s += "    Length: %d\n"%(self.length)
        s += "    Number of words: %d\n"%(self.nb_words)
        s += "    Polarity: %d\n"%(self.polarity)
        return s


if __name__ == '__main__':
    test = open("test_tweets.txt")
    for tweet in test:
        t = Tweet(tweet)
        print t
