import os
from common import Common

class ControversialTopics():

    basepath = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, topic_name):
        super().__init__()

        basepath = os.path.dirname(os.path.abspath(__file__))
        datapath = basepath + "/result/{}/".format(topic_name)  # Datapath for Oral Questions

        readfile = '{}-removed-cliche.csv'.format(topic_name)

        filename = 'raw-controversial-{}.csv'.format(topic_name)
        removed_duplicated_file = 'controversial-{}.csv'.format(topic_name)
        newfile = os.path.join(datapath, filename)
        finalfile = os.path.join(datapath, removed_duplicated_file)

        self.common = Common()

        self.find_controversial_topics_with_sentiment(datapath,readfile,newfile)

        self.common.remove_duplicated_words(source_file=newfile, new_file=finalfile)

    def find_controversial_topics_with_sentiment(self,datapath,readfile,newfile):
        data = self.common.read_csv(datapath, readfile)
        data['lower_speechtext'] = data['speechtext_without_cliche'].str.lower()

        name = "wikipedia-controversial-issues.txt"
        with open(name, 'r', encoding='utf8') as f:
            for line in f:
                # for word in line.split():
                line = line.lower()
                line = line.strip()
                filtered_new_data = data[data['lower_speechtext'].str.count(line) > 1]
                filtered_new_data = filtered_new_data.drop(['lower_speechtext'], axis=1)

                if os.path.isfile(newfile):
                    self.common.write_csv_without_header(newfile, filtered_new_data)

                else:
                    self.common.write_csv_with_header(newfile, filtered_new_data)

if __name__ == '__main__':
    ControversialTopics()