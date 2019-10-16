 # Process annotation

Sentences above were labelled using our improved annotation tool [WAT-SL](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/wat-sl). The annotation results from our team is saved in web20. In wat-sl annotation structors, we have all annotators to manually label each sentence and the whole stance of the paragraph using the interface. In the end, if there is conflict in the annotation, curator will check and decide the final label.
Here, we process the curation results into a json file and calculate the agreement score between annotators.

## Generate annotation result
1. Read the curation results from wat-sl with 3 labels: conclusion, premise, non-argumentative.
2. Save the results as a json file in current directory.

## Calculate agreement score
1. Read all annotation results from wat-sl.
2. Because of the high non-agreement between annotators, we try to simplify by combining premise and non-argumentative classes, so that we only have 2 labels: conclusion and non-conclusion.
3. Calculate Fleiss kappa score of agreement.


The result of task is discussed in this [presentation](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/presentations/2019-08-12).
