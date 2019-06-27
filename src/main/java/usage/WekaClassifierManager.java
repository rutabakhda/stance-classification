package usage;

import java.io.File;
import java.sql.Timestamp;    
import java.util.Date;    
import java.text.SimpleDateFormat;  
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import de.aitools.ie.uima.io.WekaFeatureFileWriter;

public class WekaClassifierManager {

	private static final String TRAINING_SET_PATH = "data/cross-domain/debatepedia_sample-sbm/arff/content-length_pos-ngrams_token-ngrams_2019-06-14_data-debatepedia-processed.arff";

	/**
	 * The path of the feature file (see {@link WekaFeatureFileWriter}) used for
	 * testing the classifier.
	 */
	private static final String TEST_SET_PATH = "data/cross-domain/debatepedia_sample-sbm/arff/content-length_pos-ngrams_token-ngrams_2019-06-14_data-sample-sbm-processed.arff";
	private String modelFilePath = "data/cross-domain/debatepedia_sample-sbm/models/debatepedia.model";
	// -------------------------------------------------------------------------
	// REFERENCES
	// -------------------------------------------------------------------------

	/**
	 * The classifier provided in the constructor.
	 */
	private final Classifier classifier;

	/**
	 * Patterns of names of attributes to be removed from training and test set.
	 */
	private final List<Pattern> attributeIgnorePatterns;

	/**
	 * The instances read from the feature file provided in the constructor.
	 */
	private final Instances trainingInstances;

	// -------------------------------------------------------------------------
	// INITIALIZATION
	// -------------------------------------------------------------------------

	/**
	 * The constructor creates and trains a new {@link RandomForest} classifier with
	 * the provided feature file.
	 * 
	 * @param trainingSetFeatureFile The features used for training the classifier.
	 * @throws Exception If the file could not be read or the classifier not be
	 *                   trained.
	 */
	public WekaClassifierManager(File trainingSetFeatureFile) throws Exception {
		this(new RandomForest(), new ArrayList<Pattern>(), trainingSetFeatureFile);
	}

	/**
	 * The constructor trains the provided classifier with the provided feature
	 * file.
	 * 
	 * @param classifier              The classifier to use.
	 * @param attributeIgnorePatterns Patterns of names of attributes to be removed
	 *                                from training and test set.
	 * @param trainingSetFeatureFile  The feature vectors used for training the
	 *                                classifier.
	 * @throws Exception If the file could not be read or the classifier not be
	 *                   trained.
	 */
	public WekaClassifierManager(Classifier classifier, Iterable<Pattern> attributeIgnorePatterns,
			File trainingSetFeatureFile) throws Exception {
		this.classifier = classifier;
		this.attributeIgnorePatterns = new ArrayList<>();
		for (final Pattern pattern : attributeIgnorePatterns) {
			this.attributeIgnorePatterns.add(pattern);
		}
		this.trainingInstances = this.readInstances(trainingSetFeatureFile);
		// Train classifier
		System.out.println("=== Start ===");
		System.out.println(
				"Building " + this.classifier.getClass().getSimpleName() + " on " + this.trainingInstances.size()
						+ " instances with " + this.trainingInstances.numAttributes() + " attributes.");
		this.classifier.buildClassifier(this.trainingInstances);
		System.out.println("Built: " + this.classifier);
		String modelFileFolder = trainingSetFeatureFile.getParentFile().getParent() + "/" + "models";
		String modelFilePath = modelFileFolder + "/" + "model-" + this.getDateTime();              
		// Save model
		weka.core.SerializationHelper.write(modelFilePath, classifier);
	}
	
	private String getDateTime(){    
        Date date = new Date();  
        Timestamp ts=new Timestamp(date.getTime());  
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");  
        return formatter.format(ts);                     
	}

	// -------------------------------------------------------------------------
	// CLASSIFICATION METHODS
	// -------------------------------------------------------------------------

	/**
	 * Classify the feature vectors in the provided file and return an evaluation
	 * result object.
	 * 
	 * @param testSetFeatureFile The feature vectors used to evaluate the
	 *                           classifier.
	 * @return The evaluation result object.
	 * @throws Exception If the file could not be read or the feature vectors could
	 *                   not be classified.
	 */
	public Evaluation test(File testSetFeatureFile) throws Exception {
		Instances testInstances = this.readInstances(testSetFeatureFile);
		System.out.println("Evaluate on " + testInstances.size() + " instances");
		Evaluation evaluation = new Evaluation(this.trainingInstances);
		evaluation.evaluateModel(this.classifier, testInstances);
		return evaluation;
	}

	/**
	 * Classify the feature vectors in the provided file and print a summarization
	 * of the classifier and the results to standard output.
	 * 
	 * @param testSetFeatureFile The feature vectors used to evaluate the
	 *                           classifier.
	 *
	 * @throws Exception If the file could not be read or the feature vectors could
	 *                   not be classified.
	 */
	public void testAndPrint(File testSetFeatureFile) throws Exception {
		Evaluation evaluation = this.test(testSetFeatureFile);
		System.out.println();
		System.out.println("=== Summary ===");
		System.out.println(evaluation.toSummaryString());
		System.out.println();
		System.out.println(evaluation.toClassDetailsString());
		System.out.println();
		System.out.println(evaluation.toMatrixString());
	}

	// -------------------------------------------------------------------------
	// INTERNAL HELPERS
	// -------------------------------------------------------------------------

	/**
	 * Read the feature vectors in given file.
	 * 
	 * @param featureFile The file that contains the feature vectors.
	 * @return The read feature vectors.
	 * @throws Exception If the file could not be read.
	 */
	protected Instances readInstances(File featureFile) throws Exception {
		DataSource source = new DataSource(featureFile.getAbsolutePath());
		Instances instances = source.getDataSet();
		if (instances.classIndex() == -1) {
			instances.setClassIndex(instances.numAttributes() - 1);
		}

		if (!this.attributeIgnorePatterns.isEmpty()) {
			for (int a = instances.numAttributes() - 1; a >= 0; --a) {
				if (a == instances.classIndex()) {
					continue;
				}

				String attributeName = instances.attribute(a).name();
				for (Pattern pattern : this.attributeIgnorePatterns) {
					if (pattern.matcher(attributeName).matches()) {
						instances.deleteAttributeAt(a);
						break;
					}
				}
			}
		}

		return instances;
	}

	// -------------------------------------------------------------------------
	// MAIN
	// -------------------------------------------------------------------------

	/**
	 * Performs a simple training-and-test-set evaluation with a
	 * {@link RandomForest} classifier and prints a summary of the results to
	 * standard output.
	 * 
	 * @param args Either nothing (to use the {@link #TRAINING_SET_PATH} and
	 *             {@link #TEST_SET_PATH}) or
	 *             <P>
	 *             <CODE>
	 * training.arff test.arff [ignore-attribute [ignore-attribute] [...]]
	 * </CODE>
	 *             </P>
	 *             Where <CODE>ignore-attribute</CODE> are optional regular
	 *             expression patterns that match the attribute names that should be
	 *             ignored.
	 * @throws Exception If a file could not be read or the classifier could not be
	 *                   trained or evaluated.
	 */
	public static void classify(String trainingFeaturesFilePath, String testFeaturesFilePath) throws Exception {
		Classifier forest = new RandomForest();

		List<Pattern> attributeIgnorePatterns = new ArrayList<>();

		File trainingSetFeatureFile = new File(trainingFeaturesFilePath);
		WekaClassifierManager classifier = new WekaClassifierManager(forest, attributeIgnorePatterns,
				trainingSetFeatureFile);

		File testSetFeatureFile = new File(testFeaturesFilePath);
		classifier.testAndPrint(testSetFeatureFile);
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
		classify(trainingSetPath, testSetPath);

	}

}
