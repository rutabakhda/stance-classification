from statsmodels.stats.inter_rater import fleiss_kappa
import os
import pandas as pd
import json

"""
Calculate fleiss kappa score.
Print all sentences and its annotation details if high conflict
__author__ = "Anh Phuong Le"
__date__ = "2019.08.02"
"""

# some intialization
argumentative_keys = ['conclusion','premise','non-argumentative'] # categories of sentence
results_path = os.getcwd() + "/" + "annotation_results" # get current path
files = []
df = pd.DataFrame(columns=['segment_key']+argumentative_keys+['segment_content'])
speechs_annotation_result = {}
'''e.g
{
    "123456-1":{"conclusion":1,"premise":1,"non-argumentative":1}},
    "123456-2":{"conclusion":1,"premise":1,"non-argumentative":1}},
'''

# loop through all results
for root, directories, files in os.walk(results_path):
    for folder in directories:
        # check folder (should be speech nubmer)
        # print(folder)
        speech_number = folder
        folder_path = root+"/"+folder
        speechtxt_path = os.getcwd() + "/" + "annotation_tasks" + "/" + speech_number + "/" + "segment-labeling.txt"
        speech_sentences = []
        with open(speechtxt_path,'rb') as f1:
            for line in f1:
                speech_sentences.append(line.decode(errors='ignore'))
        for root2, directories2, files2 in os.walk(folder_path):
            for file_name in files2:
                if file_name.endswith(".txt"):
                    # check file (should be annotator name)
                    # print(file_name)
                    file_path = root2+"/"+file_name
                    with open(file_path) as f2:
                        next(f2) # ignore first line which is whole speech category: for or against given topic (pro vs cons)
                        for line in f2:
                            [segment, label] = line.split("=")
                            segment_number = int(segment.split(".")[-1])
                            segment_key = speech_number+"-"+str(segment_number) # "123456-1"
                            label=label.lstrip().strip("\n")
                            # create a dictionary e.g {"conclusion":0,"premise":0,"non-argumentative":0}} if the segment key not seen
                            if segment_key in speechs_annotation_result:
                                current_segment = speechs_annotation_result[segment_key]
                            else:
                                current_segment = dict.fromkeys(argumentative_keys,0) # create dictionary from keys with default value 0
                                content = ""
                                if(len(speech_sentences) > segment_number-1):
                                    content = speech_sentences[segment_number-1][:-2]
                                current_segment["segment_content"] = content
                            # update segment annotation result
                            current_segment[label] = current_segment[label]+1
                            speechs_annotation_result[segment_key] = current_segment # update

# convert to dataframe
i=0
for segment_key in speechs_annotation_result:
    segment_values = list(speechs_annotation_result[segment_key].values())
    df.loc[i] = [segment_key]+segment_values
    i = i+1
df['non-conclusion'] = df['premise'] + df['non-argumentative']
df = df.reindex(columns = ['segment_key']+argumentative_keys+['non-conclusion']+['segment_content'])
# calculate fleiss kappa with 3 keys ['conclusion','premise','non-argumentative']
# 0.21970641739986077
print(fleiss_kappa(df.drop(columns=['segment_key','non-conclusion','segment_content']).to_numpy(), method="fleiss"))

# calculate fleiss kappa with 2 keys ['conclusion','non-conclusion']
# 0.4032853876869647
print(fleiss_kappa(df.drop(columns=['segment_key','premise','non-argumentative','segment_content']).to_numpy(), method="fleiss"))

print(df.to_string())
# print the sentences
for index, row in df.iterrows():
    print("sentence: " + row.segment_content)
    if(row.conclusion > 0):
        print("===> " + str(row.conclusion) + " annotated conclusion")
