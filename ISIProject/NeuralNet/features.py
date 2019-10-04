import os
import string
import word_lists as wl

def isdigit(word):
    return word.isdigit()

def index_word(fileName):
    #return a dictionary of word frequencies in the file
    dict={}
    cnt =0
    sec_cnt = 0
    with open(fileName,'r') as file:
        y=file.read()
        y=y.splitlines()
        for x in y:
            if sec_cnt%2 == 0:
                # print(x,' \n')
                # x=x.translate(string.punctuation)
                # x=x.translate(None, string.punctuation)
                exclude = set(string.punctuation)
                x = ''.join(ch for ch in x if ch not in exclude)
                # print(x,'\n')
                # print s
                # print(x,' \n')
                x=x.split(' ')
                for i in x:
                    if i not in dict:
                        dict[i]=cnt 
                        cnt=cnt+1
                    # else:
                    #     dict[i]=1
                sec_cnt=sec_cnt+1
            else:
                sec_cnt=sec_cnt+1   
    return dict




def frequencies(fileName):
    #return a dictionary of word frequencies in the file
    dict={}
    with open(fileName,'r') as file:
        y=file.read()
        y=y.splitlines()
        for x in y:
            # print(x,' \n')
            # x=x.translate(string.punctuation)
            # x=x.translate(None, string.punctuation)
            exclude = set(string.punctuation)
            x = ''.join(ch for ch in x if ch not in exclude)
            # print s
            # print(x,' \n')
            x=x.split(' ')
            for i in x:
                if i in dict:
                    dict[i]+=1
                else:
                    dict[i]=1
    return dict

def category(word):
    if word in wl.noun_list:
        # return 'N'
        return 100
    if word in wl.verb_list:
        # return 'V'
        return 200
    if word in wl.adverb_list:
        # return 'AV'
        return 300
    if word in wl.adjective_list:
        # return 'AJ'
        return 400
    return -100