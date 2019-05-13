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

class Preprocessing():
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath_sbm = basepath + "/lipad1/statement-by-members/"  # Datapath for Statement by Members
    datapath_oq = basepath + "/lipad1/oral-questions/"  #Datapath for Oral Questions

    def __init__(self):
        super().__init__()

        #task 1 : find most common words
        global result
        result = open("week2.txt", "a+")
        result.write("=== Cliches in Oral Questions ===")
        result.write(" ")
        #self.found_cliche = self.find_cliche(self.datapath_oq,'unduplicated_oral_questions.csv')
        #self.remove_cliche(self.found_cliche, self.datapath_oq, 'unduplicated_oral_questions.csv')

        #result.write("=== Cliches in Statement by Members ===")
        #result.write(" ")
        #self.found_cliche = self.find_cliche(self.datapath_sbm,'unduplicated_statements_by_members.csv')
        #self.remove_cliche(self.found_cliche, self.datapath_sbm, 'unduplicated_statements_by_members.csv')


        #Task 2 : Report 10 most occurring subtopic in Oral Questions and Statement by Members
        #result.write("=== Subtopic 10 most occurence for Oral Questions ===")
        #result.write(" ")
        #print("Subtopic 10 most occurence for Oral Questions")
        #self.subtopic_most_count(self.datapath_oq,'unduplicated_oral_questions.csv')
        #result.write("=== Subtopic 10 most occurence for Statement by Members ===")
        #result.write(" ")
        #print("Subtopic 10 most occurence for Statement by Members")
        #self.subtopic_most_count(self.datapath_sbm,'unduplicated_statements_by_members.csv')

        #Task 3 : Finding controversial topics in Oral Questions and Statement by Members

        self.outname = 'controversial-data.csv'
        #self.fullname_oq = os.path.join(self.datapath_oq, self.outname)
        #self.find_controversial_topics(self.datapath_oq, 'removed-cliche.csv', self.fullname_oq)

        #self.fullname_sbm = os.path.join(self.datapath_sbm, self.outname)
        #self.find_controversial_topics(self.datapath_sbm, 'removed-cliche.csv',self.fullname_sbm)


        #Task 4 : Report 10 most occurring subtopics in Controversial Oral Questions and Statement by Members
        #result.write("=== Subtopic 10 most occurence for Controversial Oral Questions ===")
        #result.write(" ")
        #print("Subtopic 10 most occurence for Controversial Oral Questions")
        #self.subtopic_most_count(self.datapath_oq, 'controversial-data.csv')
        #result.write("=== Subtopic 10 most occurence for Controversial Statement by Members ===")
        #result.write(" ")
        #print("Subtopic 10 most occurence for Controversial Statement by Members")
        #self.subtopic_most_count(self.datapath_sbm, 'controversial-data.csv')

        #Task 5 : Sentiment Analysis for speechtext
        self.do_sentiment_analysis(self.datapath_oq,'removed-cliche.csv')
        self.do_sentiment_analysis(self.datapath_sbm, 'removed-cliche.csv')

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
        speechtext = data.speechtext.str.replace(r'[^\w\s\,?]','')  #Removing all panctuations from speech text
        speechtext = speechtext.str.lower()

        #Using tf idf to find words or tokens that are less important
        vectorizer = TfidfVectorizer(decode_error='replace',stop_words='english',encoding='utf-8')
        tfidf = vectorizer.fit_transform(speechtext.apply(lambda x: np.str_(x)))

        terms = vectorizer.get_feature_names()
        sums = tfidf.sum(axis=0)
        data = []
        for col, term in enumerate(terms):
            data.append( (term, sums[0,col] ))

        ranking = pd.DataFrame(data, columns=['term','rank'])
        result.write(str(ranking.sort_values('rank', ascending=False).nlargest(25, 'rank')))
        result.write(" ")
        cliches = ranking.sort_values('rank', ascending=False).nlargest(25, 'rank')
        found_cliches = cliches.term.values
        #print(found_cliches)
        return found_cliches

    def remove_cliche(self,found_cliche,datapath,filename):
        data = self.read_csv(datapath, filename)
        speechtext = data.speechtext.str.replace(r'[^\d\w\s\,?]','')
        speechtext = speechtext.str.replace("\r\n",' ')  #Removing all panctuations from speech text
        speechtext = speechtext.str.lower()

        speechtext_without_cliche = []
        for row,speech in speechtext.iteritems():
            speech = (str(speech))
            self.first_part = ''
            self.middle_part = ''
            self.last_part = ''
            #print(speech)
            if ',' in speech:
                self.first_part = speech[:speech.index(",")].split()
                temp_part = speech[speech.index(','):]
                if ',' in temp_part:
                    self.middle_part = ",".join(temp_part.split(",")[:-1]) + ','
                    self.last_part = temp_part[temp_part.rindex(',') + 1:].split()

                    first_part_array = np.array(self.first_part)
                    last_part_array = np.array(self.last_part)

                    first_part_original_string = ''
                    last_part_original_string = ''
                    first_part_without_cliche = first_part_array[~np.isin(first_part_array, found_cliche)]
                    last_part_without_cliche = last_part_array[~np.isin(last_part_array, found_cliche)]

                    if first_part_without_cliche.size != 0:
                        for string in np.nditer(first_part_without_cliche):
                            first_part_original_string = first_part_original_string + ' ' + str(string)
                            middle_part = self.middle_part.rstrip(',')

                    if last_part_without_cliche.size != 0:
                        for string in np.nditer(last_part_without_cliche):
                            last_part_original_string = last_part_original_string + ' ' + str(string)
                            self.middle_part = self.middle_part.lstrip(',')

                    middle_part = self.middle_part.strip()
                    speechtext_without_cliche.append(first_part_original_string+middle_part+last_part_original_string)
            else:
                speechtext_without_cliche.append(speech)
        data['speechtext_without_cliche'] = speechtext_without_cliche
        new_filename = 'removed-cliche.csv'
        data.to_csv(datapath+new_filename)

    def do_sentiment_analysis(self,datapath,filename):
        original_data = self.read_csv(datapath, filename)
        data = original_data[original_data['speechtext_without_cliche'].notnull()]
        speechtext = data.speechtext_without_cliche.str.replace(r'[^\d\w\s\,?]','')
        speechtext = speechtext.str.replace("\r\n",' ')  #Removing all panctuations from speech text
        speechtext = speechtext.str.lower()

        analyser = SentimentIntensityAnalyzer()
        speechtext_sentiment_score = []

        for row,speech in speechtext.iteritems():
            sentiment = analyser.polarity_scores(speech)
            sentiment_score = sentiment['compound']
            speechtext_sentiment_score.append(sentiment_score)

        data['speechtext_sentiment_score'] = speechtext_sentiment_score
        new_filename = 'removed-cliche-sentiment-score.csv'
        data.to_csv(datapath+new_filename)


    def subtopic_most_count(self,datapath,filename):
        """" Reading csv and finding 10 subtopics with most occurence """
        data = self.read_csv(datapath, filename)
        result.write(str(data['subtopic'].value_counts().nlargest(10)))
        result.write(" ")
        print(data['subtopic'].value_counts().nlargest(10))

    def find_controversial_topics(self,datapath,filename,fullname):
        read_data = self.read_csv(datapath, filename)
        subtopic = read_data.subtopic.notnull()
        data = read_data[subtopic]

        data['lower_subtopic'] = data['subtopic'].str.lower()
        data['lower_speechtext'] = data['speechtext_without_cliche'].str.lower()

        name = "wikipedia-controversial-issues - Copy.txt"
        with open(name, 'r', encoding='utf8') as f:
            for line in f:
                # for word in line.split():
                line = line.lower()
                line = line.strip()
                #print(line)

                new_data = data[data['lower_subtopic'].str.contains(line)]
                filtered_new_data = new_data[data['lower_speechtext'].str.count(line) > 1]
                filtered_new_data = filtered_new_data.drop(['lower_speechtext', 'lower_subtopic'], axis=1)
                # print(filtered_new_data)

                if os.path.isfile(fullname):
                    with open(fullname, 'a+', encoding='utf-8') as f:
                        filtered_new_data.to_csv(f, header=False, index=False)

                else:
                    with open(fullname, 'a+', encoding='utf-8') as f:
                        filtered_new_data.to_csv(f, index=False)



if __name__ == '__main__':
     Preprocessing()


