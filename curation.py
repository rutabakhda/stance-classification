import os
import shutil

basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath+ "/example-project"
task_path = datapath + "/tasks/"
task_states_path = datapath + "/task-states/"

dirs = next(os.walk(task_path))[1] # lists all directories inside given path
text = ""
for dir in dirs:                 # looping through all levels inside each directory found in previous step
    print(dir)
    new_curation_task = task_path+"curation-"+dir
    text = text+" "+"curation-"+dir
    os.mkdir(new_curation_task)
    task = task_path + dir
    files_path = os.listdir(task)
    for file in files_path:
        shutil.copy2(task+"/"+file, new_curation_task+"/"+file)

    task_state_path = task_states_path + dir
   
    files_task_states = os.listdir(task_state_path)
    print(files_task_states)
    for result_file in files_task_states:
        shutil.copy2(task_state_path+"/"+result_file, new_curation_task+"/"+result_file)

print()
with open(datapath+"/wat.conf", "a") as myfile:
    myfile.write(text)


        
        
    
