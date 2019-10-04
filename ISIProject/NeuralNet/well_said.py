from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import features #functions defining word features
import data_parser #function(s) to load train and test data from .txt files
import pickle as pickle
import pprint
import csv
import numpy as np
import random
import pickle

# test_sents=data_parser.load('test.txt')
#sents is a list of lists, each list corresponding to a sentence in the 'train.txt'
#The list has the format (word,category,label) for each word in sentence, each label corresponding to
#the entity of the word. For current training datasets, these are-
#(Date-Date, Num-Number of tickets, Dest-Destination, Src-Source Location)
#category is retreived from the Hindi WordNet database,return N for noun,
#V for verb,AV for adverb and AJ for adjective. Return X if not found in the database 
# print(train_sents,'  \n')
# for i in train_sents:
#     for x in i:
#         print(x[0],x[1],x[2])

def word2features(sent, i,freq,word_index):
    word = sent[i][0]
    category = sent[i][1]
    if(word not in freq): freq[word]=0
    feat = {
        'bias':1,
        #'word=' + word,
        'word.isdigit':features.isdigit(word),
        'category':str(category),
        'freq':float(freq[word]),
        'BOS':'0',
        'EOS':'0',
    }
    if i > 0:
        word1 = sent[i-1][0]
        if(word1 not in freq): freq[word1]=0
        category1 = sent[i-1][1]
        feat.update({
            '-1:word':word_index[word1],
            '-1:word.isdigit':features.isdigit(word1),
            '-1:category':str(category1),
            '-1:freq':float(freq[word1]),
        })
    else:
        feat.update({'BOS':'1'})
        feat.update({
            '-1:word':float(-1),
            '-1:word.isdigit':float(555.0),
            '-1:category':float(555.0),
            '-1:freq':float(555.0),
        })
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        if(word1 not in freq): freq[word1]=0
        category1 = sent[i+1][1]
        feat.update({
            '+1:word':word_index[word1],
            '+1:word.isdigit':features.isdigit(word1),
            '+1:category':str(category1),
            '+1:freq':float(freq[word1]),
        })
    else:
        feat.update({'EOS':'1'})
        feat.update({
            '+1:word':float(-1),
            '+1:word.isdigit':float(333.0),
            '+1:category':float(333.0),
            '+1:freq':float(333.0),
        })        
    return feat


def sent2features(sent,freq,word_index):
    # for i in range(len(sent)):
    #     print(word2features(sent, i),'\n\n')
    return [word2features(sent, i,freq,word_index) for i in range(len(sent))]

def sent2labels(sent,freq,word_index):
    return [label for word, category, label in sent]

def sent2tokens(sent,freq,word_index):
    return [word for word,postag,label in sent]


def create_feature_sets_and_labels(file1,test_size = 0.2):
    freq=features.frequencies(file1)
    word_index=features.index_word(file1)
    #returns a dictionary of word frequencies in the file
    # print(freq)
    train_sents=data_parser.load(file1)
    print(train_sents,'\n\n\n')
    features_to_feed=[] 
    for var in train_sents:
        new_train_data = sent2features(var,freq,word_index)
        new_labels=sent2labels(var,freq,word_index)
        training_data=[]
        # print(new_labels[0:2],'   \n')
        # print(len(new_train_data))
        for k in range(0,len(new_train_data)-3):
            # print(var[k:k+4],'\n')
            t = k 
            training_data=[]
            while t<k+3:
                new_list=[]
                for i in new_train_data[t]:
                    new_list.append(float(new_train_data[t][i]))
                # print(new_list,'\n\n\n\n')    
                training_data=training_data+new_list
                t=t+1   
            # print([training_data,new_labels[k:k+4]],'\n')   
            class_list = [0,0,0,0,0]
            count = 0
            # for itr in range(0,4):    
            #     if new_labels[k+itr]=='0':
            #         class_list[count+4]=1
            #     elif new_labels[k+itr]=='D':
            #         class_list[count+0]=1
            #     elif new_labels[k+itr]=='S':
            #         class_list[count+1]=1
            #     elif new_labels[k+itr]=='T':
            #         class_list[count+2]=1
            #     elif new_labels[k+itr]=='N':
            #         class_list[count+3]=1 
            #     count = count+5           
            if new_labels[k+1]=='0':
                class_list[4]=1
            elif new_labels[k+1]=='P':
                class_list[0]=1
            elif new_labels[k+1]=='S':
                class_list[1]=1
            elif new_labels[k+1]=='C':
                class_list[2]=1
            elif new_labels[k+1]=='D':
                class_list[3]=1    

            features_to_feed.append([training_data,class_list])
        # break    
    # print(len(features_to_feed[0][0]),'    ',features_to_feed,'\n')
    count =1
    one =0
    two =0
    three = 0 
    four = 0
    other = 0 
    new_last_list = []
    # new_last_list = new_last_list+features_to_feed
    entity=0
    for item in features_to_feed:
        if item[1][4]==1 and entity != 500:
            new_last_list.append(item)
            entity=entity+1
        elif item[1][4]!=1:
            new_last_list.append(item)         
    
    for item in new_last_list:
        print(count,'  ',len(item[1]),'   ',item[1],'\n')   
        count = count + 1
        if item[1][0]==1:
            one = one + 1 
        if item[1][1]==1:
            two = two + 1 
        if item[1][2]==1:
            three = three + 1 
        if item[1][3]==1:
            four = four + 1 
        if item[1][4]==1:
            other = other + 1 
    print(one,' ',two,' ',three,' ',four,' ',other,' \n')
    temp_list =[]
    temp_list = temp_list+new_last_list
    for i in range(0,int(other/one)):
        for item in temp_list:
            if item[1][0]==1:
                new_last_list.append(item)  
                print(item,'  \n')  
    for i in range(0,int(other/two)):
        for item in temp_list:
            if item[1][1]==1:
                new_last_list.append(item)
    for i in range(0,int(other/three)):
        for item in temp_list:
            if item[1][2]==1:
                new_last_list.append(item)
    for i in range(0,int(other/four)):
        for item in temp_list:
            if item[1][3]==1:
                new_last_list.append(item)
    print('done\n')
    one =0
    two =0
    three = 0 
    four = 0
    other = 0 
    for item in new_last_list:
        print(count,'  ',len(item[1]),'   ',item[1],'\n')   
        count = count + 1
        if item[1][0]==1:
            one = one + 1 
        if item[1][1]==1:
            two = two + 1 
        if item[1][2]==1:
            three = three + 1 
        if item[1][3]==1:
            four = four + 1 
        if item[1][4]==1:
            other = other + 1 
    print(one,' ',two,' ',three,' ',four,' ',other,' \n')
    


    # print(final_liist) 
    # features_to_feed=[]
    # features_to_feed.append(final_liist)

    # comment start here 

    # for a_list in features_to_feed:
    #     print(a_list,'\n') 

    random.shuffle(new_last_list)
    new_last_list = np.array(new_last_list)   

    testing_size = int(test_size*len(new_last_list))

    train_x = list(new_last_list[:,0][:-testing_size])
    train_y = list(new_last_list[:,1][:-testing_size])
    test_x = list(new_last_list[:,0][-testing_size:])
    test_y = list(new_last_list[:,1][-testing_size:])

    return train_x,train_y,test_x,test_y

    #comment ends here 
    # print(word_index)
# train_x,train_y,test_x,test_y  = create_feature_sets_and_labels('full_data_set.txt')
# print(len(train_x[0]))
# create_feature_sets_and_labels('train_p.txt')