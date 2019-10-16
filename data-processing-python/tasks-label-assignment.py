import pandas as pd
from common import Common
import os

common = Common()
basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath + "/lipad1/data/statement-by-members/"  # Datapath for Statement by Members
readfile = 'controversial-statement-by-members.csv'

basepath_tasks = 'G:/example-project/'
datapath_tasks = basepath_tasks + "tasks/"

tasks = next(os.walk(datapath_tasks))[1]


#rows = data[(data["basepk"] == 4109255)]
#print(rows['subtopic'])

for task in tasks:
    
    subtopic = ""
    data = pd.read_csv(datapath + readfile, delimiter=',', header=0)
    data = data[(data["basepk"] == int(task))].head(1)
    for index, row in data.iterrows():
        print(task)
        subtopic = row['subtopic']
        print(subtopic)
    speech_dir = datapath_tasks + str(task) + "/"

    txtfile = common.write_to_text(speech_dir, 'segment-labeling.conf')
    txtfile.write("title = "+str(subtopic))
    txtfile.close()

    
