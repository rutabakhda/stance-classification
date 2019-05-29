# wstud-visit-the-dome-ss19

The repository for the student project "visit the dome".

## Project Setup

### Install Eclipse, Gradle and the Required Eclipse-Plugins

* Install the Eclipse IDE.
* Install the Eclipse UIMA-Plugins. (Instruction can be found [here](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/blob/master/documentation/overview_and_setup.pdf))
* Install Gradle.

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

* Clone the [tt4j-tree-tagger](https://git.webis.de/thirdparty/thirdparty-tt4j-1.1.0) repository.
```
git clone git@webis.uni-weimar.de:thirdparty/thirdparty-tt4j-1.1.0.git
```

### Put the "lib" Directory into the aitools4-ie-uima Repository

* [TODO]


### Import the Projects to Eclipse

All Projects need to be on the same level, otherwise the project will not be working properly.

* Open Eclipse

* Import the aitools4-ie-uima project as a gradle project.

* Import the wstud-visit-the-dome-ss19 project as a gradle project. 


## Project Structure

### Corpora

In the [data](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/data) directory exists a subdirectory for ever corpus we were working on.

In the directories of the different corpora there exist an "arff" directory (e.g. [debatepedia](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/data/debatepedia/arff)), which contains the arff feature files for the corpora.

### Notebooks

The [notebook](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/notebooks) directory contains jupyter notebooks, which contain the preprocessing steps and data analysis for the different corpora.

### Java

The [java](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/java) directory contains the java source code.

### Resources

The [resources](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources) directory contains uima descriptor files and property files for the feature extraction process.

The [properties](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties) directory contains the [experiment](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/experiment), [feature](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/feature) and [normalization](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/normalization) directories.

The [experiment](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/experiment) directoy contains the property files for the experiment configuration.

The [feature](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/feature) directory contains the property files for the feature configuration.

The [normalization](https://git.webis.de/webisstud/wstud-visit-the-dome-ss19/tree/master/src/main/resources/properties/normalization) directory contains the property files, which are used for the computation of the features. They are created automatically during the feature computation process, so there is no need to modify anything in this directory.


## Contributors

* [TODO]