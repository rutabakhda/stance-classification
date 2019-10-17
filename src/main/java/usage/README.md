# Claim Extraction
Claim Extractor tries to classify conclusion vs premise sentence.

An in-domain claim extractor follows these steps:
1. Processor
2. Splitting files
3. Generate feature files
4. Run weka classifier

A cross-domain claim extractor follows these steps:
1. Processor for training set
2. Processor for test set
3. Generate feature files
4. Run weka classifier

We experimented with WebisDebate, Debatepedia, StudentEssay and Sampled Statement by Members (from Canadian Parliament Statements)
The result of task is discussed in  [classify-conclusion-premise](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/presentations/2019-05-27/classify-conclusion-premise.pdf), [experiment-on-studentessay-debatepedia-corpora](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/presentations/2019-06-17/experiments-on-student-essays-and-debatepedia-corpora.pdf), [parliamentary-data-mining](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/presentations/2019-06-17/parlimentary-debates-mining.pdf), [summary-of-current-status](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/presentations/2019-08-12/summary-of-current-status.pdf)
