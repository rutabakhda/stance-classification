import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import csv
import re
import pandas as pd
import math
import string
import contractions

def read_csv_dictionary(file_name):
    """
    Read a csv file with 2 columns and
    return a dictionary
    """
    with open(file_name) as f:
        # get data from file
        df = pd.read_csv(f, sep='\t', header=None)
    all_discussion_topics = dict(zip(df[0], df[1]))
    return all_discussion_topics

def read_json(file_name):
    """
    Read a json file and
    return a dataframe
    """
    with open(file_name) as f:
        df = pd.read_json(f)
    return df

def clean_text(argument):
    """
    Clean a sentence and
    return a cleaned sentence
    """
    # decontract
    argument = decontracted(argument)
    argument = re.sub(r"\'s", "s", argument)
    # remove content in double quote
    argument = re.sub('".*?"', '', argument)
    # remove content in brackets
    argument = re.sub('\[.*?\]', '', argument)
    # remove special character except space with regex
    argument = re.sub(r"[^a-zA-Z0-9]+", ' ', argument)
    # remove words containing numbers
    argument = re.sub('[%s]' % re.escape(string.punctuation), '', argument)
    argument = re.sub('\w*\d\w*', '', argument)
    # remove this cliches
    argument = argument.replace("vote con", "")
    argument = argument.replace("vote pro", "")
    # if the sentence is too short => remove
    if len(argument.split(" ")) < 4:
        return ""
    return argument

def split_into_sentences(text):
    """
    Split a text into sentences
    return an array
    """
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    text = " " + text + "  "
    # make lowercase
    text = text.lower()
    # remove hyperlinks
    text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '', text)
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text:
        text = text.replace(".”","”.")
    if "\"" in text:
        text = text.replace(".\"","\".")
    if "!" in text:
        text = text.replace("!\"","\"!")
    if "?" in text:
        text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    clean_sentences = []
    # clean sentences
    for sentence in sentences:
        clean_sentences.append(clean_text(sentence))
    return clean_sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    """
    Compare 2 sentences and
    return the similarity between them
    """
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

def decontracted(phrase):
    return contractions.fix(phrase)

def summarize_argument(text):
    """
    Summarize a paragraph
    to an array of sentences
    """
    stop_words = stopwords.words('english')
    summarize_text = []
    # Step 1 - Read text and split it (and clean in the way)
    sentences = split_into_sentences(text)
    # remove empty string
    sentences = list(filter(None, sentences))
    if(len(sentences) >= 2):
        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
        # print("Indexes of top ranked_sentence order are ", ranked_sentence)

        top_n = math.ceil(len(sentences)/5)
        # method 1: summarize to 5 sentences if the arguemnts is too long
        # method 2: shorten by dividing by 5, make sure odd number
        if top_n % 2 == 0:
            top_n += 1
        # print(ranked_sentence)
        for i in range(top_n):
          summarize_text.append("".join(ranked_sentence[i][1]))

        # Step 5 - Output the summarize text
        # print("Summarize Text: \n", summarize_text)
        return summarize_text

    else:
        return sentences

def write_claims_to_csv(for_arguments, against_arguments, file_name):
    """
    Write all claims to a csv file
    """
    with open(file_name, 'w') as f:
        f.write('{0}\t{1}\t{2}\n'.format("topic_index", "for_arguments", "against_arguments"))
        all_indexes = list(for_arguments.keys()) + list(against_arguments.keys())
        for i in sorted(set(all_indexes)):
            if i in list(for_arguments.keys()):
                arguments = for_arguments[i]
                for sentences in arguments:
                    # print(for_argument)
                    f.write('{0}\t{1}\t{2}\n'.format(i, sentences, ""))
            if i in list(against_arguments.keys()):
                arguments = against_arguments[i]
                for sentences in arguments:
                    # print(against_argument)
                    f.write('{0}\t{1}\t{2}\n'.format(i, "", sentences))
