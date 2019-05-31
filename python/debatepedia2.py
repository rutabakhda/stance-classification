#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import math
import pandas as pd
import numpy as np
import shutil

parser = ArgumentParser()
parser.add_argument(
    '-p',
    '--path',
    dest='path',
    default='../data/debatepedia/debatepedia-preprocessed.json',
    help='path to file',
    metavar='PATH',
)

parser.add_argument(
    '-m',
    '--mode',
    dest='mode',
    default='split_json',
    help='processing mode',
    metavar='MODE',
)

parser.add_argument(
    '-r',
    '--random',
    dest='random',
    default='split_json',
    help='processing mode',
    metavar='RANDOM',
)


args = parser.parse_args()

path = args.path
mode = args.mode
random = args.random

# path = "../data/debatepedia/debatepedia-preprocessed.json"
def split_json():
    ## Cross validation
    df = pd.read_json(path, orient='records')

    #### Drop duplicates
    df = df.drop_duplicates(subset='content', keep='first')

    #### Split by topic
    topics = df.topic.unique()
    n = len(topics)
    n_t = math.floor(n * 0.8)
    if(int(random)==1):
        df.iloc[np.random.permutation(len(df))]
        n1 = len(df)
        n1_t = math.floor(n1 * 0.8)
        df_tr = df[:n1_t]
        df_te = df[n1_t:]

    else:
        topics_tr = topics[:n_t]
        topics_te = topics[n_t:]
        df_tr = df[df['topic'].isin(topics_tr)]
        df_te = df[df['topic'].isin(topics_te)]

    #### Write to files
    t = datetime.now()
    dt = str(t)[:19].replace(' ', '_')
    parent = str(Path(path).parent)
    split_path = os.path.join(parent, dt)
    if not os.path.exists(split_path):
        os.mkdir(split_path)
    file_name = path.split('/')[-1]
    train_path = os.path.join(split_path, file_name.replace('.json',
                                                            '_train.json'))
    test_path = os.path.join(split_path, file_name.replace('.json',
                                                           '_test.json'))
    df_tr.to_json(train_path, orient='records')
    df_te.to_json(test_path, orient='records')
    return os.path.abspath(split_path)


# path = "../data/debatepedia/xmi"
def split_ksets(num_fold):
    num_fold = 5
    #### Write to files
    t = datetime.now()
    t

    dt = str(t)[:19].replace(' ', '_')
    parent = str(Path(path).parent)
    split_path = os.path.join(parent, dt)
    if not os.path.exists(split_path):
        os.mkdir(split_path)
    # print(split_path)
    for i in range(1, num_fold + 1):
        split_kfold(num_fold, i, split_path)
    return os.path.abspath(split_path)

def split_kfold(num_fold, index, split_path):
    """
    Split folders into 80% training and 20% testing based on index
    """
    # walk through folders
    folders = []
    for entry in os.scandir(path):
        if entry.is_dir():
            folders.append(entry.path)
    # for f in folders:
    #     print(f)
    test_ratio = 1 / num_fold
    test_len = int(len(folders) * test_ratio)
    t1 = int(len(folders) * test_ratio * (index - 1))
    t2 = t1 + test_len
    # split test set according to t1 and t2
    train = folders[:t1] + folders[t2:]
    test = folders[t1:t2]
    parent = os.path.join(split_path, "set" + str(index))

    # create train path and test path
    train_path = os.path.join(parent, "train")
    test_path = os.path.join(parent, "test")
    # print("train path: " + train_path)
    # print("test path: " + test_path)

    # copy the folders to train path or test path
    # according to the split

    for f in train:
        folder_name = f.split("/")[-1]
        write_path = os.path.join(train_path, folder_name)
        copy_folder(f, write_path)
    for f in test:
        folder_name = f.split("/")[-1]
        write_path = os.path.join(test_path, folder_name)
        copy_folder(f, write_path)


def copy_folder(src, des):
    try:
        shutil.copytree(src, des)
        # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)



if __name__ == '__main__':
    if mode=="split_json":
        print(split_json())
    elif mode=="split_kfold":
        print(split_ksets(5))
    sys.exit(0)


