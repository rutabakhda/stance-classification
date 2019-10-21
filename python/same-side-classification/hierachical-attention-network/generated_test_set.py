import pandas as pd
import csv
import os
import shutil

class Processing():

    def __init__(self):
        super().__init__()
        if os.path.isdir('result'):
            shutil.rmtree('result')
        os.makedirs('result')

        self.list_path = []

        self.create_csv(input_file='result/new_test.csv')

        self.read_through(data_path='data/args_pairs')
        print(self.list_path[0])

        self.write_csv(csv_file='result/new_test.csv')

        print("Process Done !!!!!!!!!!!!!!!!")

    def create_csv(self, input_file):
        """
        :param input_file: path to a .csv file
        :return: nothing
        """
        output_path = input_file.replace("\\", "/")
        with open(output_path, mode="a", encoding="utf-8") as csvfile:
            field = ["argument1", "argument2", "is_same_side"]
            csv_file = csv.DictWriter(f=csvfile, fieldnames=field)
            csv_file.writeheader()
        csvfile.close()

    def read_through(self, data_path):
        """
        :param data_path:  path of corpus (lipad)
        :return: list of path of all .csv files
        """
        for root, directory, files in os.walk(data_path):
            for folder in directory:
                self.read_through(folder)
            for file in files:
                self.list_path.append(root + "/" + os.path.relpath(file))

    def write_csv(self, csv_file):
        with open(file=csv_file, mode='a', encoding="utf-8") as output_csv:
            output_writer = csv.writer(output_csv)
            for path in self.list_path:
                text_row = []
                data = pd.read_csv(filepath_or_buffer=path, header=0).values
                text_row.append(str(data[0][6]))
                text_row.append(str(data[1][6]))
                if "positive_pairs" in str(path):
                    text_row.append(str(1))
                else:
                    text_row.append(str(0))
                output_writer.writerow(text_row)
        output_csv.close()



if __name__ == '__main__':
    Processing()