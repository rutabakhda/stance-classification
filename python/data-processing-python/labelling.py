from datetime import datetime
from dateutil import parser
import os
import shutil
import re
import csv
import pandas as pd


class Labelling():
    def __init__(self, topic_name):
        super().__init__()

        basepath = os.path.dirname(os.path.abspath(__file__))
        datapath = basepath + "/result/{}/".format(topic_name)  # Datapath for Oral Questions

        readfile = 'controversial-{}.csv'.format(topic_name)

        filename = 'labelled-{}.csv'.format(topic_name)
        newfile = os.path.join(datapath, filename)

        self.list_party = ['liberal', 'progressive conservative', 'conservative (1867-1942)', 'new democratic party',
                           'conservative', 'co-operative commonwealth federation (c.c.f.)', 'bloc québécois',
                           'social credit', 'unionist', 'national government', 'reform', 'laurier liberal',
                           'independent', 'progressive', 'canadian alliance', 'ralliement créditiste',
                           'liberal-conservative', 'united farmers of alberta', 'labour', 'no affiliation',
                           'liberal labour', 'unionist (liberal)', 'independent conservative', 'liberal progressive',
                           'independent liberal', 'green', 'ndp', 'independent progressive', 'green party',
                           'independent progressive conservative', 'independent labour', 'nationalist liberal',
                           'reconstruction', 'independent c.c.f.', 'bloc populaire canadien',
                           'united farmers of ontario-labour', 'united farmers', 'unity', 'new party', 'bloc',
                           'labour progressive', 'new democracy', 'united farmers of ontario', 'gpq (ex-bloc)',
                           'forces et démocratie', 'québec debout', 'nationalist']

        self.create_csv(input_file=newfile)
        self.party_duration = pd.read_csv(filepath_or_buffer='data/PartyData.csv', header=0, delimiter=';').values
        self.add_role_process(input_file=os.path.join(datapath, readfile), output_file=newfile)

    def add_role_process(self, input_file, output_file):
        """
        :param input_file: path to old .csv file
        :param output_file: path to new .csv file
        :return: nothing
        """
        goverment_count = 0
        opposite_count = 0
        unknown_count = 0
        input_csv = pd.read_csv(filepath_or_buffer=input_file, header=0, usecols=[0,1,2,4,5,6]).values
        with open(file=output_file, mode='a', encoding="utf-8") as output_csv:
            output_writer = csv.writer(output_csv)
            # speech_time = parser.parse(input_csv[0, 2])
            # print(speech_time)
            for speech_record in input_csv:
                speech_time = parser.parse(speech_record[1])
                for row in self.party_duration:
                    if (speech_time > parser.parse(str(row[0]))) and (speech_time < parser.parse(str(row[1]))):
                        if str(speech_record[3]).lower() in str(row[2]).lower():
                            goverment_count += 1
                            text = ["Government"]
                        else:
                            if str(speech_record[3]).lower() in self.list_party:
                                opposite_count += 1
                                text = ["Opposition"]
                            else:
                                unknown_count +=1
                                text = ["Unknown"]
                        text.extend(['{}'.format(str(column)) for column in speech_record])
                        output_writer.writerow(text)
                        break
            output_csv.close()
        # return [goverment_count, opposite_count, unknown_count]


    def create_csv(self, input_file):
        """
        :param input_file: path to a .csv file
        :return: nothing
        """
        output_path = input_file.replace("\\", "/")
        with open(output_path, mode="a", encoding="utf-8") as csvfile:
            field = ["Role", "basepk", "speechdate",
                     "subtopic", "speakerparty", "speakername", "speechtext"]
            csv_file = csv.DictWriter(f=csvfile, fieldnames=field)
            csv_file.writeheader()
        csvfile.close()


if __name__ == '__main__':
    Labelling()
