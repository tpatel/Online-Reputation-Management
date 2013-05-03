#!/usr/bin/python2.7

"""
A little script processes the data in the Micro_WNOp and produces lexicons that
can be used to score words.

By: Ludwig Forsberg 2013.
"""

import json

class MicroWnopLexicon:
    """
    A class that uses the Micro-WNOp-data to create lexicons to give the scores for a word.

    It just process the data and enters the different words with values into
    separate dictionaries for every lexicon in the file. Then it can create new
    lexicons ('SepMicroWnopLexicon') that then can be used to retrieve the scores
    for a word.
    By: Ludwig Forsberg 2013.
    """

    word_map_list = [] #a list of all the dictionaries

    ## create all the dictionaries

    def __init__(self):
        ''' create all the dictionaries '''
        temp_word_map_list = [] #a temporary list of dictionaries
        
        ##open the data-file
        f = open('../lexicon/Micro-WNOp-data.txt', 'r')
        
        ##parse the data file
        #for every line in the data-file
        for line in f:
            #ignore lines starting with a comment
            if '#' != line[0]:
                ##parse the score-part of the line
                #split the line up in scores and text
                parse_line = line.split('\t')
                #count how many lexicons are noted in the same line
                nr_lists = (len(parse_line)-1)/2
                #create enough temporary lexicons to contain all of the
                #lexicons whose scores are present on the same line
                while len(temp_word_map_list) < nr_lists:
                    temp_word_map_list.append(dict([]))

                ##parse the word-part of the line
                words = parse_line[nr_lists*2].split(' ')
                for word in words:
                    #remove all the trailing information from the word
                    word = word.split('#', 1)
                    ##add the scores to each lexicon whose scores are present
                    ##on a line
                    #for every set of scores
                    for i in range(0, nr_lists):
                        #calculate the offset among the scores
                        off = i*2
                        #get the new scores present on the line
                        new_values = [float(parse_line[0+off]),
                                float(parse_line[1+off])]
                        #check if the word is already present in the dictionary
                        if word[0] in temp_word_map_list[i]:
                            ##if so, add the new score with the old score and
                            ##update the amount of matches made on the word
                            temp = temp_word_map_list[i][word[0]]
                            #update matches
                            temp[2] += 1
                            #add the scores
                            temp_word_map_list[i][word[0]] = map(sum, zip(temp, new_values+[0]));
                        else:
                            #just add the scores with matches set to 1
                            temp_word_map_list[i][word[0]] = new_values + [1]
                            
            #handle lines where an old set of lexicons are complete
            elif '# end' == line[0:5]:
                #add all the lexicons to the main list of lexicons
                for word_map in temp_word_map_list:
                    self.word_map_list.append(word_map)
                #clear the temporary set of lexicons
                temp_word_map_list = []

    def createLexicon(self, index):
        """ a function that creates new lexicons using an index """

        #check if the index is valid
        if index >= len(self.word_map_list) or 0 > index:
            #if index is invalid, return None and give error output
            print 'Error, tried to create an index that does not exist'
            return None
        else:
            #if index is valid, create and return the new lexicon
            return SepMicroWnopLexicon(self.word_map_list[index])

class SepMicroWnopLexicon:
    """
    A class that uses a dictionary to determine the score for a word.

    It just looks in the dictionary and process the scores a bit (divide the sum of
    scores with the number of occurrences in the lexicon) before returning it. 

    By: Ludwig Forsberg 2013
    """

    word_map = dict([]) #a dictionary for the lexicon
    
    def __init__(self, p_word_map):
        """ a function that just initialize the dictionary for the lexicon """

        self.word_map = p_word_map

    def getScore(self, tweet_word):
        """ 
        a function that returns the score of a word in a list with first the
        positive value and then the negative
        """

        #check if the word is in the dictionary
        if tweet_word in self.word_map:
            #divide the summed score in the lexicon with the number of occurrences
            #it had in the lexicon and then return it
            return [self.word_map[tweet_word][i]/self.word_map[tweet_word][2] \
                        for i in range(0,2)]
        else:
            #if the word is not present, return a 0.0 word
            return [0.0, 0.0]

