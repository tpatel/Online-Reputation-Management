#!/usr/bin/python2.7

import re
import string
import nltk
from nltk.corpus.reader import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()

class Tweet:
    """This class represents a tweet for the SVM with all its features"""

    def __init__(self, struct):
        self.url_pattern = re.compile("http")
        self.tweet_id = struct['id_str'].encode('utf-8')
        self.text = struct['text'].encode('utf-8').rstrip()
        self.words = self.clean_text(self.text)
        self.cleaned_text = " ".join(self.words)
        
        self.retweetCount = struct['retweet_count']
        self.favoriteCount = struct['favorite_count']
        self.creation = struct['created_at'].encode('utf-8')
        self.followers = struct['user_followers_count']
        
        self.userId = struct['user_id_str'].encode('utf-8')
        self.userName = struct['user_screen_name'].encode('utf-8')
        
        if 'retweeted_status_id_str' in struct:
            self.retweeted = True
            self.retweetedStatusId = struct['retweeted_status_id_str'].encode('utf-8')
        else:
            self.retweeted = False
        
        self.popularity = 0 # Used in statistics computations
        
        self.polarity = 0
        self.lexicon_score = [0, 0]

        self.length = len(self.text)
        self.nb_words = len(self.text.split())
        self.unigrams = {}
        self.bigrams = {}


    def get_features_representation(self):
        """Return a list with all the features of the tweet"""
        return self.unigrams.values() + self.bigrams.values()
        return self.unigrams.values()
        #return self.unigrams.values() + [self.length, self.nb_words]

    def get_unigrams(self):
        """Return the set of unigrams in the tweet"""
        unigrams = set()
        for w in self.words:
            if len(w) > 2 and w[0] != "#" and w[0] != "@" \
                    and not re.match(self.url_pattern, w):
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
            w1 = w2
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
            w1 = w2
        for b in self.bigrams.keys():
            if self.bigrams[b] > 0:
                self.bigrams[b] = 1 

    def clean_words(self):
        words = self.text.lower().translate(None, string.punctuation).split()
        words = [w for w in words if w and not re.match(self.url_pattern, w)]
        return words

    def clean_text(self, text):
        words = text.lower().translate(None, string.punctuation).split()
        words = [w for w in words if w and not re.match(self.url_pattern, w)]
        cleaned = []
        for w in nltk.pos_tag(words):
            k = self.get_wordnet_pos(w[1])
            if k:
                cleaned.append(lmtzr.lemmatize(w[0], k))
            else:
                cleaned.append(lmtzr.lemmatize(w[0]))
        return cleaned


    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''

    def is_equal_to(self, tweet):
        """Rough comparison between the text of two tweets
           Returns True iff the words in the tweets are the same"""
        set1 = set(self.get_unigrams())
        set2 = set(tweet.get_unigrams())
        return set1.issubset(set2) or set2.issubset(set1)

    def __str__(self):
        s = "[%f, %f] %s"%(self.lexicon_score[0], self.lexicon_score[1],
                self.text.rstrip())
        return s

