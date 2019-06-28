from common import Common

from glob import glob
import os



class CombineTopics():
    def __init__(self):
        super().__init__()

        self.common = Common()


        basepath = os.path.dirname(os.path.abspath(__file__))
        datapath = basepath + "/lipad1/"
        self.EXT = '*.csv'

        category_oq = 'oral-questions'
        category_sbm = 'statement-by-members'
        filename_oq =  category_oq + '-original.csv'
        new_dir_oq = datapath + './' + category_oq  # Creating new directory for given category
        newfile_oq = os.path.join(new_dir_oq, filename_oq)

        filename_sbm = category_sbm + '-original.csv'
        new_dir_sbm = datapath + './' + category_sbm  # Creating new directory for given category
        newfile_sbm = os.path.join(new_dir_sbm, filename_sbm)

        #TASK 1 : Find Oral questions and Statement by members data
        self.find_categories(datapath,category_oq,new_dir_oq,newfile_oq)  # finding oral questions data
        self.find_categories(datapath, category_sbm,new_dir_sbm,newfile_sbm)  # finding oral questions data


    def find_categories(self,datapath,category,new_dir,newfile):
        dirs = next(os.walk(datapath))[1] # lists all directories inside given path

        for dir in dirs:                 # looping through all levels inside each directory found in previous step
            files = self.loop_through(datapath, dir)  # Finding csv files inside each dir

            for file in files:  #Reading data from each csv file
                data = self.common.read_csv('',file)
                elderly = data.maintopic.notnull()
                data1 = data[elderly]

                if category == 'oral-questions':
                    american = data1['maintopic'] == "Oral Questions"
                elif category == 'statement-by-members':
                    american = data1['maintopic'] == "Statements By Members"
                else:
                    pass
                cat_data = data1[american]


                # self.common.make_dir(new_dir)

                if (not cat_data.empty):
                    if os.path.isfile(newfile):
                        self.common.write_csv_without_header(newfile,cat_data)

                    else:
                        self.common.write_csv_with_header(newfile,cat_data)


    def loop_through(self,datapath,dir):
             for path, subdir, files in (os.walk(datapath + dir)):
                for filename in glob(os.path.join(path, self.EXT)):
                    files = []
                    files.append(filename)
             return files

if __name__ == '__main__':
    CombineTopics()

