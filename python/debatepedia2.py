#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import math
import pandas as pd

parser = ArgumentParser()
parser.add_argument(
    '-p',
    '--path',
    dest='path',
    default='../data/debatepedia/debatepedia-preprocessed.json',
    help='path to file',
    metavar='PATH',
)

args = parser.parse_args()

path = args.path

def split():
    ## Cross validation
    df = pd.read_json(path, orient='records')

    #### Drop duplicates
    df = df.drop_duplicates(subset='content', keep='first')

    #### Split by topic
    topics = df.topic.unique()
    n = len(topics)
    n_t = math.floor(n * 0.8)
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

if __name__ == '__main__':
    print(split())
    sys.exit(0)


