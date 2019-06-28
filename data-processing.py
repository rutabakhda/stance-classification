import pandas as pd
from glob import glob
import os
from os import path

basepath = path.dirname(__file__)
datapath = basepath+"/lipad/2018/1/"
EXT = '*.csv'

for path,subdir,files in os.walk(datapath):
    for filename in glob(os.path.join(path,EXT)):
        print("file name is " + filename)

        data = pd.read_csv(filename)
        data_oral_questions = data.maintopic == 'Oral Questions'
        print(data[data_oral_questions])
