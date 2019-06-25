from combine_topics import CombineTopics
from remove_fields import RemoveFields
from remove_cliche import RemoveCliche
from find_controversial_topics import ControversialTopics
from labelling import Labelling
from common import Common
import os
from collect_data import Collect_data
from speechtext_to_sentences import Split_Speechtext
import shutil


class Main():
    def __init__(self) -> None:
        super().__init__()
        if os.path.isdir('result'):
            shutil.rmtree('result')
        os.makedirs('result')

        self.common = Common()
        list_path = self.common.read_through(data_path='lipad')
        debate_list = self.common.debate_list()

        oq_topic = ['oral questions', 'oral question period', 'questions', 'questions.']
        sbm_topic = ['statements by members']

        # List of debate topic
        emergency_debate_topic = ['emergency debate']
        commons_debates_after_recess = ['commons debates after recess', 'comomns debates']
        continuation_of_debate = ['continuation of debate on address in reply',
                                  'continuation of debate on motion for reference to public accounts committee',
                                  'continuation of debate on the annual financial statement of the acting minister of finance.']
        supply_proc_topic = ['supply-proc edure resuming on thursday or friday debate on amendment']
        subject_matter = ['subject matter of questions to be debated']
        supply_official = ['supply-official reporting of debates.']
        statement_in_debate = ['statement in debate on defence estimates respecting royal military college']
        address_debate = ['address debate']
        canada_united = [
            'canada-united states-continuation of debate on motion for approval subject to required legislation']
        house_of_commons_debates = ['house of commons debates', 'debates of the house.']

        # self.generate_csv_output_files(topic_name='oral-question', topic_title=oq_topic, list_path=list_path)
        # self.generate_csv_output_files(topic_name='statement-by-members', topic_title=sbm_topic, list_path=list_path)

        self.generate_csv_output_files(topic_name='emergency-debate', topic_title=emergency_debate_topic,
                                       list_path=list_path)
        # self.generate_csv_output_files(topic_name='commons-debates-after-recess',
        #                                topic_title=commons_debates_after_recess, list_path=list_path)
        # self.generate_csv_output_files(topic_name='continuation-of-debate', topic_title=continuation_of_debate,
        #                                list_path=list_path)
        # self.generate_csv_output_files(topic_name='supply-proc', topic_title=supply_proc_topic,
        #                                list_path=list_path)
        # self.generate_csv_output_files(topic_name='subject-matter', topic_title=subject_matter, list_path=list_path)
        # self.generate_csv_output_files(topic_name='supply-official', topic_title=supply_official, list_path=list_path)
        # self.generate_csv_output_files(topic_name='statement-in-debate', topic_title=statement_in_debate,
        #                                list_path=list_path)
        # self.generate_csv_output_files(topic_name='address-debate', topic_title=address_debate, list_path=list_path)
        # self.generate_csv_output_files(topic_name='canada-united', topic_title=canada_united, list_path=list_path)
        # self.generate_csv_output_files(topic_name='house-of-commons-debates', topic_title=house_of_commons_debates,
        #                                list_path=list_path)
        # self.generate_csv_output_files(topic_name='other-debate', topic_title=debate_list, list_path=list_path)

    def generate_csv_output_files(self, topic_name, topic_title, list_path):
        Collect_data(topic_name=topic_name, topic_list=topic_title, list_path=list_path)
        RemoveFields(topic_name=topic_name)
        RemoveCliche(topic_name=topic_name)
        ControversialTopics(topic_name=topic_name)
        Labelling(topic_name=topic_name)
        Split_Speechtext(topic_name=topic_name)
        print("Done the process of generating set of '{}' files".format(topic_name))


if __name__ == '__main__':
    Main()
