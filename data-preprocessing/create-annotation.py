import os
import math
import random

basepath = 'G:/project/example-project/'
datapath = basepath + "tasks/"

tasks = next(os.walk(datapath))[1]
total_task = len(tasks)

annotators = []
done_annotators = []
f = open(basepath+"annotators.txt", "r").read().split('\n')

for x in f:
    annotators.append(x)

total_annotators = len(annotators)
task_per_annotator = math.ceil((total_task*3)/total_annotators)

dict = {}
unassigned_tasks = []

for task in tasks:

    for i in range(3):

        isTaskAssigned = False
        count = 0
        while(not isTaskAssigned):
            annotator = random.choice(annotators)

            if annotator in dict:

                if len(dict[annotator]) < (task_per_annotator):

                    if (task in dict[annotator]):
                        count = count + 1
                        if count > 4:
                            unassigned_tasks.append(task)
                            isTaskAssigned = True
                        pass
                    else:

                        dict[annotator].append(task)
                        isTaskAssigned = True
                        i = i + 1

                else:

                    annotators.remove(annotator)
                    done_annotators.append(annotator)


            else:
                if annotator not in done_annotators:
                    tasks_list = []
                    tasks_list.append(task)
                    dict[annotator] = tasks_list
                    isTaskAssigned = True
                    i = i + 1

print(done_annotators)
print(unassigned_tasks)
if len(unassigned_tasks)!= 0:
    for task in unassigned_tasks:
        assigned = False
        while(not assigned):
            annotator1 = random.choice(done_annotators)
            annotator2 = random.choice(annotators)

            temp_task = dict[annotator1][0]

            if temp_task not in dict[annotator2] and task not in dict[annotator1]:
                dict[annotator1].remove(temp_task)
                dict[annotator2].append(temp_task)
                dict[annotator1].append(task)
                assigned = True
                unassigned_tasks.remove(task)
print(unassigned_tasks)





text_file = open("Output.txt", "w")
for key, value in dict.items():
    #print(key)
    #print(value)
    assigned_tasks = ' '.join(value)
    text_file.write("annotator."+key+".name = "+key+"\n")
    text_file.write("annotator."+key+".password = visitthedome\n")
    text_file.write("annotator."+key+".tasks = "+assigned_tasks+"\n")
    text_file.write("\n")
