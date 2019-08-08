package usage;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class WekaClassifierManager {

	private Classifier classifier;
	private Instances trainingInstances;
	private Instances testingInstances;

	static String TRAINING_SET_PATH = "data/cross-domain/debatepedia_sample-sbm/arff/content-length_pos-ngrams_token-ngrams_2019-06-14_data-debatepedia-processed.arff";
	static String TEST_SET_PATH = "data/cross-domain/debatepedia_sample-sbm/arff/content-length_pos-ngrams_token-ngrams_2019-06-14_data-sample-sbm-processed.arff";

	private static final String INPUT_FILE = "data/sample-sbm/json/";
	private ArrayList<JSONObject> originalData;

	private ArrayList<JSONObject> getOriginalData() throws JSONException {

		File inputFolder = new File(INPUT_FILE);
		ArrayList<JSONObject> originalInstances = new ArrayList<JSONObject>();

		File[] files = inputFolder.listFiles(new FilenameFilter() {
			@Override
			public boolean accept(File dir, String name) {
				return name.endsWith(".json");
			}
		});

		for (File file : files){
			String json = this.readJsonFile(file);
			if (!json.equals("")) {
				JSONArray array = new JSONArray(json);
				for (int i=0; i < array.length(); i++) {
					originalInstances.add(array.getJSONObject(i));
				}
			}
		}
		return originalInstances;
	}

	public WekaClassifierManager(String trainingFeaturesFilePath, String testFeaturesFilePath) throws Exception {

		File trainingSetFeatureFile = new File(trainingFeaturesFilePath);
		File testFeatureFile = new File(testFeaturesFilePath);

		this.trainingInstances = this.readInstances(trainingSetFeatureFile);
		this.testingInstances = this.readInstances(testFeatureFile);

		this.classifier = new RandomForest();

		this.originalData = this.getOriginalData();

	}

	private String readJsonFile(File inputFile) {
		String content = "";
		try {
			BufferedReader reader = new BufferedReader(new FileReader(inputFile));
			String line = reader.readLine();
			while (line != null) {
				content = content + line;
				line = reader.readLine();
			}
			reader.close();
		} catch (Exception e) {
			throw new RuntimeException();
		}
		return content;
	}

	public static void main(String[] args) throws Exception {
		String trainingSetPath = TRAINING_SET_PATH;
		String testSetPath = TEST_SET_PATH;
		if (args.length > 0 && args[0].length() > 0) {
			trainingSetPath = args[0];

		}

		if (args.length > 1 && args[1].length() > 0) {
			testSetPath = args[1];
		}

		classify(trainingSetPath, testSetPath, false);
	}

	public static void classify(String trainingFeaturesFilePath, String testFeaturesFilePath, boolean traceback) throws Exception {
		boolean needTrain = true;

		String modelFilePath = "";
		String modelFileFolder = new File(trainingFeaturesFilePath).getParentFile().getParent() + "/" + "models";
		if (needTrain) {
			modelFilePath = modelFileFolder + "/" + "model-" + getDateTime();
		} else {
			File[] allModelFiles = new File(modelFileFolder).listFiles();
			Arrays.sort(allModelFiles, new Comparator<File>() {
				@Override
				public int compare(File f1, File f2) {
					return Long.compare(f1.lastModified(), f2.lastModified());
				}
			});
			modelFilePath = allModelFiles[0].getAbsolutePath();
		}

		WekaClassifierManager manager = new WekaClassifierManager(trainingFeaturesFilePath, testFeaturesFilePath);

		File trainingSetFeatureFile = new File(trainingFeaturesFilePath);

		manager.trainingInstances = manager.readInstances(trainingSetFeatureFile);

		manager.buildClassifier(trainingSetFeatureFile, modelFilePath);

		// manager.classifier = (Classifier) SerializationHelper.read(modelFilePath);
		File testSetFeatureFile = new File(testFeaturesFilePath);
		manager.testAndPrint(testSetFeatureFile, traceback);
	}

	private void buildClassifier(File trainingSetFeatureFile, String modelFilePath) throws Exception {
		// Train classifier
		System.out.println("=== Start ===");
		System.out.println(
				"Building " + this.classifier.getClass().getSimpleName() + " on " + this.trainingInstances.size()
						+ " instances with " + this.trainingInstances.numAttributes() + " attributes.");
		this.classifier.buildClassifier(this.trainingInstances);
		System.out.println("Built: " + this.classifier);

		// Save model
//		weka.core.SerializationHelper.write(modelFilePath, classifier);
	}

	private Evaluation test(File testSetFeatureFile, boolean traceback) throws Exception {
		System.out.println("Evaluate on " + this.testingInstances.size() + " instances");
		System.out.println();
		Evaluation evaluation = new Evaluation(this.trainingInstances);
		evaluation.evaluateModel(this.classifier, this.testingInstances);

		if(traceback) {
			System.out.println("Tracing back to original data ...");
			System.out.println("Format: sentence" + "\n" + "actual unit type, predicted unit type \n");
			int countIncorrectPremise = 0;
			int countIncorrectConclusion = 0;

			for (int i = 0; i < this.testingInstances.size(); i++) {
				Instance instance = this.testingInstances.get(i);
				double prediction = this.classifier.classifyInstance(instance);
				String actualString = instance.classAttribute().value((int) instance.classValue());
				String predictedString = instance.classAttribute().value((int) prediction);

				if (!actualString.contentEquals(predictedString)) {
					JSONObject originalJsonObject = this.originalData.get(i);
					System.out.println(originalJsonObject.getString("content") + "\n"
							+ originalJsonObject.getString("unitType") + " , " + predictedString + "\n");
					if (actualString.contentEquals("premise")) {
						countIncorrectPremise++;
					} else if (actualString.contentEquals("conclusion")) {
						countIncorrectConclusion++;
					}
				}
			}

			System.out.println("===SUMMARY===");
			System.out.println("Number of incorrected labeled premise   : " + String.valueOf(countIncorrectPremise));
			System.out.println("Number of incorrected labeled conclusion: " + String.valueOf(countIncorrectConclusion));
			System.out.println("=============");
		}
		return evaluation;
	}

	public void testAndPrint(File testSetFeatureFile, boolean traceback) throws Exception {
		Evaluation evaluation = this.test(testSetFeatureFile, traceback);
		System.out.println();
		System.out.println("=== Summary ===");
		System.out.println(evaluation.toSummaryString());
		System.out.println();
		System.out.println(evaluation.toClassDetailsString());
		System.out.println();
		System.out.println(evaluation.toMatrixString());
	}

	private Instances readInstances(File featureFile) throws Exception {
		DataSource source = new DataSource(featureFile.getAbsolutePath());
		Instances instances = source.getDataSet();
		if (instances.classIndex() == -1) {
			instances.setClassIndex(instances.numAttributes() - 1);
		}

		return instances;
	}

	private static String getDateTime() {
		Date date = new Date();
		Timestamp ts = new Timestamp(date.getTime());
		SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		return formatter.format(ts);
	}
}