from common import Common
import os
import re
import nltk
import pandas as pd
from common import Common

class SeparateIntoLines():
    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath_sbm = basepath + "/lipad1/annotation/"  # Datapath for Statement by Members
    datapath_oq = basepath + "/lipad1/oral-questions/"  # Datapath for Oral Questions

    readfile_sbm = 'statement-by-members-controversial-topics-sample.csv'

    newfile_sbm = 'test.csv'

    #newdir_path = os.path.dirname(basepath)
    newdir_path = basepath + "/lipad1/annotation/"

    def __init__(self):
        super().__init__()
        self.common = Common()

        # convert_into_lines(datapath_oq, 'controversial-data.csv', outname)
        # write_to_text(datapath_oq, 'controversial-data-separate-lines-sample-single.csv', 'segment-labeling-sample-single.txt')

        self.convert_into_lines(self.datapath_sbm, self.readfile_sbm, self.newfile_sbm, self.newdir_path)
        # write_to_text(datapath_sbm, 'statement-by-members-controversial-topics-sample-separate-lines.csv', 'segment-labeling.txt')

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

    def convert_into_lines(self, path, file, newfile, newdir_path):

        new_data = pd.DataFrame(columns=['basepk', 'maintopic', 'split_speech_text','speakerparty'])
        data = self.common.read_csv(path, file)
        for index, row in data.iterrows():
            speechtext = row.speechtext_without_cliche
            basepk = row.basepk
            speech = str(speechtext)
            splitted_text = self.split_into_sentences(speech)
            new_row = {}
            check = 0

            speech_dir = newdir_path + str(basepk) + "/"
            self.common.make_dir(speech_dir)

            txtfile = self.common.write_to_text(speech_dir, 'segment-labeling.txt')

            for split_statement in splitted_text:
                new_row['basepk'] = row.basepk
                new_row['maintopic'] = row.maintopic
                new_row['speakerparty'] = row.speakerparty

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
        new_data.to_csv(path + newfile, encoding='utf-8', index=False)

    def nltk_splitting(self, text):
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        splitted_text = sent_detector.tokenize(text.strip())
        # splitted_text = nltk.sent_tokenize(text)  # this gives us a list of sentences
        return splitted_text

if __name__ == '__main__':
    SeparateIntoLines()
