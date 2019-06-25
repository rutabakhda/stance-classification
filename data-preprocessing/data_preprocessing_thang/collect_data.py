import numpy as np
import pandas as pd
import os
import csv
import shutil
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string

class Collect_data():
    def __init__(self,topic_name, topic_list, list_path):
        super().__init__()

        os.makedirs('result/{}'.format(topic_name))
        self.list_path = list_path
        # self.read_through(data_path=data_path)
        path = 'result/{}/{}-original.csv'.format(topic_name, topic_name)
        self.create_csv(path=path)
        self.write_csv(path=path, topic_list=topic_list)


    def create_csv(self,path):
        with open(path, mode="a", encoding="utf-8") as csvfile:
            field = ["basepk", "hid", "speechdate", "pid", "opid", "speakeroldname", "speakerposition", "maintopic",
                     "subtopic", "subsubtopic", "speechtext", "speakerparty", "speakerriding", "speakername",
                     "speakerurl"]
            csv_file = csv.DictWriter(f=csvfile, fieldnames=field)
            csv_file.writeheader()
        csvfile.close()

    def write_csv(self, path, topic_list):
        for file_path in self.list_path:
            data = pd.read_csv(filepath_or_buffer=file_path, header=0).values
            for row in data:
                if str(row[7]).lower() in topic_list:
                    with open(path, mode="a", encoding="utf-8") as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(row)
                    csv_file.close()
                else:
                    pass

    def read_through(self, data_path):
        for root, directory, files in os.walk(data_path):
            for folder in directory:
                self.read_through(folder)
            for file in files:
                self.list_path.append(root + "/" + os.path.relpath(file))


if __name__ == '__main__':
    Collect_data(data_path='lipad/')