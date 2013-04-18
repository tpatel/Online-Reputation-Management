#!/usr/bin/python2.7

import re
import string

class Tweet:
    """This class represents a tweet for the SVM with all its features"""

    def __init__(self, tweet_id, text, polarity=0):
        self.tweet = text
        print text
        self.url_pattern = re.compile("http")
        self.tweet_id = tweet_id

        self.polarity = polarity
        self.length = len(text)
        self.nb_words = len(text.split())
        self.words = self.clean_words();
        self.unigrams = {}
        self.bigrams = {}

    def get_features_representation(self):
        """Return a list with all the features of the tweet"""
        return self.unigrams.values() + self.bigrams.values()
        #return self.unigrams.values() + [self.length, self.nb_words]

    def get_unigrams(self):
        """Return the set of unigrams in the tweet"""
        unigrams = set()
        for w in self.words:
            if len(w) > 2 and w[0] != "#" and not re.match(self.url_pattern, w):
                unigrams.add(w)
        return unigrams

    def set_unigrams(self, unigrams):
        """Get the set of unigrams over all the tweets to create the feature
           representation"""
        self.unigrams = dict((u,0) for u in unigrams)
        for w in self.words:
            if w in self.unigrams.keys():
                self.unigrams[w] += 1

    def get_bigrams(self):
        """Return the set of bigrams in the tweet"""
        bigrams = set()
        w1 = self.words[0] if self.words else ""
        for w2 in self.words[1:]:
            bigrams.add("%s %s"%(w1,w2))
        return bigrams

    def set_bigrams(self, bigrams):
        """Get the set of biigrams over all the tweets to create the feature
           representation"""
        self.bigrams = dict((u,0) for u in bigrams)
        w1 = self.words[0] if self.words else ""
        for w2 in self.words[1:]:
            b = "%s %s"%(w1,w2)
            if b in self.bigrams.keys():
                self.bigrams[b] += 1

    def clean_words(self):
        words = self.tweet.lower().translate(None, string.punctuation).split()
        words = [w for w in words if w and not re.match(self.url_pattern, w)]
        return words


    def __str__(self):
        s = "%s\n"%(self.tweet.rstrip())
        s += "    ID: %s\n"%(self.tweet_id)
        s += "    Polarity: %d\n"%(self.polarity)
        return s


if __name__ == '__main__':
    test = open("test_tweets.txt")
    for tweet in test:
        t = Tweet(tweet)
        print t
