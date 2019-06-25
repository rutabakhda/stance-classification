import pandas as pd
import os
from common import Common

class RemoveFields():
    def __init__(self, topic_name):
        super().__init__()

        self.common = Common()


        basepath = os.path.dirname(os.path.abspath(__file__))

        datapath_oq = basepath + "/result/{}/".format(topic_name)
        readfile_oq = '{}-original.csv'.format(topic_name)
        filename_oq = '{}.csv'.format(topic_name)
        newfile_oq = os.path.join(datapath_oq, filename_oq)

        self.remove_fields(readfile_oq,datapath_oq,newfile_oq)

    def remove_fields(self,readfile,datapath,newfile):
        data = pd.read_csv(filepath_or_buffer=datapath+readfile, usecols=[0,2,8,10,11,13])
        data.drop_duplicates(inplace=True, subset='speechtext', keep='first')
        if os.path.isfile(newfile):
            self.common.write_csv_without_header(newfile,data)

        else:
            self.common.write_csv_with_header(newfile, data)


if __name__ == '__main__':
    RemoveFields()