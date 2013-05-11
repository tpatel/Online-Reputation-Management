#!/usr/bin/python2.7

"""
This file is running the tests to compare our results
"""

import math
import json
from main_analysis import MainAnalysis
from tweet_loader import TweetSet
from lexicon_analysis import LexiconAnalysis
from lexicon_sentiments_analysis import LexiconSentimentsAnalysis

class Tests:
    def __init__(self):
        pass

    def get_svm_results(self, f, nb=-1):
        """Return the MainAnalysis result for the nb first tweets in file f"""
        #train the SVM
        a = MainAnalysis(f)
        a.learn()

        if nb == -1:
            return a.classify(a.datas.tweets)
        else:
            return a.classify(a.datas.tweets[0:nb])

    def get_manual_results(self, files, nb):
        """Return the manual classification result for the nb first tweets
           in files in files"""
        manual = []
        for f in files:
            data = open(f, 'r')
            tweets = json.loads(open(f, 'r').read())
            data.close()
            if not manual:
                manual = tweets[0:nb]
                for t in manual:
                    v = [0, 0, 0]
                    if t["score"] >= 2:
                        v[0] += 1
                    elif t["score"] <= -1:
                        v[2] += 1
                    else:
                        v[1] += 1
                    t["score"] = v
            else:
                for i in range(nb):
                    if tweets[i]["score"] >= 2:
                        manual[i]["score"][0] += 1
                    elif t["score"] <= -1:
                        manual[i]["score"][2] += 1
                    else:
                        manual[i]["score"][1] += 1

        for t in manual:
            pol = t["score"].index(max(t["score"]))
            if max(t["score"]) == 1:
                pol = 1

            if pol == 0:
                t["score"] = 10
            elif pol == 1:
                t["score"] = 0
            else:
                t["score"] = -10
            
#            t["score"] /= len(files)
#            if t["score"] >= 2:
#                t["score"] = 10
#            elif t["score"] <= -1:
#                t["score"] = -10
#            else:
#                t["score"] = 0

        return manual

    def compare_svm_manual(self, f, nb):
        manual_files = [f+".ludwig", f+".kristoffer", f+".romain"]
        svm_results = self.get_svm_results(f, nb)
        manual_results = self.get_manual_results(manual_files, nb)
        print "SVM Polarity vs. Manual Polarity"
        agree = 0
        for i in range(nb):
            if svm_results[i].polarity == manual_results[i]["score"]:
                agree += 1
            print "%s\t %d\t -\t %d\t %s"%(svm_results[i].tweet_id,
                    svm_results[i].polarity, manual_results[i]["score"],
                    svm_results[i].text)

        print "\n\nAgree on %d tweets (%d%%)"%(agree, agree*100/nb)

    def compare_lexicon_manual(self, f, nb):
        lexicon = LexiconSentimentsAnalysis()
        datas = TweetSet(f, nb)
        manual_files = [f+".ludwig", f+".kristoffer", f+".romain",
                f+".thibaut"]
        manual_results = self.get_manual_results(manual_files, nb)
        print "Lexicon Polarity vs. Manual Polarity"
        agree = 0
        for i in range(nb):
            t = datas.tweets[i]
            score = lexicon.getScoreTweet(t.cleaned_text)
            pol = 0
            if score[0] - score[1] >= 2:
                pol = 10
            elif score[1] - score[0] >= 2:
                pol = -10
            if pol == manual_results[i]["score"]:
                agree += 1
            print "%s\t %d\t -\t %d\t %s"%(t.tweet_id, pol,
                    manual_results[i]["score"], t.text)

        print "\n\nAgree on %d tweets (%d%%)"%(agree, agree*100/nb)

    def get_company_score(self, f, tweak=True):
        svm_results = self.get_svm_results(f)
        score = {"pos":0, "neu":0, "neg":0}
        for t in svm_results:
            #s = t.followers + t.retweetCount + t.favoriteCount
            s = 1
            if tweak:
                s = math.log(t.followers+1) + t.retweetCount + t.favoriteCount
            if t.polarity == 10:
                score["pos"] += s
            elif t.polarity == 0:
                score["neu"] += s
            else:
                score["neg"] += s
            
        total = float(score["neg"] + score["neu"] + score["pos"])/100
        score["opinion"] = "%f%%"%(float(score["pos"]*100)/(score["neg"] + score["pos"]))
        score["pos"] = "%f%%"%(float(score["pos"])/total)
        score["neu"] = "%f%%"%(float(score["neu"])/total)
        score["neg"] = "%f%%"%(float(score["neg"])/total)
        return score


    def get_company_score_with_lexicon(self, f, tweak=True):
        lexicon = LexiconSentimentsAnalysis()
        datas = TweetSet(f)
        score = {"pos":0, "neu":0, "neg":0}
        for t in datas.tweets:
            p = lexicon.getScoreTweet(t.text)
            s = 1
            if tweak:
                s = math.log(t.followers+1) + t.retweetCount + t.favoriteCount
            if p[0] - p[1] >= 2:
                score["pos"] += s
            elif p[1] - p[0] >= 2:
                score["neg"] += s
            else:
                score["neu"] += s
            
        total = float(score["neg"] + score["neu"] + score["pos"])/100
        score["opinion"] = "%f%%"%(float(score["pos"]*100)/(score["neg"] + score["pos"]))
        score["pos"] = "%f%%"%(float(score["pos"])/total)
        score["neu"] = "%f%%"%(float(score["neu"])/total)
        score["neg"] = "%f%%"%(float(score["neg"])/total)
        return score



if __name__ == '__main__':
    coca_file = '../tweets/coca cola.4592.json'
    disney_file = '../tweets/disney.7403.json'
    costco_file = '../tweets/costco.7164.json'
    microsoft_file = '../tweets/microsoft.17858.json'
    louis_vuiton_file = '../tweets/louisvuitton.2792.json'
    gazprom_file = '../tweets/gazprom.2016.json'
    tests = Tests()
    tests.compare_lexicon_manual(coca_file, 100)
    tests.compare_lexicon_manual(disney_file, 100)
    tests.compare_lexicon_manual(costco_file, 100)
    tests.compare_svm_manual(coca_file, 100)
    tests.compare_svm_manual(disney_file, 100)
    tests.compare_svm_manual(costco_file, 100)
#    print "Coca cola without tweaks: %s"%(tests.get_company_score(coca_file, False))
#    print "Disney without tweaks: %s"%(tests.get_company_score(disney_file, False))
#    print "CostCo without tweaks: %s"%(tests.get_company_score(costco_file, False))
#    print "Microsoft without tweaks: %s"%(tests.get_company_score(microsoft_file, False))
#    print "Louis Vuiton without tweaks: %s"%(tests.get_company_score(louis_vuiton_file, False))
#    print "Gazprom without tweaks: %s"%(tests.get_company_score(gazprom_file, False))
#    print "Coca cola with tweaks: %s"%(tests.get_company_score(coca_file))
#    print "Disney with tweaks: %s"%(tests.get_company_score(disney_file))
#    print "CostCo with tweaks: %s"%(tests.get_company_score(costco_file))
#    print "Microsoft with tweaks: %s"%(tests.get_company_score(microsoft_file))
#    print "Louis Vuiton with tweaks: %s"%(tests.get_company_score(louis_vuiton_file))
#    print "Gazprom with tweaks: %s"%(tests.get_company_score(gazprom_file))

