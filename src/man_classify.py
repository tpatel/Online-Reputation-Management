#!/usr/bin/python2.7

'''
A little script to classify tweets stored on a file in json format.

It can process a file in a separate session and remembers where one was
before. It requests the user to specify the file to be processed and the name
of the user. The specified file is then processed and the result is printed to
the same file and file path but with the user-name concatenated to the
file-name. In other words if the file to be processed is /tweets/microsoft.17858.json
and the user is 'ludwig' then the result is stored in /tweets/microsoft.17858.json.ludwig.

By: Ludwig Forsberg 2013
'''


import json

tweets = '../tweets/microsoft.17858.json'

''' just a function that gives some error output'''
def printWrongInput():
    print ('Your input was incorrect, please try again or press \'h\' and ' + 
    'enter to get more information.')

''' save the results onto a file '''
def saveResults(jsonObj, file_path):
    f = open(file_path, 'w')
    print jsonObj
    json.dump(jsonObj, f);
    f.close()

''' the main function '''
if __name__ == '__main__':
    #construct the file path strings for input and output
    file_path = '../tweets/'
    file_name = raw_input('What file in ../tweets would you like to parse?\n')
    in_file_path = file_path + file_name
    user = raw_input('What is your user name?\n')
    out_file_path = file_path + file_name + "." + user

    #open the output file if existing and retrieve the json object
    try:
        f_out = open(out_file_path, 'r')
        file_string = f_out.read()
        out_jsonObj = json.loads(file_string)
        f_out.close()
    
    ##if the file doesn't exist, make a new list
    except Exception:
        out_jsonObj = []
    
    ##start at the end of the loaded list
    i = len(out_jsonObj)

    ##open the input file with tweets to parse
    f_in = open(in_file_path, 'r')
    file_string = f_in.read()
    
    ##get the json in the file
    in_jsonObj = json.loads(file_string)

    ##start loop to classify all the tweets in the file
    cont = True
    while (cont):
        score = -3 #magic number score
        #indicate which tweet
        print 'Tweet no ' + str(i) + ':\n' + in_jsonObj[i]['text']
        #get input from the user
        answer = raw_input('\nPlease classify the following tweet (press h ' + 
                           'and enter for help)\n')
        ##parse the input
        if('h' == answer):
            #print the help string
            print ('enter 1 for negative, 11 for negative but unsure, 2 for ' +
            'neutral, 22 for neutral but unsure, 3 for positive, 33 for ' + 
            'positive but unsure, \'b\' to go back and \'f\' to go forward ' +
            'one step, \'b x\' and \'f x \' to go back or forward x steps ' + 
            '(or to the end or beginning of the list), \'s\' to save your ' +
            'current progress and \'e\' to save and exit.')
        elif('b' == answer):
            #decrease the counter if not at the beginning
            if(i > 0):
                i -= 1
        elif('f' == answer):
            #increase the counter if not at the first un-scored tweet
            if(i < (len(out_jsonObj))):
                i += 1
        elif('1' == answer):
            #set the score to indicate sure negative
            score = -2
        elif('11' == answer):
            #set the score to indicate unsure negative
            score = -1
        elif('2' == answer):
            #set the score to indicate sure neutral
            score = 0
        elif('22' == answer):
            #set the score to indicate unsure neutral
            score = 1
        elif('3' == answer):
            #set the score to indicate sure positive
            score = 3
        elif('33' == answer):
            #set the score to indicate unsure positive
            score = 2
        elif('s' == answer):
            #save the current scores
            saveResults(out_jsonObj, out_file_path)
            print 'You have now saved your results!'
        elif('e' == answer):
            #save and exit your current score
            cont = False
            saveResults(out_jsonObj, out_file_path);
            print 'You have now saved your results and exited the program!'
        else:
            ##figure out if a 'b x' or 'f x' command was given
            #split the string in two
            answer = answer.split(' ', 1)
            if(2 == len(answer)):
                #if 'b x' was given
                if('b' == answer[0]):
                    #decrease the iterator
                    i -= int(answer[1])
                    #if the iterator get too small, set to first element
                    if(i < 0):
                        i = 0;
                #if 'f x' was given
                elif('f' == answer[0]):
                    #increment the iterator
                    i += int(answer[1])
                    #if the iterator is passed the last element scored, set
                    #iterator to that element
                    if(i >= len(out_jsonObj)):
                        i = len(out_jsonObj)-1
                else:
                    #indicate that the input was faulty
                    printWrongInput()
            else:
                #indicate that the input was faulty
                printWrongInput()
        #check if a new score was added
        if(-3 != score):
            #check if a new tweet had its score set
            if(i == len(out_jsonObj)):
                #append the score to the result
                out_jsonObj.append({'id_str':in_jsonObj[i]['id_str'],
                                    'score':score})
            #if the score of a tweet was updated
            else:
                #update the score
                out_jsonObj[i]['score'] = score
            #update the iterator to point to the next element
            i += 1
        #check if all tweets has been classified
        if(i == len(in_jsonObj)):
            #indicate that the classification is complete and exit loop
            cont = False
            print 'You have completely classified all the tweets in the file'
