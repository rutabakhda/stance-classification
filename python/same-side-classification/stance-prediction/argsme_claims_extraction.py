from helper_argsme_claims_extraction import *

"""
Step 1: claims extraction
Get all arguments from a topic e.g abortion
with a given list of specific (more detail) topics regarding the target topic
and these topics take a stance (or not) regarding the target topic
"""

if __name__=="__main__":
    # to load everything from dataset
    df = read_json(sys.argv[1]) # path to args-me.json

    # load all discussion topics from file
    all_discussion_topics = read_csv_dictionary("../data/argsme_all_topics_abortion/argsme_all_topics_abortion_ranked.csv")

    '''
    # loop through all dataset
    # if the topic is in topics list, get the stance of the argument
    # summarize the argument to several sentences
    # add the summary to a list of all claims
    # write the list to csv file
    '''
    specific_topic = "abortion"
    all_claims_for = {} # index (of topic): [list of all summary]
    all_claims_against = {}
    for index, row in df.iterrows():
        text_id = row['arguments']['id']
        stance = row['arguments']['premises'][0]['stance']
        text = row['arguments']['premises'][0]['text']
        topic = row['arguments']['conclusion']
        dict_data = {
            "stance" : stance,
            "topic" : topic,
            "text" : text
        }

        # if the topic is in topics list, get the stance of the argument
        if topic in all_discussion_topics:
            is_pro = all_discussion_topics[topic]
            if is_pro == '-':
                continue
            else:
                # summarize the argument to several sentences
                summary = summarize_argument(text)
                # get index of topic
                ind = list(all_discussion_topics).index(topic)
                # get stance of arguments and
                # add summary to list
                if (is_pro == 'y' and stance == 'PRO') or (is_pro == 'n' and stance == 'CON'):
                    stance = "for"
                    if ind not in all_claims_for.keys():
                        all_claims_for[ind] = []
                    all_claims_for[ind].append(summary)
                elif (is_pro == 'n' and stance == 'PRO') or (is_pro == 'y' and stance == 'CON'):
                    stance = "against"
                    if ind not in all_claims_against.keys():
                        all_claims_against[ind] = []
                    all_claims_against[ind].append(summary)
            print("-", end = "")
            # print(summary)
    print("")
    # end for

    # write claims to csv file
    write_claims_to_csv(all_claims_for, all_claims_against, "../data/argsme_all_claims_abortion/argsme_all_claims_abortion.csv")
