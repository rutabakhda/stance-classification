import os
from common import Common
import pandas as pd
import re

class generateAnnotations():

    def __init__(self):
        super().__init__()

        self.common = Common()

        basepath = os.path.dirname(os.path.abspath(__file__))
        datapath_sbm = basepath + "/lipad1/data/statement-by-members/"  # Datapath for Statement by Members
        datapath_oq = basepath + "/lipad1/oral-questions/"  # Datapath for Oral Questions
        datapath_annotation = basepath + "/lipad1/annotation/"  # Datapath for Oral Questions
        readfile_oq = 'controversial-oral-questions.csv'
        readfile_sbm = 'controversial-statement-by-members.csv'

        newdir_path = os.path.dirname(basepath)
        newdir_path = newdir_path + "/example-project/tasks/"

        #self.speech_to_annotations(datapath_sbm,readfile_sbm,newdir_path)
        self.convert_into_lines(datapath_sbm, readfile_sbm,datapath_annotation,newdir_path)

    def speech_to_annotations(self,datapath,readfile,newdir_path):

        data = self.common.read_csv(datapath, readfile)
        oq1 = data['subtopic'] == "Abortions"
        oq2 = data['subtopic'] == "Abortion"
        oq3 = data['subtopic'] == "Status of Women"
        oq4 = data['subtopic'] == "Human Rights"
        oq5 = data['subtopic'] == "Human Rights in Sudan"
        oq6 = data['subtopic'] == "Criminal Code"
        oq7 = data['subtopic'] == "Immigration"
        oq8 = data['subtopic'] == "Body Shaming"

        cat_data = data[oq1 | oq2 | oq3 | oq4 | oq5 | oq6 | oq7 | oq8]

        for row in cat_data.itertuples():
            basepk = row.basepk
            speech = row.speechtext_without_cliche

            speech_dir = newdir_path + str(basepk) + "/"
            self.common.make_dir(speech_dir)

            txtfile = self.common.write_to_text(speech_dir,'segment-labeling.txt')
            txtfile.write(str(speech))
            txtfile.close()

    def split_into_sentences(self, text):
        alphabets = "([A-Za-z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"
        digits = "([0-9])"

        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
        text = re.sub(websites, "<prd>\\1", text)
        if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
        text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
        text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
        if "..." in text: text = text.replace("...", "<prd><prd><prd>")
        if "”" in text: text = text.replace(".”", "”.")
        if "\"" in text: text = text.replace(".\"", "\".")
        if "!" in text: text = text.replace("!\"", "\"!")
        if "?" in text: text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    def convert_into_lines(self, path, file, datapath_annotation, newdir_path):


        data = self.common.read_csv(path, file)
        oq1 = data['subtopic'] == "Abortions"
        oq2 = data['subtopic'] == "Abortion"
        oq3 = data['subtopic'] == "Status of Women"
        oq4 = data['subtopic'] == "Human Rights"
        oq5 = data['subtopic'] == "Human Rights in Sudan"
        oq6 = data['subtopic'] == "Criminal Code"
        oq7 = data['subtopic'] == "Immigration"
        oq8 = data['subtopic'] == "Body Shaming"

        cat_data = data[oq1 | oq2 | oq3 | oq4 | oq5 | oq6 | oq7 | oq8]

        for index, row in cat_data.iterrows():
            new_data = pd.DataFrame(columns=['basepk', 'split_speech_text', 'speakerparty'])
            speechtext = row.speechtext_without_cliche
            basepk = row.basepk
            speech = str(speechtext)
            splitted_text = self.split_into_sentences(speech)
            new_row = {}
            check = 0

            speech_dir = newdir_path + str(int(basepk)) + "/"
            self.common.make_dir(speech_dir)

            txtfile = self.common.write_to_text(speech_dir, 'segment-labeling.txt')

            for split_statement in splitted_text:
                new_row['basepk'] = int(row.basepk)
                new_row['speakerparty'] = row.speakerparty
                #print(split_statement)
                new_row['split_speech_text'] = split_statement

                if check == 0:
                    if (split_statement.count('"') == 1):
                        check = 1
                        split_statement = 'QUOTE_START ' + split_statement
                        new_row['split_speech_text'] = split_statement
                        new_data.loc[len(new_data)] = new_row

                    else:
                        new_row['split_speech_text'] = split_statement
                        new_data.loc[len(new_data)] = new_row

                else:
                    if (split_statement.count('"') == 1):
                        check = 0
                        split_statement = 'QUOTE_END ' + split_statement
                        new_row['split_speech_text'] = split_statement
                        new_data.loc[len(new_data)] = new_row

                    else:
                        split_statement = 'QUOTE_CONTINUE ' + split_statement
                        new_row['split_speech_text'] = split_statement
                        new_data.loc[len(new_data)] = new_row

                txtfile.write(str(new_row['split_speech_text']) + '\n')
            txtfile.close()
            print(new_row)
            new_data.loc[len(new_data)] = new_row
            outfile = open(datapath_annotation + str(int(basepk))+".csv",'w+', encoding='utf-8' )
            new_data.to_csv(outfile)
            outfile.close()


if __name__=='__main__':
    generateAnnotations()