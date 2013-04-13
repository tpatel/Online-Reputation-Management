#!/usr/bin/python2.7

class Tweet:
    """This class represents a tweet for the SVM with all its features"""

    def __init__(self, tweet, polarity=0):
        self.tweet = tweet

        self.polarity = polarity
        self.length = len(tweet)
        self.nb_words = len(tweet.split())

    def get_features_representation(self):
        return [self.length, self.nb_words]

    def __str__(self):
        s = "%s\n"%(self.tweet.rstrip())
        s += "    Length: %d\n"%(self.length)
        s += "    Number of words: %d\n"%(self.nb_words)
        return s


if __name__ == '__main__':
    test = open("test_tweets.txt")
    for tweet in test:
        t = Tweet(tweet)
        print t
