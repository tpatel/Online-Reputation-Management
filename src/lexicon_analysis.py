#!/usr/bin/python2.7

""" 
A little script that takes a file with tweets and a couple of lexicons and uses
the lexicons to score the tweets and then store the result in a different file.

By: Ludwig Forsberg 2013.
"""

import json
import sys

import micro_wnop_lexicon as lex1 #lexicon creator

dir_path = '../tweets/' #path to the tweets

lex_list = [] #list of lexicons

class LexiconAnalysis:

    def __init__(self):
<<<<<<< HEAD
        """ a function that initializes the list of lexicons to be used """
        
=======
        ''' a function that initializes the list of lexicons to be used '''
>>>>>>> a0ce34983b60d5f2b71d909a21941b6513bd330e
        ##initialize the different lexicon creators
        wno = lex1.MicroWnopLexicon()
        
        ##add the lexicons to the list
        lex_list.append(wno.createLexicon(0))
        lex_list.append(wno.createLexicon(1))
        lex_list.append(wno.createLexicon(2))
        lex_list.append(wno.createLexicon(3))
        lex_list.append(wno.createLexicon(4))
        lex_list.append(wno.createLexicon(5))
    
    def saveResults(self, jsonObj, file_path):
<<<<<<< HEAD
        """ save the results onto a file """
=======
        ''' save the results onto a file '''
>>>>>>> a0ce34983b60d5f2b71d909a21941b6513bd330e
        f = open(file_path, 'w')
        json.dump(jsonObj, f);
        f.close()

    def getScoreTweet(self, tweet):
<<<<<<< HEAD
        """ a function that returns the score for a tweet """
=======
        ''' a function that returns the score for a tweet '''
>>>>>>> a0ce34983b60d5f2b71d909a21941b6513bd330e
        score = [0, 0]
        ##for all the words in the tweet
        word_list = tweet.lower().split()
        for word in word_list:
            ##and for all lexicons in the list
            for lexicon in lex_list:
                #add the score of that word in that lexicon to the total score
                #for that word
                score = map(sum, zip(score, lexicon.getScore(word)))
        return score
    
    def processTweets(self, in_file):
<<<<<<< HEAD
        """ 
        a function that process a number of tweets in a certain file in json format 
        """

=======
        ''' a function that process a number of tweets in a certain file in
        json format '''
>>>>>>> a0ce34983b60d5f2b71d909a21941b6513bd330e
        ##create the path to the file we will process
        file_path = dir_path + in_file

        ##try to open and parse the file we will process
        try:
            f_in = open(file_path, 'r')
            file_string = f_in.read()
            in_jsonObj = json.loads(file_string)
            f_in.close()
            
        ##if the file doesn't exist, make a new empty list
        except Exception:
            in_jsonObj = []
        
        ##process the tweets and put in the result
        #create the list that will contain the result
        out_jsonObj = []
        #for every tweet in the file
        for tweet in in_jsonObj:
            #calculate the score and put it in the result
            out_jsonObj.append({'id_str': tweet['id_str'], 'score': \
        self.getScoreTweet(tweet['text'])})
        
        ##save the result of processing the tweets
        self.saveResults(out_jsonObj, file_path + '.lex_scored')
        
if __name__ == '__main__':
<<<<<<< HEAD
    """ 
    the main function that expects a file name to the file with tweets to be
    processed to be provided 
    """

=======
    ''' the main function that expects a file name to the file with tweets to
    be processed to be provided '''
>>>>>>> a0ce34983b60d5f2b71d909a21941b6513bd330e
    l = LexiconAnalysis()
    if 2 == len(sys.argv):
        l.processTweets(sys.argv[1])
    else:
        print "provide the name of the file you want to process!"
