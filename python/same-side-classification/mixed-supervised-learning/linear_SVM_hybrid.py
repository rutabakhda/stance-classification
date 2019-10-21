import pandas as pd
import numpy as np
import nltk
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import scipy
from scipy import sparse
from sklearn.model_selection import train_test_split
import re
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import string
import pickle

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# import and instantiate CountVectorizer (with the default parameters)
# read file into pandas using a relative path
path = 'training-within-domain.csv'

data = pd.read_csv(path, error_bad_lines=False,sep=',', header=0,nrows=5000)

# Reading 2 arguments
X1 = data.argument1
X2 = data.argument2
y = data.stance

X1.index += 1
X2.index += 1

# Glove word embedding
gloveFile = "glove.6B\\glove.6B.50d.txt"
def loadGloveModel(gloveFile):
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    return model


# Preproecessing data
def preprocess(raw_text):    
    # keep only words
    text = re.sub(r'^https?:\/\/.*[\r\n]*', ' ', raw_text, flags=re.MULTILINE)
    letters_only_text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    
    # convert to lower case and split 
    words = letters_only_text.lower()
    return words

#Calculating cosine similarity between numeric vectors
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

    stopword = nltk.corpus.stopwords.words('english')

    l1 = [word for word in l1 if word not in stopword]
    l2 = [word for word in l2 if word not in stopword]

    wn = nltk.WordNetLemmatizer()

    l1 = [wn.lemmatize(word) for word in l1]
    l2 = [wn.lemmatize(word) for word in l2] 

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

sentiment_arr_train = np.array([])
sentiment_arr_train = np.array([])
cosine_similarity_train = np.array([])

sentiment_arr_test = np.array([])
cosine_similarity_test = np.array([])

#Splitting into train-test set
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y, test_size = 0.33,random_state=2)
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y, test_size = 0.33,random_state=2)

for i,v in X1_train.iteritems():
    snt = analyser.polarity_scores(X1_train[i])
    comp = snt['compound']
    cosine_distance = cosine_distance_wordembedding_method(X1_train[i],X2_train[i])
    sentiment_arr_train = np.concatenate((sentiment_arr_train, [comp]))
    cosine_similarity_train = np.concatenate((cosine_similarity_train, [cosine_distance])) 


for i,v in X1_test.iteritems():
    snt = analyser.polarity_scores(X1_test[i])
    comp = snt['compound']
    cosine_distance = cosine_distance_wordembedding_method(X1_test[i],X2_test[i])
    sentiment_arr_test = np.concatenate((sentiment_arr_test, [comp]))
    cosine_similarity_test = np.concatenate((cosine_similarity_test, [cosine_distance])) 

sentiment_arr_train = sentiment_arr_train.reshape(sentiment_arr_train.shape[0],-1)
sentiment_arr_train = sparse.csr_matrix(sparse.csr_matrix(sentiment_arr_train))

cosine_similarity_train = cosine_similarity_train.reshape(cosine_similarity_train.shape[0],-1)
cosine_similarity_train = sparse.csr_matrix(sparse.csr_matrix(cosine_similarity_train))

sentiment_arr_test = sentiment_arr_test.reshape(sentiment_arr_test.shape[0],-1)
sentiment_arr_test = sparse.csr_matrix(sparse.csr_matrix(sentiment_arr_test))

cosine_similarity_test = cosine_similarity_test.reshape(cosine_similarity_test.shape[0],-1)
cosine_similarity_test = sparse.csr_matrix(sparse.csr_matrix(cosine_similarity_test))

# instantiate the vectorizer
vect1 = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2))

vect1.fit(X1_train)
vect1.fit(X2_train)
X1_train_dtm = vect1.transform(X1_train)
X2_train_dtm = vect1.transform(X2_train)
X_train_dtm = scipy.sparse.hstack([X1_train_dtm,X2_train_dtm,sentiment_arr_train,cosine_similarity_train])
X_train_dtm.data = np.nan_to_num(X_train_dtm.data)

X1_test_dtm = vect1.transform(X1_test)
X2_test_dtm = vect1.transform(X2_test)
X_test_dtm = scipy.sparse.hstack([X1_test_dtm,X2_test_dtm,sentiment_arr_test,cosine_similarity_test])
X_test_dtm.data = np.nan_to_num(X_test_dtm.data)

# calculate accuracy of class predictions
from sklearn import svm
lin_clf = svm.LinearSVC()
lin_clf.fit(X_train_dtm, y1_train)
y_pred_class = lin_clf.predict(X_test_dtm)

from sklearn import metrics
# calculate accuracy of class predictions
from sklearn import metrics
print("accuracy score")
print(metrics.accuracy_score(y1_test, y_pred_class))
print("confusion matrix")
# print the confusion matrix
print(metrics.confusion_matrix(y1_test, y_pred_class))
print("classification report")
print(metrics.classification_report(y1_test, y_pred_class))

# save the model to disk
with open('cross-domain-model.pkl', 'wb') as fout:
  pickle.dump((vect1, lin_clf), fout)
print('Classifier trained')
