#!/bin/bash
####################################
#
# ADU Classification Pipeline
# Input: Json File
# Process:
STEP1="Split File into Training & Testing"
STEP2="Use UIMA to convert to XMI files"
STEP3="Generate Feature Files"
STEP4="Use Weka to train classifier"
# 4. Generate output results
# Output: Performace of Classfier or Labelled Data
#
####################################

echo $PWD
echo
CLASSPATH=bin/main:../aitools4-ie-uima/bin/main:../.gradle/caches/modules-2/files-2.1/org.apache.uima/uimaj-tools/2.7.0/a59d128b03ff9a0bc5016c1faecd6799b12632f5/uimaj-tools-2.7.0.jar:../.gradle/caches/modules-2/files-2.1/org.apache.uima/uimaj-document-annotation/2.7.0/44243011b32316cf4d44183936a78c968e640d9e/uimaj-document-annotation-2.7.0.jar:../.gradle/caches/modules-2/files-2.1/org.apache.uima/uimaj-cpe/2.7.0/726ac0cfc5c4e8f582abd08d177245d0b61424d2/uimaj-cpe-2.7.0.jar:../.gradle/caches/modules-2/files-2.1/org.apache.uima/uimaj-adapter-vinci/2.7.0/ec72c997e1496b54e3fd4c72f03389476cc8ccae/uimaj-adapter-vinci-2.7.0.jar:../.gradle/caches/modules-2/files-2.1/org.apache.uima/uimaj-core/2.7.0/8432471d972f344c317698ef05ce0433aeb91f76/uimaj-core-2.7.0.jar:../.gradle/caches/modules-2/files-2.1/com.syncthemall/boilerpipe/1.2.2/c2df7f14474b85529fc9965b1f8da531645e0a80/boilerpipe-1.2.2.jar:../.gradle/caches/modules-2/files-2.1/com.ibm.icu/icu4j/53.1/786d9055d4ca8c1aab4a7d4ac8283f973fd7e41f/icu4j-53.1.jar:../.gradle/caches/modules-2/files-2.1/com.github.rholder/snowball-stemmer/1.3.0.581.1/35a89d519949c33c6f28e8f37b3df7893b776ca4/snowball-stemmer-1.3.0.581.1.jar:../.gradle/caches/modules-2/files-2.1/edu.stanford.nlp/stanford-corenlp/3.5.2/1d5d0876de963c41ebf39d1d5570972ca7b592b4/stanford-corenlp-3.5.2.jar:../.gradle/caches/modules-2/files-2.1/com.googlecode.mate-tools/anna/3.0/84bc3d5700a3a82a7aa452139e3da98d8439bac2/anna-3.0.jar:../.gradle/caches/modules-2/files-2.1/com.google.code.structure-graphic/structure-graphic/1.0/4acce5f4904d8804e33d41d561fa7ce4e46c5c6a/structure-graphic-1.0.jar:../.gradle/caches/modules-2/files-2.1/de.webis.aitools/aitools4-ie-texhyphenator4j/1.1/a9c6411215bd1ecdbf5d3f500e9724850aaa9a1a/aitools4-ie-texhyphenator4j-1.1.jar:../.gradle/caches/modules-2/files-2.1/tw.edu.ntu.csie/libsvm/3.1/69f4a2fd91f0033446a6aaa21e71f706529ae61a/libsvm-3.1.jar:../.gradle/caches/modules-2/files-2.1/nz.ac.waikato.cms.weka/weka-dev/3.7.5/eef311f8f334ab6ac45cb4c68de2728cb7511340/weka-dev-3.7.5.jar:../.gradle/caches/modules-2/files-2.1/org.annolab.tt4j/org.annolab.tt4j/1.2.1/e60af715c9fce40617c8da7bcceeda0bae655d76/org.annolab.tt4j-1.2.1.jar:../.gradle/caches/modules-2/files-2.1/net.sourceforge.nekohtml/nekohtml/1.9.19/8a49406347d345bade1e6152e05e5f4dcbf7def5/nekohtml-1.9.19.jar:../.gradle/caches/modules-2/files-2.1/com.io7m.xom/xom/1.2.10/4165e25bef19aad134f6498cc277110b9bc5e52b/xom-1.2.10.jar:../.gradle/caches/modules-2/files-2.1/de.jollyday/jollyday/0.4.7/aa1c57aa11494985854b8ec8d39574754db67f22/jollyday-0.4.7.jar:../.gradle/caches/modules-2/files-2.1/joda-time/joda-time/2.1/8f79e353ef77da6710e1f10d34fc3698eaaacbca/joda-time-2.1.jar:../.gradle/caches/modules-2/files-2.1/com.googlecode.efficient-java-matrix-library/ejml/0.23/fb9a880674f0d241d727ee2bc5e6a839d3007fe8/ejml-0.23.jar:../.gradle/caches/modules-2/files-2.1/javax.json/javax.json-api/1.0/a74939ecbf7294b40accb4048929577f5ddcee2/javax.json-api-1.0.jar:../.gradle/caches/modules-2/files-2.1/net.sf.squirrel-sql.thirdparty-non-maven/java-cup/0.11a/1de46cc85d147d9f91af59d4a0107091c8b112d6/java-cup-0.11a.jar:../.gradle/caches/modules-2/files-2.1/org.pentaho.pentaho-commons/pentaho-package-manager/0.9.9/b4a92864320847a170b549b1864185d5305fd359/pentaho-package-manager-0.9.9.jar:../.gradle/caches/modules-2/files-2.1/org.apache.uima/jVinci/2.7.0/a1ae863231ceb2c2463eeaa7d4aa254aa1dccec6/jVinci-2.7.0.jar:../.gradle/caches/modules-2/files-2.1/xalan/xalan/2.7.0/a33c0097f1c70b20fa7ded220ea317eb3500515e/xalan-2.7.0.jar:../.gradle/caches/modules-2/files-2.1/javax.xml.bind/jaxb-api/2.2.7/2f51c4bb4724ea408096ee9100ff2827e07e5b7c/jaxb-api-2.2.7.jar:../.gradle/caches/modules-2/files-2.1/org.json/json/20180813/8566b2b0391d9d4479ea225645c6ed47ef17fe41/json-20180813.jar:../apache-uima/lib/jackson-core-2.9.2.jar:../apache-uima/lib/java-json.jar:../apache-uima/lib/javaparser-core-3.2.2.jar:../apache-uima/lib/jVinci.jar:../apache-uima/lib/org.annolab.tt4j-1.0.16.jar:../apache-uima/lib/procyon-compilertools-0.5.32.jar:../apache-uima/lib/procyon-core-0.5.32.jar:../apache-uima/lib/slf4j-api-1.7.25.jar:../apache-uima/lib/slf4j-jdk14-1.7.25.jar:../apache-uima/lib/uima-adapter-soap.jar:../apache-uima/lib/uima-adapter-vinci.jar:../apache-uima/lib/uima-core.jar:../apache-uima/lib/uima-cpe.jar:../apache-uima/lib/uima-document-annotation.jar:../apache-uima/lib/uima-examples.jar:../apache-uima/lib/uimaj-bootstrap.jar:../apache-uima/lib/uimaj-json.jar:../apache-uima/lib/uimaj-v3migration-jcas.jar:../apache-uima/lib/uima-tools.jar

function step1(){
    # step 1
    echo $STEP1
    # source ../my_env/bin/activate
    cd python
    PATH_TO_JSON=../data/debatepedia/debatepedia-preprocessed.json
    split_path=`python debatepedia2.py -p $PATH_TO_JSON`
    echo $split_path
    cd ..
    echo ....ok
    echo
}

function step2(){
    # step 2
    echo $STEP2
    java -cp $CLASSPATH usage.DebatepediaProcessingPipeline $split_path
    echo ....ok
    echo
}

function step3(){
    # step 3
    echo $STEP3
    file_path=src/main/resources/properties/experiment/experiment-config_debatepedia.properties
    training_path="$split_path/xmi/debatepedia-preprocessed_train"
    testing_path="$split_path/xmi/debatepedia-preprocessed_test"
    output_path="$split_path/arff"
    # replace training path
    search_pattern="input_corpus_folder_0"
    replace_line="$search_pattern=$training_path"
    configLine ^$search_pattern $replace_line $file_path
    # replace testing path
    search_pattern="input_corpus_folder_1"
    replace_line="$search_pattern=$testing_path"
    configLine ^$search_pattern $replace_line $file_path
    # replace output path
    search_pattern="output_folder"
    replace_line="$search_pattern=$output_path"
    configLine ^$search_pattern $replace_line $file_path
    java -cp $CLASSPATH usage.FeatureFileGenerator
    echo ....ok
    echo
}

function step4(){
    # step 4
    echo $STEP4
    echo $split_path
    arff_folder=$split_path/arff

    java -classpath ../weka/weka.jar weka.classifiers.trees.RandomForest -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1 \
    -t $arff_folder/*train.arff \
    -T $arff_folder/*test.arff \
    -do-not-check-capabilities -o

    echo ....ok
    echo
}

#configLine [searchPattern] [replaceLine] [filePath]
function configLine {
  local OLD_LINE_PATTERN=$1; shift
  local NEW_LINE=$1; shift
  local FILE=$1
  local NEW=$(echo "${NEW_LINE}" | sed 's/\//\\\//g')
  echo $PWD
  touch "${FILE}"
  sed -i '/'"${OLD_LINE_PATTERN}"'/{s/.*/'"${NEW}"'/;h};${x;/./{x;q100};x}' "${FILE}"
  if [[ $? -ne 100 ]] && [[ ${NEW_LINE} != '' ]]
  then
    echo "${NEW_LINE}" >> "${FILE}"
  fi
}

#split_path='data/debatepedia/2019-05-31_02:41:04'
if [[ "$1" == "1" ]]
then
step1
elif [[ "$1" == "2" ]]
then
step2
elif [[ "$1" == "3" ]]
then
step3
elif [[ "$1" == "4" ]]
then
step4
else
step1
step2
step3
step4
fi