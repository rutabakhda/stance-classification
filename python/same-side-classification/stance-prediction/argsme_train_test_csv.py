from helper_argsme_train_test_similarity import *
from helper_argsme_exploratory_data_analysis import *
from nltk.corpus import wordnet
import nltk
import csv
import re
import pandas as pd
import numpy as np
import ast

"""
Step 4.1: Generate Train and Test csv
with 2 methods: using each sentence or using the whole argument
"""

def get_for_against_arguments(df):
    """
    Read the dataframe and
    return the for and against arguments in a tuple
    """
    for_arguments = []
    against_arguments = []
    for index, row in df.iterrows():
        # accumulate all the training arguments
        if type(row['for_arguments']) is str and row['for_arguments'] != None and row['for_arguments'] != "" and row['for_arguments'].lower() != "nan":
            for_arguments.append(". ".join(ast.literal_eval(row['for_arguments'])))
        if type(row['against_arguments']) is str and row['against_arguments'] != None and row['against_arguments'] != "" and row['against_arguments'].lower() != "nan":
            against_arguments.append(". ".join(ast.literal_eval(row['against_arguments'])))
    return (for_arguments, against_arguments)


def create_df(arguments, stance):
    targets = []
    if stance == "for":
        targets = [1] * len(arguments)
    elif stance == "against":
        targets = [0] * len(arguments)
    data_tuples = list(zip(arguments,targets))
    df = pd.DataFrame(data_tuples, columns=['question_text','target'])
    # print(df.head())
    return df

def get_for_against_claims(df):
    """
    Read the dataframe and
    return the for and against arguments in a tuple
    """
    for_arguments = []
    against_arguments = []
    for index, row in df.iterrows():
        # accumulate all the training arguments
        if type(row['for_arguments']) is str and row['for_arguments'] != None and row['for_arguments'] != "" and row['for_arguments'].lower() != "nan":
            for_arguments = for_arguments + ast.literal_eval(row['for_arguments'])
        if type(row['against_arguments']) is str and row['against_arguments'] != None and row['against_arguments'] != "" and row['against_arguments'].lower() != "nan":
            against_arguments = against_arguments + ast.literal_eval(row['against_arguments'])
    return (for_arguments, against_arguments)

if __name__=="__main__":
    df = read_csv("../data/argsme_all_claims_abortion/argsme_all_claims_abortion.csv")
    # train and test using each sentence
    (for_arguments, against_arguments) = get_for_against_claims(df)
    # train and test using full argument
    # (for_arguments, against_arguments) = get_for_against_arguments(df)
    for_arguments = clean_data_2(for_arguments)
    against_arguments = clean_data_2(against_arguments)
    df1 = create_df(for_arguments, "for")
    df0 = create_df(against_arguments, "against")
    df = pd.concat([df1, df0], axis=0)
    df = df.sample(frac=1).reset_index(drop=True)
    # drop rows contain empty string
    filter = df["question_text"] != ""
    df = df[filter]
    # print(df.head())
    num_rows = df.shape[0]
    num_train = int(num_rows * 0.8)
    df_train = df.iloc[:num_train, :]
    df_test = df.iloc[num_train:, :]
    df_train.head()
    df_test.head()
    print(df_train)
    print(df_test)
    df_train.to_csv(r"train.csv")
    df_test.to_csv(r"test.csv")
