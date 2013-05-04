#!/usr/bin/python2.7

"""
This file is running the tests to compare our results
"""

import json
from main_analysis import MainAnalysis

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
            else:
                for i in range(nb):
                    manual[i]["score"] += tweets[i]["score"]

        for t in manual:
            t["score"] /= len(files)
            if t["score"] >= 2:
                t["score"] = 10
            elif t["score"] <= -1:
                t["score"] = -10
            else:
                t["score"] = 0

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
                    manual_results[i]["id_str"])

        print "\n\nAgree on %d tweets (%d%%)"%(agree, agree*100/nb)


#print "%d: %s - Polarity %d"%(i, t.tweet_id, t.polarity)

if __name__ == '__main__':
    coca_file = '../tweets/coca cola.4592.json'
    disney_file = '../tweets/disney.7403.json'
    costco_file = '../tweets/costco.7164.json'
    tests = Tests()
    tests.compare_svm_manual(coca_file, 100)
    tests.compare_svm_manual(disney_file, 100)
    tests.compare_svm_manual(costco_file, 100)

