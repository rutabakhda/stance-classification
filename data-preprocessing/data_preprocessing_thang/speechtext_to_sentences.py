import numpy as np
import pandas as pd
import os
import shutil
from keras.preprocessing.text import Tokenizer
from nltk import sent_tokenize
import csv
import re

class Split_Speechtext():
    def __init__(self, topic_name):
        super().__init__()

        basepath = os.path.dirname(os.path.abspath(__file__))
        datapath = basepath + "/result/{}/".format(topic_name)  # Datapath for Oral Questions

        readfile = 'labelled-{}.csv'.format(topic_name)

        filename = 'sentences-{}.csv'.format(topic_name)
        newfile = os.path.join(datapath, filename)

        self.create_csv(input_file=newfile)
        self.speechtext_to_sentences(docs=os.path.join(datapath, readfile), output_file=newfile)

    def create_csv(self, input_file):
        """
        :param input_file: path to a .csv file
        :return: nothing
        """
        output_path = input_file.replace("\\", "/")
        with open(output_path, mode="a", encoding="utf-8") as csvfile:
            field = ["Role", "basepk", "speechdate",
                     "subtopic", "speakerparty", "sentences", "speakername"]
            csv_file = csv.DictWriter(f=csvfile, fieldnames=field)
            csv_file.writeheader()
        csvfile.close()

    def speechtext_to_sentences(self, docs, output_file):
        count = 0
        content = pd.read_csv(filepath_or_buffer=docs, header=0).values
        with open(file=output_file, mode='a', encoding="utf-8") as output_csv:
            output_writer = csv.writer(output_csv)
            for row in content:
                role = str(row[0])
                basepk = str(row[1])
                speechdate = str(row[2])
                subtopic = str(row[3])
                speakerparty = str(row[4])
                speakername = str(row[5])
                # sentences = sent_tokenize(text=str(row[5]).lower(), language='english')
                sentences = self.split_into_sentences(text=str(row[6]).lower())
                for sentence in sentences:
                    count += 1
                    text = [role, basepk, speechdate, subtopic, speakerparty, sentence, speakername]
                    output_writer.writerow(text)

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

if __name__ == '__main__':
    Split_Speechtext()