import pandas as pd
import csv
import os
import shutil


class Preprocessing():
    def __init__(self, data_path_1, data_path_2, type_1, type_2):
        super().__init__()
        if os.path.isdir('result'):
            shutil.rmtree('result')
        os.makedirs('result')
        self.process(type=type_1, data_path=data_path_1)
        self.process(type=type_2, data_path=data_path_2)
        # self.process(type='statements_by_members', data_path='data/statements_by_members.csv')
        # self.create_dataset(output="new_dataset.csv")

    def process(self, type='OQ', data_path='data/oral_questions.csv'):
        input_data = pd.read_csv(filepath_or_buffer=data_path, header=0).values

        # Remove clichés such as "mr.speaker" at the beginning of the speeches ....
        self.remove_cliches(output="{}_remove_cliches.csv".format(str(type)), input_data=input_data)
        input_data = pd.read_csv(filepath_or_buffer='result/{}_remove_cliches.csv'.format(str(type)), header=0).values

        # Report the ten most occurring subtopics in the ....
        sub_topic = self.sub_topic(data=input_data)
        self.record_words(path='result/{}_sorted_subtopic.txt'.format(str(type)), list_words=sub_topic)
        # print("10 most sub topic: {}".format(sub_topic))

        #  Filter the speeches to those that target a controversial topic
        filter_data = open(file='data/controversial_issues.txt', mode='r', encoding="utf-8")
        controversial_topic_list = filter_data.readlines()

        if type == 'OQ':
            self.filter_controversial_topic_mode_1(output='OQ_filter_type_1.csv',
                                                   controversial_topic_list=controversial_topic_list,
                                                   input_data=input_data)
            self.filter_controversial_topic_mode_2(output='OQ_filter_type_2.csv', input_data=input_data)
        else:
            self.filter_controversial_topic_mode_1(output='SBM_filter_type_1.csv',
                                                   controversial_topic_list=controversial_topic_list,
                                                   input_data=input_data)
            self.filter_controversial_topic_mode_2(output='SBM_filter_type_2.csv', input_data=input_data)

        self.create_dataset(output_train="{}_new_db_train.csv".format(str(type)),
                            output_test="{}_new_db_test.csv".format(str(type)), input_data=input_data,
                            controversial_topic_list=controversial_topic_list)

        # Report the most occurring controversial topics ....
        input_text = pd.read_csv(filepath_or_buffer='result/{}_filter_type_1.csv'.format(str(type)), header=0).values
        list_subtopic = self.most_frequent_subtopic(input_data=input_text, num_topic=10, type=type)

    def remove_cliches(self, output, input_data):
        with open(file='result/{}'.format(output), mode='a', encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            field = ["basepk", "hid", "speechdate", "pid", "opid", "speakeroldname", "speakerposition", "maintopic",
                     "subtopic", "subsubtopic", "speechtext", "speakerparty", "speakerriding", "speakername",
                     "speakerurl"]
            output_csv = csv.DictWriter(f=output_file, fieldnames=field)
            output_csv.writeheader()

            for data in input_data:
                text = str(data[10]).lower()
                if "mr. speaker, " in text[:20]:
                    new_text = text.replace("mr. speaker, ", "")
                    data[10] = new_text
                if "mr. speaker" in text[-20:]:
                    new_text = text.replace("mr. speaker", "")
                    data[10] = new_text
                writer = csv.writer(output_file)
                writer.writerow(data)

    def sub_topic(self, data):
        subtopic_list = {}
        for row in data:
            if str(row[8]).lower() not in subtopic_list.keys():
                subtopic_list[str(row[8]).lower()] = 1
            else:
                subtopic_list[str(row[8]).lower()] += 1

        return subtopic_list

    def record_words(self, path, list_words):
        with open(path, mode="a", encoding="utf-8") as csv_file:
            for w in sorted(list_words, key=list_words.get, reverse=True):
                row = "{}, {}".format(w, list_words[w])
                csv_file.write(row + "\n")
        csv_file.close()

    def filter_controversial_topic_mode_1(self, output, controversial_topic_list, input_data):
        with open(file='result/{}'.format(output), mode='a', encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            field = ["basepk", "hid", "speechdate", "pid", "opid", "speakeroldname", "speakerposition", "maintopic",
                     "subtopic", "subsubtopic", "speechtext", "speakerparty", "speakerriding", "speakername",
                     "speakerurl"]
            output_csv = csv.DictWriter(f=output_file, fieldnames=field)
            output_csv.writeheader()

            for row in input_data:
                for topic in controversial_topic_list:
                    if str(row[8]).lower() in str(topic).lower():
                        writer = csv.writer(output_file)
                        writer.writerow(row)
                        break

    def filter_controversial_topic_mode_2(self, output, input_data):
        with open(file='result/{}'.format(output), mode='a', encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            field = ["basepk", "hid", "speechdate", "pid", "opid", "speakeroldname", "speakerposition", "maintopic",
                     "subtopic", "subsubtopic", "speechtext", "speakerparty", "speakerriding", "speakername",
                     "speakerurl"]
            output_csv = csv.DictWriter(f=output_file, fieldnames=field)
            output_csv.writeheader()

            for row in input_data:
                subtopic = str(row[8])
                speechtext = str(row[10])
                if speechtext.count(subtopic) >= 2:
                    writer = csv.writer(output_file)
                    writer.writerow(row)

    def create_dataset(self, output_train, output_test, input_data, controversial_topic_list):
        ci_count = 0
        non_ci_count = 0
        # count = 0
        with open(file='result/{}'.format(output_train), mode='a', encoding="utf-8") as output_train_file, open(
                file='result/{}'.format(output_test), mode='a', encoding="utf-8") as output_test_file:
            writer_1 = csv.writer(output_train_file)
            writer_2 = csv.writer(output_test_file)
            field = ["label", "basepk", "hid", "speechdate", "pid", "opid", "speakeroldname", "speakerposition",
                     "maintopic",
                     "subtopic", "subsubtopic", "speechtext", "speakerparty", "speakerriding", "speakername",
                     "speakerurl"]
            output_csv_1 = csv.DictWriter(f=output_train_file, fieldnames=field)
            output_csv_1.writeheader()
            output_csv_2 = csv.DictWriter(f=output_test_file, fieldnames=field)
            output_csv_2.writeheader()

            for row in input_data:
                # count += 1
                for topic in controversial_topic_list:
                    is_ci_topic = False
                    if str(row[8]).lower() in str(topic).lower():
                        is_ci_topic = True
                        writer_1 = csv.writer(output_train_file)
                        writer_2 = csv.writer(output_test_file)
                        ci_count += 1
                        if ci_count <= 900:
                            # text = ['{}'.format(count), '{}'.format(1), '{}'.format(str(row[10]))]
                            # text = ['{}'.format(1), '{}'.format(str(row))]
                            text = ['{}'.format(1)]
                            text.extend(['{}'.format(str(column)) for column in row])
                            writer_1.writerow(text)
                        if (ci_count > 900) and (ci_count <= 1000):
                            text = ['{}'.format(1)]
                            text.extend(['{}'.format(str(column)) for column in row])
                            writer_2.writerow(text)
                        break

                if is_ci_topic == False:
                    non_ci_count += 1
                    if non_ci_count <= 900:
                        # text = ['{}'.format(count), '{}'.format(0), '{}'.format(str(row[10]))]
                        # text = ['{}'.format(0), '{}'.format(str(row[10]))]
                        text = ['{}'.format(0)]
                        text.extend(['{}'.format(str(column)) for column in row])
                        writer_1.writerow(text)
                    if(non_ci_count > 900) and (non_ci_count <= 1000):
                        text = ['{}'.format(0)]
                        text.extend(['{}'.format(str(column)) for column in row])
                        writer_2.writerow(text)

    def most_frequent_subtopic(self, input_data, type='OQ', num_topic=10):
        sub_topic_list = {}
        for row in input_data:
            if str(row[8]).lower() not in sub_topic_list:
                sub_topic_list[str(row[8]).lower()] = 1
            else:
                sub_topic_list[str(row[8]).lower()] += 1

        self.record_words(path="result/{}_controversy_sorted_subtopic.csv".format(str(type)), list_words=sub_topic_list)
        list_topic = sorted(sub_topic_list, key=sub_topic_list.get, reverse=True)[0:num_topic]
        return list_topic


if __name__ == '__main__':
    Preprocessing(data_path_1='data/oral_questions.csv', type_1='OQ', data_path_2='data/statements_by_members.csv',
                  type_2='SBM')
