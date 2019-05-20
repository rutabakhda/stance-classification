import csv
import nltk
import os
import re
from os import path
import pandas as pd

def read_csv(datapath,filename):
    """ Reading the csv file from given path """
    read_csv_data = pd.read_csv(datapath+filename,delimiter=',' ,header=0,nrows=1)
    return read_csv_data

def convert_into_lines(path,file,newfile):

    new_data = pd.DataFrame(columns=['speakeroldname','maintopic','split_speech_text'])
    data = read_csv(path,file)
    for index, row in data.iterrows():
        speechtext = row.speechtext_without_cliche
        speech = str(speechtext)
        splitted_text = nltk_splitting(speech)
        new_row = {}
        check = 0
        speecht = ""

        for split_statement in splitted_text:
            new_row['speakeroldname'] = row.speakeroldname
            new_row['maintopic'] = row.maintopic

            print('--------------------')
            print(split_statement)
            if check == 0:

                if (split_statement.count('"') == 1):
                    print("finally")
                    check = 1
                    speecht = speecht+split_statement
                else:
                    new_row['split_speech_text'] = split_statement
                    new_data.loc[len(new_data)] = new_row

            else:
                print('SHOULD GO HERE')
                if(split_statement.count('"') == 1):
                    print('end')
                    speecht = speecht + split_statement
                    new_row['split_speech_text'] = speecht
                    new_data.loc[len(new_data)] = new_row
                    check = 0
                    speecht = ''
                else:
                    print('continue')
                    speecht = speecht + split_statement
    new_data.to_csv(path+newfile, encoding='utf-8', index=False)

def nltk_splitting(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    splitted_text = sent_detector.tokenize(text.strip())
    #splitted_text = nltk.sent_tokenize(text)  # this gives us a list of sentences
    return splitted_text

def write_to_text(path,file,newfile):
    data = read_csv(path,file)
    speechtext = data.split_speech_text
    txtfile = open(path+newfile, "a+")
    for index, speech in speechtext.iteritems():
        print(speech)
        txtfile.write(speech+'\n')
    txtfile.close()

    
if __name__ == '__main__':

    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath_sbm = basepath + "/lipad1/statement-by-members/"  # Datapath for Statement by Members

    datapath_oq = basepath + "/lipad1/oral-questions/"  # Datapath for Statement by Members

    outname = 'controversial-data-separate-lines.csv'
    fullname_sbm = os.path.join(datapath_sbm,outname)
    fullname_oq = os.path.join(datapath_oq, outname)

    convert_into_lines(datapath_oq, 'controversial-data.csv', outname)
    write_to_text(datapath_oq, 'controversial-data-separate-lines.csv', 'segment-labeling.txt')

    convert_into_lines(datapath_sbm, 'controversial-data.csv', outname)
    write_to_text(datapath_sbm, 'controversial-data-separate-lines.csv', 'segment-labeling.txt')