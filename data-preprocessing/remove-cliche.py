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
    datapath_sbm = basepath + "/lipad/statement-by-members/combined-all-csv/"  # Datapath for Statement by Members
    datapath_oq = basepath + "/lipad/oral-questions/combined-all-csv/"  #Datapath for Oral Questions

    def __init__(self):
        super().__init__()
        #task 1 : find most common words
        self.find_cliche(self.datapath_sbm,'combined.csv')
        self.find_cliche(self.datapath_oq,'combined.csv')

        #Task 2 : Report 10 most occurring subtopic in Oral Questions and Statement by Members
        print("Subtopic 10 most occurence for Oral Questions")
        self.subtopic_most_count(self.datapath_oq,'combined-oral-questions.csv')
        print("Subtopic 10 most occurence for Statement by Members")
        self.subtopic_most_count(self.datapath_sbm,'combined-statement-by-members.csv')

        #Task 3 : Finding controversial topics in Oral Questions and Statement by Members
        self.outname = 'controversial-data.csv'
        self.fullname_oq = os.path.join(self.datapath_oq, self.outname)
        self.find_controversial_topics(self.datapath_oq, 'combined-oral-questions.csv', self.fullname_oq)

        self.fullname_sbm = os.path.join(self.datapath_sbm, self.outname)
        self.subtopic_most_count(self.datapath_sbm, 'combined-statement-by-members.csv',self.fullname_sbm)

        #Task 4 : Report 10 most occurring subtopics in Controversial Oral Questions and Statement by Members
        print("Subtopic 10 most occurence for Controversial Oral Questions")
        self.subtopic_most_count(self.datapath_oq, 'controversial-data.csv')
        print("Subtopic 10 most occurence for Controversial Statement by Members")
        self.subtopic_most_count(self.datapath_sbm, 'controversial-data.csv')


    def read_csv(self,datapath,filename):
        """ Reading the csv file from given path """
        read_csv_data = pd.read_csv(datapath+filename,delimiter=',' ,header=0)
        return read_csv_data

    def find_cliche(self,datapath,filename):
        """ Calculates the most common words (cliches) in csv
        Removes the punctuations from csv
        TF-IDF to calculate most common words
        Extracting most common words

        """
        data = self.read_csv(datapath,filename)
        speechtext = data.speechtext.str.replace(pattern, '')  #Removing all panctuations from speech text

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

    def subtopic_most_count(self,datapath,filename):
        """" Reading csv and finding 10 subtopics with most occurence """
        data = self.read_csv(datapath, filename)
        print(data['subtopic'].value_counts().nlargest(10))

    def find_controversial_topics(self,datapath,filename,fullname):
        read_data = self.read_csv(datapath, filename)
        subtopic = read_data.subtopic.notnull()
        data = read_data[subtopic]

        data['lower_subtopic'] = data['subtopic'].str.lower()
        data['lower_speechtext'] = data['speechtext'].str.lower()

        name = "wikipedia-controversial-issues - Copy.txt"
        with open(name, 'r', encoding='utf8') as f:
            for line in f:
                # for word in line.split():
                line = line.lower()
                line = line.strip()
                print(line)

                new_data = data[data['lower_subtopic'].str.contains(line)]
                filtered_new_data = data[data['lower_speechtext'].str.count(line) > 1]
                filtered_new_data = filtered_new_data.drop(['lower_speechtext', 'lower_subtopic'], axis=1)
                # print(filtered_new_data)

                if os.path.isfile(fullname):
                    with open(fullname, 'a', encoding='utf-8') as f:
                        filtered_new_data.to_csv(f, header=False, index=False)

                else:
                    with open(fullname, 'a', encoding='utf-8') as f:
                        filtered_new_data.to_csv(f, index=False)


if __name__ == '__main__':
     Preprocessing()


