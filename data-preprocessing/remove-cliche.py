from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import re
import os
from os import path
import string
rem = string.punctuation
pattern = r"[{}]".format(rem)

class Preprocessing():
    def __init__(self):
        super().__init__()

        #task 1 : find most common words
        basepath = path.dirname(__file__)
        datapath-sbm = basepath+"/lipad/statement-by-members/combined-all-csv/"
        datapath-oq = basepath+"/lipad/statement-by-members/combined-all-csv/"
        self.find_cliche(datapath-sbm,'combined.csv')
        self.find_cliche(datapath-oq,'combined.csv')

    def find_cliche(self,datapath,filename):
        
        #datapath = basepath+"/lipad/statement-by-members/combined-all-csv/"
        data = pd.read_csv(datapath+filename,delimiter=',' ,header=0, names=['speechtext'])
        speechtext = data.speechtext.str.replace(pattern, '')


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


