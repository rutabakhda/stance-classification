"""
@author: Thang Nguyen <nhthang1009@gmail.com>
"""
import pandas as pd
from torch.utils.data.dataset import Dataset
import csv
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np


class MyDataset(Dataset):

    def __init__(self, data_path, dict_path, max_length_sentences=30, max_length_word=35):
        super(MyDataset, self).__init__()

        data = pd.read_csv(data_path, sep='\t', header=0).values

        self.texts_1, self.texts_2, self.labels = zip(*data)
        self.dict = pd.read_csv(filepath_or_buffer=dict_path, header=None, sep=" ", quoting=csv.QUOTE_NONE,
                                usecols=[0]).values
        self.dict = [word[0] for word in self.dict]
        self.max_length_sentences = max_length_sentences
        self.max_length_word = max_length_word
        self.num_classes = len(set(self.labels))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        label = self.labels[index]
        text1 = self.texts_1[index]
        document1_encode = [
            [self.dict.index(word) if word in self.dict else -1 for word in word_tokenize(text=sentences)] for sentences
            in
            sent_tokenize(text=text1)]

        for sentences in document1_encode:
            if len(sentences) < self.max_length_word:
                extended_words = [-1 for _ in range(self.max_length_word - len(sentences))]
                sentences.extend(extended_words)

        if len(document1_encode) < self.max_length_sentences:
            extended_sentences = [[-1 for _ in range(self.max_length_word)] for _ in
                                  range(self.max_length_sentences - len(document1_encode))]
            document1_encode.extend(extended_sentences)

        document1_encode = [sentences[:self.max_length_word] for sentences in document1_encode][
                           :self.max_length_sentences]

        document1_encode = np.stack(arrays=document1_encode, axis=0)
        document1_encode += 1

        text2 = self.texts_2[index]
        document2_encode = [
            [self.dict.index(word) if word in self.dict else -1 for word in word_tokenize(text=sentences)] for sentences
            in
            sent_tokenize(text=text2)]

        for sentences in document2_encode:
            if len(sentences) < self.max_length_word:
                extended_words = [-1 for _ in range(self.max_length_word - len(sentences))]
                sentences.extend(extended_words)

        if len(document2_encode) < self.max_length_sentences:
            extended_sentences = [[-1 for _ in range(self.max_length_word)] for _ in
                                  range(self.max_length_sentences - len(document2_encode))]
            document2_encode.extend(extended_sentences)

        document2_encode = [sentences[:self.max_length_word] for sentences in document2_encode][
                           :self.max_length_sentences]

        document2_encode = np.stack(arrays=document2_encode, axis=0)
        document2_encode += 1
        return document1_encode.astype(np.int64), document2_encode.astype(np.int64), label


if __name__ == '__main__':
    test = MyDataset(data_path="../data/train.csv", dict_path="../data/glove.6B.50d.txt")
    print(test.__getitem__(index=2))
