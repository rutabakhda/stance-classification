import os
from os import walk
import re
import nltk
import pickle
import pandas as pd
import numpy as np
import string
import scipy
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath +'/data/Data_Research_Project/Dataset_2/args_pairs/'
file = 'testing-cross-domain.csv'
data = pd.read_csv(datapath + file,encoding = "ISO-8859-1")


gloveFile = "glove.6B\\glove.6B.50d.txt"

def loadGloveModel(gloveFile):
    print ("Loading Glove Model")
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print ("Done.",len(model)," words loaded!")
    return model



def preprocess(raw_text):
    
    # keep only words
    text = re.sub(r'^https?:\/\/.*[\r\n]*', ' ', raw_text, flags=re.MULTILINE)
    letters_only_text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    
    # convert to lower case and split 
    words = letters_only_text.lower()
    return words

def cosine_distance_between_two_words(word1, word2):
    import scipy
    return (1- scipy.spatial.distance.cosine(model[word1], model[word2]))

def calculate_heat_matrix_for_two_sentences(s1,s2):
    s1 = preprocess(s1)
    s2 = preprocess(s2)
    result_list = [[cosine_distance_between_two_words(word1, word2) for word2 in s2] for word1 in s1]
    result_df = pd.DataFrame(result_list)
    result_df.columns = s2
    result_df.index = s1
    return result_df

def cosine_distance_wordembedding_method(s1, s2):
    
    s1_processed = preprocess(s1)
    s2_processed = preprocess(s2)
    
    S1 = " ".join(filter(lambda x:x[0]!='#', s1_processed.split()))
    l1 = list(S1.split(" ")) 

    S2 = " ".join(filter(lambda x:x[0]!='#', s2_processed.split()))
    l2 = list(S2.split(" ")) 

    l1_words = [word for word in l1 if word in model.keys()]
    l2_words = [word for word in l2 if word in model.keys()]

    vector_1 = np.mean([model[word] for word in l1_words],axis=0)
    
    vector_2 = np.mean([model[word] for word in l2_words],axis=0)
    
    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    cosine = float("{0:.4f}".format(cosine))

    #print('Word Embedding method with a cosine distance asses that our two sentences are similar to',cosine)
    return cosine

analyser = SentimentIntensityAnalyzer()
model = loadGloveModel(gloveFile)

with open('within-domain-model.pkl', 'rb') as fin:
    vect, classifier = pickle.load(fin)

new_data = pd.DataFrame(columns=['id', 'argument1', 'aid1', 'argument2', 'id2','aid2','stance','predicted_stance'])
count = 0
for index,row in data.iterrows():
    count = count + 1
    new_row = {}
    new_row['id'] = row['id']
    sentence1 = " ".join(row['argument1'].split())
    new_row['argument1'] = sentence1
    new_row['aid1'] = row['aid1']
    sentence2 = " ".join(row['argument2'].split())
    new_row['argument2'] = sentence2
    
    new_row['id2'] = row['id2']
    new_row['aid2'] = row['aid2']
    new_row['stance'] = row['stance']
                    
    argument1 = np.array([sentence1])
    argument2 = np.array([sentence2])

    X1_test = pd.Series(argument1)
    X2_test = pd.Series(argument2)
    sentiment_arr_test = np.array([])
    cosine_similarity_test = np.array([])


    for i,v in X1_test.iteritems():
        snt = analyser.polarity_scores(X1_test[i])
        comp = snt['compound']
        cosine_distance = cosine_distance_wordembedding_method(X1_test[i],X2_test[i])
        sentiment_arr_test = np.concatenate((sentiment_arr_test, [comp]))
        cosine_similarity_test = np.concatenate((cosine_similarity_test, [cosine_distance])) 


    sentiment_arr_test = sentiment_arr_test.reshape(sentiment_arr_test.shape[0],-1)
    sentiment_arr_test = sparse.csr_matrix(sparse.csr_matrix(sentiment_arr_test))

    cosine_similarity_test = cosine_similarity_test.reshape(cosine_similarity_test.shape[0],-1)
    cosine_similarity_test = sparse.csr_matrix(sparse.csr_matrix(cosine_similarity_test))

    X1_test_dtm = vect.transform(X1_test)
    X2_test_dtm = vect.transform(X2_test)

    X_test_dtm = scipy.sparse.hstack([X1_test_dtm,X2_test_dtm,sentiment_arr_test,cosine_similarity_test])
    X_test_dtm.data = np.nan_to_num(X_test_dtm.data)
    pred_single = classifier.predict(X_test_dtm)
    new_row['predicted_stance'] = pred_single[0]
    new_data.loc[len(new_data)] = new_row

new_data.to_csv(datapath+ 'testing-cross-domain-annotated.csv',sep='\t', encoding='utf-8', index=False)
