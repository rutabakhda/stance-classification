from helper_argsme_train_test_similarity import *
from helper_argsme_exploratory_data_analysis import *

"""
Step 2: Data exploratory analysis
Different methods to explore the argsme abortion claims
by n-grams frequency
by n-grams tfidf
by phrasing
"""

def n_grams_frequency(for_arguments, against_arguments):
    """
    Generate N (1,2,3) grams frequency distribution and
    return draw wordcloud
    """
    print("n_grams_frequency")
    # maybe further clean the dataset
    for_arguments = clean_data_1(for_arguments)
    against_arguments = clean_data_1(against_arguments)
    # generate gram distribution, draw wordcloud and save to file
    for my_tuple in [(for_arguments,"for"),(against_arguments,"against")]:
        arguments = my_tuple[0]
        stance = my_tuple[1]
        file1 = stance + "_" + "unigrams.txt"
        file2 = stance + "_" + "bigrams.txt"
        file3 = stance + "_" + "trigrams.txt"
        unigram_distribution = generate_grams_distribution(arguments, file1, "uni")
        bigram_distribution = generate_grams_distribution(arguments, file2, "bi")
        trigram_distribution = generate_grams_distribution(arguments, file3, "tri")

def tfidf_distribution(for_arguments, against_arguments):
    """
    Generate tfidf word distribution and
    draw wordcloud
    """
    print("tfidf_distribution")
    for_arguments = clean_data_2(for_arguments)
    against_arguments = clean_data_2(against_arguments)
    for my_tuple in [(for_arguments,"for"),(against_arguments,"against")]:
        sentences = my_tuple[0]
        stance = my_tuple[1]
        cvec = CountVectorizer(stop_words='english', min_df=3, max_df=0.5, ngram_range=(1,2))
        sf = cvec.fit_transform(sentences)
        transformer = TfidfTransformer()
        transformed_weights = transformer.fit_transform(sf)
        weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
        weights_df = pd.DataFrame({'term': cvec.get_feature_names(), 'weight': weights})
        # get list of 100 top words by tfidf
        list_words = list(weights_df.sort_values(by='weight', ascending=False).head(100)["term"].values)
        if stance == "for":
            for_set_words = set(list_words)
            for_df = weights_df.sort_values(by='weight', ascending=False).head(100)
        elif stance == "against":
            against_set_words = set(list_words)
            against_df = weights_df.sort_values(by='weight', ascending=False).head(100)

    # check distint and common words from the list
    for_distinct_words = for_set_words.difference(against_set_words)
    against_distinct_words = against_set_words.difference(for_set_words)
    common_words = for_set_words.intersection(against_set_words)

    # write list to file
    write_list_to_file("for_distinct_words.txt",list(for_distinct_words))
    write_list_to_file("against_distinct_words.txt",list(against_distinct_words))
    write_list_to_file("abortion_common_words.txt",list(against_distinct_words))

    # draw wordcloud of each distinct list
    for_df_filter = for_df[for_df['term'].isin(list(for_distinct_words))]
    for_distinct_tfidf = dict(zip(for_df_filter.term, for_df_filter.weight))
    name = "for" + "_distinct_tokens"
    draw_wordcloud(for_distinct_tfidf, name)

    against_df_filter = against_df[against_df['term'].isin(list(against_distinct_words))]
    against_distinct_tfidf = dict(zip(against_df_filter.term, against_df_filter.weight))
    name = "against" + " distinct tokens"
    draw_wordcloud(against_distinct_tfidf, name)

    # sum up tfidf value for common words and draw wordcloud
    for_df_filter = for_df[for_df['term'].isin(list(common_words))]
    for_common_tfidf = dict(zip(for_df_filter.term, for_df_filter.weight))
    against_df_filter = against_df[against_df['term'].isin(list(common_words))]
    against_common_tfidf = dict(zip(against_df_filter.term, against_df_filter.weight))
    name = "common" + " tokens"
    draw_wordcloud(dict(Counter(for_common_tfidf)+Counter(against_common_tfidf)), "common")

def phrase_distribution(for_arguments, against_arguments):
    """
    Extract phrases based on regex and
    draw wordcloud
    """
    for_arguments = clean_data_2(for_arguments)
    against_arguments = clean_data_2(against_arguments)
    for my_tuple in [(for_arguments,"for"),(against_arguments,"against")]:
        string_array = []
        arguments = my_tuple[0]
        stance = my_tuple[1]
        for sentence in arguments:
            string_array += extract_chunks(sentence)
            # break
        # word count dict
        word_could_dict=Counter(string_array)
        # dict to list
        frequencies = OrderedDict(sorted(word_could_dict.items(), key=lambda t: t[1], reverse=True))
        # Converting into list of tuple
        frequencies = [(k, v) for k, v in frequencies.items()]
        write_list_to_file(stance+"_phrases.txt", frequencies)
        name = stance + " phrases"
        draw_wordcloud(word_could_dict, name)

if __name__=="__main__":
    # load arguments from dataset
    df = read_csv("../data/argsme_all_claims_abortion/argsme_all_claims_abortion.csv")
    (for_arguments, against_arguments) = get_for_against_claims(df)
    n_grams_frequency(for_arguments, against_arguments)
    tfidf_distribution(for_arguments, against_arguments)
    phrase_distribution(for_arguments, against_arguments)
    compare_sentece_length(for_arguments, against_arguments)
    plt.show()
