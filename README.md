# wstud-visit-the-dome-ss19

The repository for the student project "visit the dome".  This project analyzes the entire collection of Canadian parliament discussions over 100 years and identifies arguments related to controversial topics and decides their stance in relation to topics. These arguments are then integrated into args.me search engine.

## Project Setup

### Install Eclipse, Gradle and the required Eclipse-Plugins

* Install the Eclipse IDE.
* Install the Eclipse UIMA-Plugins. (Instruction can be found [here](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/blob/master/documentation/overview_and_setup.pdf) in chapter 3.1.2)

### Clone the required Repositories

Clone all the repositories into the same directory.

* Clone [this](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19) repository.
```
git clone git@webis.uni-weimar.de:webisstud/wstud-visit-the-dome-ss19.git
```

* Clone the [aitools4-ie-uima](https://git.webis.de/aitools/aitools4-ie-uima) repository.
```
git clone git@webis.uni-weimar.de:aitools/aitools4-ie-uima.git
```

* Clone the [tt4j-wrapper](https://git.webis.de/aitools/aitools4-ie-tt4j-wrapper) repository.
```
git clone git@webis.uni-weimar.de:aitools/aitools4-ie-tt4j-wrapper.git
```

### Copy the lib Directory

```
cd aitools4-ie-tt4j-wrapper/
cp -avr lib/ ../aitools4-ie-uima/

```
The [tt4j-wrapper](https://git.webis.de/aitools/aitools4-ie-tt4j-wrapper) repository can be deleted afterwards.


### Import the Projects to Eclipse

All Projects need to be on the same level in Eclipse, otherwise the project will not be working properly.

* Open Eclipse.

* Import the [aitools4-ie-uima](https://git.webis.de/aitools/aitools4-ie-uima) project as a gradle project.

* Import the [wstud-visit-the-dome-ss19](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19) project as a gradle project.


## Project Structure

### Python

All the tasks that are run using Python. The input data is stored in webis 20.

*[Data Preprocessing](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/python/data-processing-python)* - Preprocess the parliament dataset.

*[Agreement Processing](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/python/agreement-processing)* - Get the results from wat-sl annotation and process.

*[Generate Pairs  Speeches](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/python/generate-pairs-speeches)* - Generate pairs of statements based on political position, topic and period.

*[Same side classification](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/python/same-side-classification)* - Classify whether the statements are in the same side of the topic.

### Notebook

The [notebook](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/notebooks) directory contains jupyter notebooks, which contain the preprocessing steps and data analysis for the different corpora.

### Wat-sl
Source code for running improved wat-sl annotation tool.

### Java
We use java for extracting claims from parliament statements.
##### Source code

The [src/main/java](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/java) directory contains the java source code. More explanation on how to use the source code for the task is in [src/main/java/usage](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/java/usage)

##### Corpora

In the [data](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/data) directory exists a subdirectory for every corpus we were working on.

In the directories of the different corpora there exist an "arff" directory (e.g. [debatepedia](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/data/debatepedia/arff)), which contains the arff feature files for the corpora.

##### Resources

The [src/main/resources](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources) directory contains uima descriptor files and property files for the feature extraction process.

The [properties](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties) directory contains the [experiment](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/experiment), [feature](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/feature) and [normalization](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/normalization) directories.

The [experiment](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/experiment) directoy contains the property files for the experiment configuration.

The [feature](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/feature) directory contains the property files for the feature configuration.

The [normalization](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/normalization) directory contains the property files, which are used for the computation of the features. They are created automatically during the feature computation process, so there is no need to modify anything in this directory.
