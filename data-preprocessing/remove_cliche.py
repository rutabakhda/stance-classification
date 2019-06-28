from common import Common
import importlib
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import re
import os
from os import path
import string
from typing import Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class RemoveCliche():
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath_sbm = basepath + "/result/statement-by-members/"  # Datapath for Statement by Members
    datapath_oq = basepath + "/result/oral-questions/"  #Datapath for Oral Questions

    readfile_oq = 'oral-questions.csv'
    readfile_sbm = 'statement-by-members.csv'

    filename_oq = 'oral-questions-removed-cliche.csv'
    newfile_oq = os.path.join(datapath_oq, filename_oq)
    filename_sbm = 'statement-by-members-removed-cliche.csv'
    newfile_sbm = os.path.join(datapath_sbm, filename_sbm)


    def __init__(self, topic_name):
        super().__init__()

        basepath = os.path.dirname(os.path.abspath(__file__))
        datapath = basepath + "/result/{}/".format(topic_name)  # Datapath for Oral Questions

        readfile = '{}.csv'.format(topic_name)

        filename = '{}-removed-cliche.csv'.format(topic_name)
        newfile = os.path.join(datapath, filename)

        self.common = Common()

        #task 1 : find most common words
        self.found_cliche = self.find_cliche(datapath,readfile)
        self.remove_cliche(self.found_cliche, datapath,readfile,newfile)


    def find_cliche(self,datapath,filename):
        """ Calculates the most common words (cliches) in csv
        Removes the punctuations from csv
        TF-IDF to calculate most common words
        Extracting most common words

        """
        data = self.common.read_csv(datapath,filename)
        ##speechtext = data.speechtext.str.replace(r'[^\w\s\,?]','')  #Removing all panctuations from speech text
        speechtext = data.speechtext.str.lower()

        #Using tf idf to find words or tokens that are less important
        vectorizer = TfidfVectorizer(decode_error='replace',stop_words='english',encoding='utf-8')
        tfidf = vectorizer.fit_transform(speechtext.apply(lambda x: np.str_(x)))

        terms = vectorizer.get_feature_names()
        sums = tfidf.sum(axis=0)
        data = []
        for col, term in enumerate(terms):
            data.append( (term, sums[0,col] ))

        ranking = pd.DataFrame(data, columns=['term','rank'])
        cliches = ranking.sort_values('rank', ascending=False).nlargest(25, 'rank')
        found_cliches = cliches.term.values
        #print(found_cliches)
        return found_cliches

    def remove_cliche(self,found_cliche,datapath,filename,newfile):
        data = self.common.read_csv(datapath, filename)
        ##speechtext = data.speechtext.str.replace(r'[^\d\w\s\,?]','')
        speechtext = data.speechtext.str.replace("\r\n",' ')  #Removing all panctuations from speech text
        #speechtext = speechtext.str.lower()

        speechtext_without_cliche = []
        for row,speech in speechtext.iteritems():
            speech = (str(speech))
            self.first_part = ''
            self.middle_part = ''
            self.last_part = ''
            #print(speech)
            if ',' in speech:
                self.first_part_raw = speech[:speech.index(",")].lower()
                self.first_part = re.sub(r'[^\w\s\d]','',self.first_part_raw)
                self.first_part = self.first_part.split()

                temp_part = speech[speech.index(','):]
                if ',' in temp_part:
                    self.middle_part = ",".join(temp_part.split(",")[:-1]) + ','
                    self.last_part_raw = temp_part[temp_part.rindex(',') + 1:]
                    self.last_part = re.sub(r'[^\w\s\d]', '', self.last_part_raw)
                    self.last_part = self.last_part.split()

                    first_part_array = np.array(self.first_part)
                    #last_part_array = np.array(self.last_part)

                    first_part_original_string = ''
                    #last_part_original_string = ''
                    first_part_without_cliche = first_part_array[~np.isin(first_part_array, found_cliche)]
                    #last_part_without_cliche = last_part_array[~np.isin(last_part_array, found_cliche)]

                    if first_part_without_cliche.size != 0:
                        for string in np.nditer(first_part_without_cliche):
                            first_part_original_string = first_part_original_string + ' ' + str(string)
                            self.middle_part = self.middle_part.rstrip(',')

                    #if last_part_without_cliche.size != 0:
                    #    for string in np.nditer(last_part_without_cliche):
                    #        last_part_original_string = last_part_original_string + ' ' + str(string)
                    #        self.middle_part = self.middle_part.lstrip(',')

                    middle_part = self.middle_part.strip()
                    final_text = first_part_original_string+middle_part+self.last_part_raw

                    if final_text[0] == ',':
                        final_text = final_text[1:].strip()
                    speechtext_without_cliche.append(final_text)
            else:
                speechtext_without_cliche.append(speech)
        data['speechtext_without_cliche'] = speechtext_without_cliche

        if os.path.isfile(newfile):
            self.common.write_csv_without_header(newfile, data)

        else:
            self.common.write_csv_with_header(newfile, data)

    def find_controversial_topics_with_sentiment(self,datapath,filename,fullname):
        read_data = self.read_csv(datapath, filename)
        subtopic = read_data.subtopic.notnull()
        data = read_data[subtopic]

        data['lower_speechtext'] = data['speechtext_without_cliche'].str.lower()

        filtered_new_data = data[data['speechtext_sentiment_score'] < 0.3 or data['speechtext_sentiment_score'] > 0.7]
        filtered_new_data = filtered_new_data.drop(['lower_speechtext'], axis=1)
        # print(filtered_new_data)

        if os.path.isfile(fullname):
            with open(fullname, 'a+', encoding='utf-8') as f:
                filtered_new_data.to_csv(f, header=False, index=False)

        else:
            with open(fullname, 'a+', encoding='utf-8') as f:
                filtered_new_data.to_csv(f, index=False)



if __name__ == '__main__':
     RemoveCliche()


