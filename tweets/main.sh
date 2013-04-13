#!/bin/sh

touch alltweets.txt
rm alltweets.txt
node extractText.js
cd ../src/
python lexicon_sentiments_analysis.py ../tweets/alltweets.txt > ../tweets/rankedTweets
cd ../tweets/
cat rankedTweets | sort -n | head -n 20 > out #20 best tweets
cat rankedTweets | sort -n | tail -n 20 >> out #20 worst tweets
cat rankedTweets | grep "^0\.000000" | awk '{print length, $0}' | sort -rn | awk '{$1=""; print $0 }' | head -n 20 >> out #20 longest neutral tweets
