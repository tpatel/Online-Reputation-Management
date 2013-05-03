#!/usr/bin/python2.7

"""
A python script to extract the polarity ratings from all manually classified tweets

By: Kristoffer Hallqvist 2013.
"""

import json

tweetpath = "../tweets/"
raters = ["kristoffer", "ludwig", "romain", "thibaut"]
tweetfiles = ["coca cola.4592.json","costco.7164.json","disney.7403.json"]


if __name__ == '__main__':
    """ the main function """

    #Go through all combinations of brands and raters
    
    for tname in tweetfiles:
        for rname in raters:
            fpath = tweetpath + tname + "." + rname
            print tname + rname
            
            #If the file exists:
            try:
                #Load the tweets from file
                f = open(fpath, 'r')
                content = f.read()
                tweets = json.loads(content)
                f.close()
                
                #Print the id and score
                for tweet in tweets:
                    print str(tweet["id_str"]) + "\t" + str(tweet["score"])

            
            #if the file doesn't exist, ignore it
            #Someone hasn't completed the classification!
            except Exception:
                print "No existing file for this rater"
        




