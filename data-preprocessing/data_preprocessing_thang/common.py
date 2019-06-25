import pandas as pd
import numpy as np
from os import path
import os


class Common():
    def make_dir(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)


    def read_csv(self, datapath, filename):
        """ Reading the csv file from given path """
        read_csv_data = pd.read_csv(datapath + filename, delimiter=',', header=0)
        return read_csv_data


    def write_csv_with_header(self, filename, data):
        with open(filename, 'a', encoding='utf-8') as f:
            data.to_csv(f, index=False)


    def write_csv_without_header(self, filename, data):
        with open(filename, 'a', encoding='utf-8') as f:
            data.to_csv(f, header=False, index=False)

    def read_through(self, data_path):
        list_path = []
        for root, directory, files in os.walk(data_path):
            for folder in directory:
                self.read_through(folder)
            for file in files:
                list_path.append(root + "/" + os.path.relpath(file))
        return list_path

    def debate_list(self, file_name='data/debate_topic.txt'):
        data = pd.read_csv(filepath_or_buffer=file_name, header=None, delimiter="\t")[0]
        debate_list = []
        for item in data:
            debate_list.append(str(item))

        return debate_list[14:]
    
    def remove_duplicated_words(self, source_file='result/oral_questions.csv', keep_record="first",
                                new_file='result/unduplicated_oral_questions.csv'):
        df = pd.read_csv(filepath_or_buffer=source_file, header=0)
        df.drop_duplicates(inplace=True, subset='speechtext', keep=keep_record)
        df.to_csv(new_file, index=False)


if __name__ == '__main__':
    Common()
