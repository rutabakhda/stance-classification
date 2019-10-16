import os
import pandas as pd
import json
import numpy as np

"""
Generate agreement between annotators based on curation result.
Save the results as json file in current directory.
e.g:
[
  {
    "content": "the Prime Minister is absurdly wrapping himself and his party in the cloak of human rights on the marriage issue, suggesting that support for traditional marriage reflects hostility to basic rights, but Canadian political history tells a totally different story.",
    "topic": "Human Rights",
    "unitType": "premise"
  },
  {
    "content": "It was the Liberal Party that imposed the infamous head tax on Chinese immigrants; created a racist immigration system with the Exclusion Act; interred all Japanese Canadians; rejected Jewish refugees before and during the war; imposed martial law in 1970; permitted Ernst Zundel to run for its party leadership in 1968; eliminated constitutionally guaranteed rights for confessional education; and preached moral equivalence during the cold war and in China today.",
    "topic": "Human Rights",
    "unitType": "premise"
  },
  ...
]
__author__ = "Anh Phuong Le"
__date__ = "2019.08.04"
"""

# some intialization
argumentative_keys = ['conclusion','premise','non-argumentative'] # categories of sentence
results_path = sys.argv[1] # "curation_results" # current path os.getcwd() + "/"
files = []
df = pd.DataFrame(columns=['segment_key']+argumentative_keys+['content','topic'])
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
        speech_number = folder.split("-")[-1]
        folder_path = root+"/"+folder
        speechtxt_path = os.getcwd() + "/" + "annotation_tasks" + "/" + speech_number + "/" + "segment-labeling.txt"
        speechconf_path = os.getcwd() + "/" + "annotation_tasks" + "/" + speech_number + "/" + "segment-labeling.conf"
        speech_sentences = []

        with open(speechconf_path, 'rb') as f3:
            first_line = f3.readline().decode(errors='ignore')
            topic = first_line.split("=")[-1]

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
                                current_segment["content"] = content
                                current_segment["topic"] = topic
                            # update segment annotation result
                            current_segment[label] = current_segment[label]+1
                            speechs_annotation_result[segment_key] = current_segment # update

# convert to dataframe
i=0
for segment_key in speechs_annotation_result:
    segment_values = list(speechs_annotation_result[segment_key].values())
    df.loc[i] = [segment_key]+segment_values
    i = i+1

# df = df.reindex(columns = ['segment_key']+argumentative_keys+['non-conclusion']+['content'])
df['unitType'] = np.where(df['conclusion']==1, 'conclusion', 'premise')
df = df.drop(columns=['segment_key','conclusion','premise','non-argumentative'])
print(df.to_string())
df.to_json("sampled_sbm2.json", orient = "records")
