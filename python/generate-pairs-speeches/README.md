# Generate pairs of speeches

To generate positive / negative pairs of speeches made by politicians, based on their political position (government or opposition), term and frequent topics.

## Speech distribution for parties 
1. Read the csv ```Canadian_Parliament_CSV_Output/statement-by-members/labelled-statement-by-members.csv``` - webis 20
2. Group data by speaker party or political position
3. Draw barchart to visualize the distribution

## Divide by periods
1. Read the csv ```Canadian_Parliament_CSV_Output/statement-by-members/labelled-statement-by-members.csv``` - webis 20.
2. Divide data by parliament terms.
3. Save statements from each period to one folder.

## Divide by topics
1. Read the folder from previous step.
2. Divide all data by topics, get the most 10 frequent topic and plot a piechart of topics distribution for each term.
3. Save statements from each period and each topic to one folder.

## Combine statements to pairs
1. Read the folder from previous step.
2. Combine statements in the same term, about same topic to pairs of positive or negative based on its political position.
3. Results is saved in ```args_pairs.zip``` - webis20

The result of task is discussed in this [presentation](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/presentations/2019-08-19).
