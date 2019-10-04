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
            # print(line,'    <--hep\n')    
            label_line=x[i+1]
            # print(label_line,'  \n')
            # g = input('') 
            label_dict={}
            labels=label_line.split(' ')
            # print('labels === ',labels,' yup\n')
            for label in labels:
                # print('label=== ' ,label,' \n')
                pos=label.find(':')
                # print('pos === ',pos,'<--har\n')
                # print(label[pos+1:],'       ',label[:label.find(':')],'\n\n\n')
                label_dict[label[pos+1:]]=label[:label.find(':')]
            line_list=[]
            # line=line.translate( string.punctuation)
            exclude = set(string.punctuation)
            line = ''.join(ch for ch in line if ch not in exclude)
            # print('line == ',line,'    end \n')
            words=line.split(' ')
            # print('words == ',words,'    end \n')
            for word in words:
                cat=features.category(word)
                if word in label_dict:
                    line_list.append([word,cat,label_dict[word]])
                else:
                    line_list.append([word,cat,'0'])
            listt.append(line_list)
            # print(line_list,' \n\n\n\n\n\n')
            # print(listt,' \n')
    return listt

