# Data Preprocessing

To find the speech-text by Canadian parliament members which contains arguments for controversial topics.

## Basic Preprocessing
1. Filtering speech-text which are "Oral questions" or "statement by members ```combine_topics.py```
2. Removing duplicates and cleaning the data ```common.py```
3. Running analysis on above data to find statistics such as most occurring sequential words, most discussed topics ``` process.py```


## Extracting controversial speeches from processed data
1. Removing cliches from the speech-texts ```remove_cliche.py```
2. Using Wikipedia controversial topics list to identify controversial topics ```find_controversial_topics.py```
3. Finding controversial speech-text for controversial topics based on the controversial word occurrences and sentiment analysis
4. Running statistics on found controversial topics

## Identifying political position of the speech-text
1. Generating a text file with time duration of each term with ruling party and opposition party with members list ```labelling.py```
2. Adding the political position of the member in each speech-text

## Retrieving controversial arguments from the entire speech-texts
1. As our focus is controversial arguments, we need to identify controversial part of the speeches
2. Splitting the speeches into individual sentences ```separate_into_lines.py```
3. Labeling each sentence as argumentative, non argumentative and conclusion

## Annotation of speeches using WAT-SL tool
Sentences above were labelled using annotation tool [WAT-SL](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/wat-sl)








