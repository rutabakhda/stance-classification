import csv
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import glob
import errno
import sys
from helper_argsme_claims_extraction import *

"""
Step 5.1: Process parliament data
by reading all the abortion speech
and check whether it is against (0), for (1), or
taking no stance (2)
"""

"""
start
"""

def get_abortion_statements(df, file_name, full_df):
    df1 = df[df["speechtext"].str.contains("abortion")]
    # save filter speechtexts
    term = file_name.split("/")[-1].strip(".csv")
    if full_df is None:
        df = df1
    else:
        df = pd.concat([full_df, df1])
    return df

def get_abortion_statements_from_all_period(path):
    files = glob.glob(path+"/*.csv") # get all csv files in folder
    count = 0
    full_df = None
    for name in files:
        print(name)
        try:
            with open(name) as f:
                # get data from file
                df = pd.read_csv(name, sep='\t', index_col=0)
                file_name = name.split("/")[-1]
                # divide by topic
                full_df = get_abortion_statements(df, name, full_df)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    df = full_df
    df["summary"] = df.apply(lambda row : summarize_argument(row['speechtext']), axis = 1)
    df["stance"] = 2
    print(list(df.columns.values.tolist()) )
    df1 = df.filter(["Role","basepk","speechtext","summary","stance"])
    for index, row in df.iterrows():
        print(row["speechtext"])
        print("current stance: ", row["stance"])
        input_number = input()
        if input_number != "" and (int(input_number) == 1 or int(input_number) == 0):
            df1.at[index, 'stance'] = int(input_number)

    df1.to_csv("parliament_abortion.csv")
    print("number of abortion related statements", df.shape[0])
    return df1

if __name__=="__main__":
    # read the folders with csv files
    path = sys.argv[1] # path to dataset by period folder 'dataset_by-period'
    get_abortion_statements_from_all_period(path)
