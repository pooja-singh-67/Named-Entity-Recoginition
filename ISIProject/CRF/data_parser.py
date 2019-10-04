import os
import features
import string
import pickle as pickle



def load(fileName):
    listt=[]
    
    with open(fileName,'r') as file:
        x=file.read()
        x=x.splitlines()
        for i in range(0,len(x),2):
            line=x[i]
            label_line=x[i+1]
            label_dict={}
            labels=label_line.split(' ')
            for label in labels:
                pos=label.find(':')
                label_dict[label[pos+1:]]=label[:label.find(':')]
            line_list=[]
            line=line.translate( string.punctuation)
            words=line.split(' ')
            for word in words:
                cat=features.category(word)
                if word in label_dict:
                    line_list.append([word,cat,label_dict[word]])
                else:
                    line_list.append([word,cat,'0'])
            listt.append(line_list)
    return listt

