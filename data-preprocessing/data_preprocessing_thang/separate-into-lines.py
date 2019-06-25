import csv
import nltk
import os
import re
from os import path
import pandas as pd

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

def read_csv(datapath,filename):
    """ Reading the csv file from given path """
    read_csv_data = pd.read_csv(datapath+filename,delimiter=',' ,header=0,nrows=1)
    return read_csv_data

def read_csv_entire(datapath,filename):
    """ Reading the csv file from given path """
    read_csv_data = pd.read_csv(datapath+filename,delimiter=',' ,header=0)
    return read_csv_data



def split_into_sentences(text):
     text = " " + text + "  "
     text = text.replace("\n"," ")
     text = re.sub(prefixes,"\\1<prd>",text)
     text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
     text = re.sub(websites,"<prd>\\1",text)
     if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
     text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
     text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
     text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets +"[.]","\\1<prd>\\2<prd>\\3<prd>",text)
     text = re.sub(alphabets + "[.]" + alphabets +"[.]","\\1<prd>\\2<prd>",text)
     text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
     text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
     text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
     if "..." in text: text = text.replace("...","<prd><prd><prd>")
     if "”" in text: text = text.replace(".”","”.")
     if "\"" in text: text = text.replace(".\"","\".")
     if "!" in text: text = text.replace("!\"","\"!")
     if "?" in text: text = text.replace("?\"","\"?")
     text = text.replace(".",".<stop>")
     text = text.replace("?","?<stop>")
     text = text.replace("!","!<stop>")
     text = text.replace("<prd>",".")
     sentences = text.split("<stop>")
     sentences = sentences[:-1]
     sentences = [s.strip() for s in sentences]
     return sentences



def convert_into_lines(path,file,newfile):

    new_data = pd.DataFrame(columns=['speakeroldname','maintopic','split_speech_text'])
    data = read_csv(path,file)
    for index, row in data.iterrows():
        speechtext = row.speechtext_without_cliche
        speech = str(speechtext)
        splitted_text = split_into_sentences(speech)
        new_row = {}
        check = 0
        split_statement1 = ""

        for split_statement in splitted_text:
            new_row['speakeroldname'] = row.speakeroldname
            new_row['maintopic'] = row.maintopic

            #print('--------------------')
            #print(split_statement)

            if check == 0:
                if (split_statement.count('"') == 1):
                    check = 1
                    split_statement1 = 'Quote starts : '+split_statement
                    new_row['split_speech_text'] = split_statement1
                    new_data.loc[len(new_data)] = new_row

                else:
                    new_row['split_speech_text'] = split_statement
                    new_data.loc[len(new_data)] = new_row


            else:
                if (split_statement.count('"') == 1):
                    check = 0
                    split_statement1 = 'Quote ends : '+split_statement
                    new_row['split_speech_text'] = split_statement1
                    new_data.loc[len(new_data)] = new_row

                else:
                    split_statement1 = 'Quote continues : '+split_statement
                    new_row['split_speech_text'] = split_statement1
                    new_data.loc[len(new_data)] = new_row

            print('--------------------')
            print(split_statement1)

            # if check == 0:
            #
            #     if (split_statement.count('"') == 1):
            #         print("finally")
            #         check = 1
            #         speecht = speecht+split_statement
            #     else:
            #         new_row['split_speech_text'] = split_statement
            #         new_data.loc[len(new_data)] = new_row
            #
            # else:
            #     print('SHOULD GO HERE')
            #     if(split_statement.count('"') == 1):
            #         print('end')
            #         speecht = speecht + split_statement
            #         new_row['split_speech_text'] = speecht
            #         new_data.loc[len(new_data)] = new_row
            #         check = 0
            #         speecht = ''
            #     else:
            #         print('continue')
            #         speecht = speecht + split_statement
    new_data.to_csv(path+newfile, encoding='utf-8', index=False)

def nltk_splitting(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    splitted_text = sent_detector.tokenize(text.strip())
    #splitted_text = nltk.sent_tokenize(text)  # this gives us a list of sentences
    return splitted_text

def write_to_text(path,file,newfile):
    data = read_csv_entire(path,file)
    speechtext = data.split_speech_text
    txtfile = open(path+newfile, "a+")
    for index, speech in speechtext.iteritems():
        print(speech)
        txtfile.write(str(speech)+'\n')
    txtfile.close()

    
if __name__ == '__main__':

    basepath = os.path.dirname(os.path.abspath(__file__))
    datapath_sbm = basepath + "/lipad1/statement-by-members/"  # Datapath for Statement by Members

    #datapath_oq = basepath + "/lipad1/oral-questions/"  # Datapath for Statement by Members

    outname = 'test.csv'
    fullname_sbm = os.path.join(datapath_sbm,outname)
    #fullname_oq = os.path.join(datapath_oq, outname)

    #convert_into_lines(datapath_oq, 'controversial-data.csv', outname)
    #write_to_text(datapath_oq, 'controversial-data-separate-lines-sample-single.csv', 'segment-labeling-sample-single.txt')

    convert_into_lines(datapath_sbm, 'test-sample.csv', outname)
    #write_to_text(datapath_sbm, 'statement-by-members-controversial-topics-sample-separate-lines.csv', 'segment-labeling.txt')