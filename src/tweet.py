#!/usr/bin/python2.7

import re
import string
import json

from lexicon_sentiments_analysis import LexiconSentimentsAnalysis

class Tweet:
    """This class represents a tweet"""

    def __init__(self, struct):
        self.id = struct['id_str'].encode('utf-8')
        self.text = struct['text'].encode('utf-8').rstrip()
        
        self.retweetCount = struct['retweet_count']
        self.favoriteCount = struct['favorite_count']
        self.creation = struct['created_at'].encode('utf-8')
        self.followers = struct['user_followers_count']
        
        self.userId = struct['user_id_str'].encode('utf-8')
        self.userName = struct['user_screen_name'].encode('utf-8')
        
        self.polarity = 0
        
    def __str__(self):
        s = "%s %f"%(self.text, self.polarity)
        return s


if __name__ == '__main__':
    fileSource = "../tweets/louisvuitton.2792.json"
    json_data = open(fileSource)
    data = json.load(json_data)
    tweets = []
    for i in data:
        tweets.append(Tweet(i));
    
    l = LexiconSentimentsAnalysis()
    for i in tweets:
        i.polarity = l.analyse_text(i.text)
    
    negative = sorted(tweets, key=lambda tweet: tweet.polarity)
    negative = negative[0:20]
    positive = sorted(tweets, key=lambda tweet: -tweet.polarity)
    positive = positive[0:20]
    
    neutral = [tweet for tweet in tweets if tweet.polarity == 0]
    neutral = sorted(neutral, key=lambda tweet: -len(tweet.text))
    
    print negative[0], positive[0], neutral[0]
    
    
    
    
    
    
    
    
    
    
