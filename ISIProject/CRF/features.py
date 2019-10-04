import os
import string
import pickle

#import word_lists as wl

def isdigit(word):
    return word.isdigit()

def frequencies(fileName):
    dict={}
    with open(fileName,'r') as file:
        y=file.read()
        y=y.splitlines()
        for x in y:
            x=x.translate( string.punctuation)
            x=x.split(' ')
            for i in x:
                if i in dict:
                    dict[i]+=1
                else:
                    dict[i]=1
    return dict
pickle_file = 'list_of_words.pickle'
f = open(pickle_file, 'rb')
save = pickle.load(f)
noun_list=save['noun']
adverb_list=save['adverb']
verb_list=save['verb']
adjective_list=save['adjective']
del save

def category(word):
    if word in noun_list:
        return 'N'
    if word in verb_list:
        return 'V'
    if word in adverb_list:
        return 'AV'
    if word in adjective_list:
        return 'AJ'
    return 'X' 
    pass