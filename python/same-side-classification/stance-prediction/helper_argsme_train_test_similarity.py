from nltk.corpus import stopwords

from nltk.corpus import stopwords
import ast
stop_words = stopwords.words('english')
from helper_argsme_claims_extraction import *
import csv
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import itertools

def read_csv(file_name):
    """
    Read csv file and
    return the dataframe
    """
    with open(file_name) as f:
        # get data from file
        df = pd.read_csv(f, sep='\t')
    return df

def divide_df(df, fraction, saved):
    """
    Divide dataset based on fraction
    and return the training and test dataframe,
    save if require
    """
    df_test = df.sample(frac=fraction)
    df_training = df.loc[~df.index.isin(df_test.index)]
    df_test = df_test.sort_index()
    #
    # save to files
    if saved:
        df_training.to_csv(r'training_abortion_arguments_stance.csv',index=True,sep='\t')
        df_test.to_csv(r'test_abortion_arguments_stance.csv',index=True,sep='\t')
    return (df_training, df_test)

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

def rank_arguments(arguments):
    """
    Read all arguments and rank by sentence similarity
    and return ranked arguments
    """
    # generate similarity matrix across topics
    sentence_similarity_martix = build_similarity_matrix(arguments, stop_words)
    # rank topics
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    # sort the rank
    ranked_sentences = [x for _,x in sorted(zip(scores,arguments))]
    return ranked_sentences

def write_list_to_file(file_name, list_string):
    """
    Write list of arguments
    to file, each line each sentence
    """
    with open(file_name, 'w') as f:
        for item in list_string:
            f.write("%s\n" % str(item))

def predict_stance(argument, training_arguments, results):
    """
    Loop through each sentence of the argument and
    compare with the training arguments
    append the intermediate result (sentence, most_similar_sentence, highest_similarity_score) to results array
    """
    result = []
    for_count = 0
    against_count = 0
    category = 0
    for_arguments = training_arguments[0]
    against_arguments = training_arguments[1]
    for sentence in argument:
        highest_similarity = 0
        most_similar_sentence = ""
        side = "for"
        for sentence1 in for_arguments:
            similarity = sentence_similarity(sentence, sentence1)
            if similarity>highest_similarity:
                highest_similarity = similarity
                most_similar_sentence = sentence1
                side = "for"
        for sentence2 in against_arguments:
            similarity = sentence_similarity(sentence, sentence2)
            if similarity>highest_similarity:
                highest_similarity = similarity
                most_similar_sentence = sentence2
                side = "against"
        if side == "for":
            for_count += 1
        elif side == "against":
            against_count += 1
        results.append((sentence, most_similar_sentence, highest_similarity))
    if for_count > against_count:
        return "for"
    elif against_count > for_count:
        return "against"
    else:
        return "uncategory"

def test_arguments_similarity(save_file, training_arguments, df_test, similarity_results_file_name):
    """
    Loop through all testing data, predict the stance based on the arguments;
    save the text with actual and predicted stance into a file
    compare and print the overall result
    Return confusion matrix
    """
    similarity_results = []
    test_arguments_results = []
    count_for_correct = 0
    count_against_correct = 0
    count_for_incorrect = 0
    count_against_incorrect = 0
    for index, row in df_test.iterrows():
        # get argument text and stance
        if type(row['for_arguments']) is str and row['for_arguments'] != None and row['for_arguments'] != "" and row['for_arguments'].lower() != "nan":
            argument = ast.literal_eval(row['for_arguments'])
            stance = "for"
        if type(row['against_arguments']) is str and row['against_arguments'] != None and row['against_arguments'] != "" and row['against_arguments'].lower() != "nan":
            argument = ast.literal_eval(row['against_arguments'])
            stance = "against"
        # predict and compare
        predicted_stance = predict_stance(argument, training_arguments, similarity_results)
        # add to test_arguments_results
        test_arguments_results.append((argument, stance, predicted_stance))
        if predicted_stance == stance:
            if predicted_stance == "for":
                count_for_correct += 1
            elif predicted_stance == "against":
                count_against_correct += 1
        else:
            if predicted_stance == "for":
                count_for_incorrect += 1
            elif predicted_stance == "against":
                count_against_incorrect += 1
        print("-", end = "")
    # write overall results and similarity results of each sentence to file
    write_similarity_results_to_file(similarity_results_file_name, similarity_results)
    write_to_test_results(save_file, test_arguments_results)
    return np.array([[count_for_correct, count_against_incorrect],
                     [count_for_incorrect, count_against_correct]])

def write_to_test_results(file_name, results):
    """
    Write all test results to csv file in 3 columns:
    arguments, stance, predicted_stance
    """
    with open(file_name, 'w') as f:
        f.write('{0}\t{1}\t{2}\n'.format("arguments", "stance", "predicted_stance"))
        for my_tuple in results:
            f.write('{0}\t{1}\t{2}\n'.format(my_tuple[0], my_tuple[1], my_tuple[2]))

def write_similarity_results_to_file(file_name, results):
    """
    Write all result to csv file in 3 columns:
    sentence, most_similar_sentence, highest_similarity_score
    """
    with open(file_name, 'w') as f:
        f.write('{0}\t{1}\t{2}\n'.format("sentence", "most_similar_sentence", "highest_similarity_score"))
        for my_tuple in results:
            f.write('{0}\t{1}\t{2}\n'.format(my_tuple[0], my_tuple[1], my_tuple[2]))

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    Plots the confusion matrix.
    """
    cm = np.array(cm)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + classes)
    ax.set_yticklabels([''] + classes)
    thresh = (cm.max()+cm.min()) / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], "d"),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

def plot_accuracy(confusion_matrix):
    """
    Plot the accuracy.
    """
    cm = np.array(confusion_matrix)
    T = cm[0,0] + cm[1,1]
    F = cm[1,0] + cm[0,1]
    # normalize
    T_norm = T/(T+F)
    F_norm = F/(T+F)
    # labels
    labels = ["Correct", "Incorrect"]
    sizes = [T_norm, F_norm]
    colors = ['lightcoral', 'lightskyblue']
    plt.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Accuracy")
    plt.show()
