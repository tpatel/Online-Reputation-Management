#!/usr/bin/python2.7

import re
import string
import json

class Tweet:
    """This class represents a tweet"""

    def __init__(self, struct):
        self.id = struct['id_str']
        self.text = struct['text'].encode('utf-8')
        print self
        
        self.retweetCount = struct['retweet_count']
        self.favoriteCount = struct['favorite_count']
        self.creation = struct['created_at']
        self.followers = struct['user_followers_count']
        
        self.userId = struct['user_id_str']
        self.userName = struct['user_screen_name']
        
    def __str__(self):
        s = "%s\n"%(self.text.rstrip())
        return s


if __name__ == '__main__':
    fileSource = "../tweets/louisvuitton.2792.json"
    json_data = open(fileSource)
    data = json.load(json_data)
    tweets = []
    for i in data:
        tweets.append(Tweet(i));
