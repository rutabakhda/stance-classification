import nltk
from nltk import bigrams
from nltk import trigrams
from helper_argsme_train_test_similarity import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import Tree, word_tokenize, pos_tag, RegexpParser
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from wordcloud import WordCloud
import csv
import re
import pandas as pd
import numpy as np
import ast
from spacy.lang.en import English
import spacy
import itertools
import string
from wordcloud import WordCloud
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer

import collections
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re

stop_words = set(stopwords.words('english'))

def generate_grams_distribution(arguments, file_name, gram_type):
    """
    Generate gram distribution and
    save to file name
    return gram distribution
    """
    grams = []

    counter = 0
    for argument in arguments:
        tokens = nltk.word_tokenize(argument)
        if gram_type == "uni":
            grams += tokens
        elif gram_type == "bi":
            bi_tokens = [" ".join(bigram) for bigram in nltk.bigrams(tokens)]
            grams += bi_tokens
        elif gram_type == "tri":
            tri_tokens = [" ".join(trigram) for trigram in nltk.trigrams(tokens)]
            grams += tri_tokens
        counter += 1
    # print(file_name)
    gram_distribution = sorted([(grams.count(item), item) for item in sorted(set(grams))],reverse=True)
    write_list_to_file(file_name, gram_distribution)
    # wordcloud
    # convert list to dict
    dict_grams = {frequency_word[1] : frequency_word[0] for frequency_word in gram_distribution }
    name = " ".join(file_name.replace(".txt","").split("_"))
    draw_wordcloud(dict_grams, name)
    return gram_distribution

def clean_data_1(arguments):
    """
    Further clean argument by
    removing stopwords and stemming
    """
    arguments = remove_stopwords(arguments)
    arguments = stemming(arguments)
    return arguments

def clean_data_2(arguments):
    """
    Further clean argument by
    lemmatizing and removing stopwords
    """
    arguments = lemmatize(arguments)
    arguments = remove_stopwords(arguments)
    return arguments

def remove_stopwords(arguments):
    """
    Remove stopwords and
    return filtered arguments
    """
    new_arguments = []
    for sentence in arguments:
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        # filter out stopwords
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        filtered_sentence = " ".join(filtered_sentence)
        new_arguments.append(filtered_sentence)
    return new_arguments

def stemming(arguments):
    """
    Stemming words and
    return arguments
    """
    ps = PorterStemmer()
    new_arguments = []
    for sentence in arguments:
        word_tokens = word_tokenize(sentence)
        new_sentence = []
        for w in word_tokens:
            new_sentence.append(ps.stem(w))
        new_sentence = " ".join(new_sentence)
        new_arguments.append(new_sentence)
    return new_arguments

def lemmatize(arguments):
    """
    Lemmatize words and
    return arguments
    """
    lemmatizer = nltk.stem.WordNetLemmatizer().lemmatize
    new_arguments = []
    for sentence in arguments:
        word_tokens = word_tokenize(sentence)
        new_sentence = []
        for w in word_tokens:
            new_sentence.append(lemmatizer(w))
        new_sentence = " ".join(new_sentence)
        new_arguments.append(new_sentence)
    return new_arguments

def extract_chunks(text_string,max_words=3,lemmatize=True):
    """
    Extract phrase nouns by using regex
    """
    # Any number of adjectives followed by any number of nouns and (optionally) again
    # any number of adjectives folowerd by any number of nouns
    grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'

    # Makes chunks using grammar regex
    chunker = nltk.RegexpParser(grammar)

    # Get grammatical functions of words
    # What this is doing: tag(sentence -> words)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text_string))

    # Make chunks from the sentences, using grammar. Output in IOB.
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                        for tagged_sent in tagged_sents))
    # Join phrases based on IOB syntax.
    candidates = [' '.join(w[0] for w in group).lower() for key, group in itertools.groupby(all_chunks, lambda l: l[2] != 'O') if key]

    # Filter by maximum keyphrase length
    candidates = list(filter(lambda l: len(l.split()) <= 3, candidates))

    # Filter phrases consisting of punctuation or stopwords
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    candidates = list(filter(lambda l: l not in stop_words and not all(c in punct for c in l),candidates))

    # lemmatize
    if lemmatize:
        lemmatizer = nltk.stem.WordNetLemmatizer().lemmatize
        candidates =  [lemmatizer(x) for x in candidates]
    print(candidates)
    return candidates

def draw_wordcloud(dict_grams, name):
    """
    Draw wordcloud
    """
    # wordcloud
    wc = WordCloud(width = 1000, height = 500)
    # wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
    #                max_font_size=150, random_state=42)

    wc.generate_from_frequencies(frequencies=dict_grams)
    plt.figure()
    plt.title(name)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

def compare_sentece_length(for_arguments, against_arguments):
    """
    Compare sentence length
    and draw the distribution as histogram
    """
    tokenizer = RegexpTokenizer(r'\w+')
    for_sent_lenghs =[len(tokenizer.tokenize(sentence)) for sentence in for_arguments]
    against_sent_lenghs =[len(tokenizer.tokenize(sentence)) for sentence in against_arguments]
    for_sent_len = [i for i in for_sent_lenghs if i!=0]
    against_sent_len = [i for i in against_sent_lenghs if i!=0]
    plt.hist(for_sent_len, bins=range(min(for_sent_len), max(for_sent_len) + 1, 1),
                  alpha=0.4, color="blue", normed=True)
    plt.hist(against_sent_len, bins=range(min(against_sent_len), max(against_sent_len) + 1, 1),
                  alpha=0.4, color="red", normed=True)
    plt.axvline(x=np.average(for_sent_len+against_sent_len),color="cyan")
    labels = ["Average", 'For',"Against"]
    plt.legend(labels)
    plt.xlabel("length of sentence")
    plt.ylabel("proportion")
    plt.title("comparing sentence length distribution in for and against argument")
