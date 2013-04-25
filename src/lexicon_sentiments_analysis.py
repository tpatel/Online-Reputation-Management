#!/usr/bin/python2.7

POSITIVE_LEXICON = "../lexicon/opinion-lexicon-English/positive-words.txt"
NEGATIVE_LEXICON = "../lexicon/opinion-lexicon-English/negative-words.txt"

class LexiconSentimentsAnalysis:
    """The class contains the lexicons and analyse a text with these"""
	
    def __init__(self):
        self.positive_words = self.get_positive_words()
        self.negative_words = self.get_negative_words()

    def get_positive_words(self):
        """Read the positive words from lexicon"""
        f  = open(POSITIVE_LEXICON)
        s = set()
        for line in f:
            if not line or line[0] == ";":
                continue
            else:
                s.add(line.rstrip())
        return s

    def get_negative_words(self):
        """Read the negative words from lexicon"""
        f  = open(NEGATIVE_LEXICON)
        s = set()
        for line in f:
            if not line or line[0] == ";":
                continue
            else:
                s.add(line.rstrip())
        return s

    def analyse_text(self, text):
        """Return the normalized score of the text"""
        t = text.lower().split()
        score = 0
        neutral = True
        for word in t:
            score += self.get_weight(word)
            if not score == 0:
                neutral = False
        if not neutral and score == 0:
        	score = 0.1
        return float(score)

    def get_weight(self, word):
        """Return the score of a word"""
        score = 0
        if word in self.positive_words:
            score += 1
        if word in self.negative_words:
            score -= 1
        return score


if __name__ == '__main__':
    l = LexiconSentimentsAnalysis()
    test = open("../tweets/alltweets.txt")
    for tweet in test:
        print "%f %s"%(l.analyse_text(tweet.rstrip()), tweet.rstrip())
    
