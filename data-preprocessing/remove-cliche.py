from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import re
import os
from os import path
import string
from typing import Any

rem = string.punctuation
pattern = r"[{}]".format(rem)

class Preprocessing():
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath_sbm = basepath + "/lipad/statement-by-members/combined-all-csv/"
    datapath_oq = basepath + "/lipad/statement-by-members/combined-all-csv/"

    def __init__(self):
        super().__init__()
        #task 1 : find most common words
        self.find_cliche(self.datapath_sbm,'combined.csv')
        self.find_cliche(self.datapath_oq,'combined.csv')

    def read_csv(self,datapath,filename):
        read_csv_data = pd.read_csv(datapath+filename,delimiter=',' ,header=0)
        return read_csv_data

    def find_cliche(self,datapath,filename):
        data = self.read_csv(datapath,filename)
        #Removing all panctuations from speech text
        speechtext = data.speechtext.str.replace(pattern, '')

        #Using tf idf to find words or tokens that are less important
        vectorizer = TfidfVectorizer(decode_error='replace', token_pattern=r'(?u)\b[A-Za-z]+\b',stop_words='english',encoding='utf-8',ngram_range=(1,2))
        tfidf = vectorizer.fit_transform(speechtext)

        terms = vectorizer.get_feature_names()
        sums = tfidf.sum(axis=0)
        data = []
        for col, term in enumerate(terms):
            data.append( (term, sums[0,col] ))

        ranking = pd.DataFrame(data, columns=['term','rank'])
        print(ranking.sort_values('rank', ascending=False).nlargest(25, 'rank'))

if __name__ == '__main__':
     Preprocessing()


