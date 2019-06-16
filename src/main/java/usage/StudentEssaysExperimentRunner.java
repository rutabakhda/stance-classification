package usage;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import org.apache.uima.resource.ResourceInitializationException;
import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

/**
 * 
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class StudentEssaysExperimentRunner {

	private static final String CORPUS_NAME = "student-essays";
	
	private static final String[] SPLIT_TYPES = { "random", "by-topic" };
	
	private static final String[] FEATURE_TYPES = { "content-length_pos-ngrams_token-ngrams", 
													"content-length_pos-ngrams",
													"content-length_token-ngrams",
													"pos-ngrams_token-ngrams",
													"content-length",
													"pos-ngrams",
													"token-ngrams" };

	private static final String PROPERTIES_SPLIT_PATH = "src/main/resources/properties/split";
	
	private static final String PROPERTIES_FEATURE_GENERATOR_PATH = "src/main/resources/properties/feature_file_generator";

	private StudentEssaysProcessor processor;

	private TrainTestSplitter splitter;

	private GenericFeatureFileGenerator generator;

	private ArrayList<String> featureGeneratorPropertiesPaths;

	private ArrayList<String> splitPropertiesPaths;

	private File featuresfilePath;

	public StudentEssaysExperimentRunner() throws ResourceInitializationException, IOException {

		this.featureGeneratorPropertiesPaths = new ArrayList<String>();
		this.splitPropertiesPaths = new ArrayList<String>();
		this.featuresfilePath = new File("data" + "/" + CORPUS_NAME + "/" + "arff");

		for (String splitType : SPLIT_TYPES) {
			String splitPropertiesPath = PROPERTIES_SPLIT_PATH + "/" + CORPUS_NAME + "/" + "split-config" + "_"
					+ splitType + ".properties";
			this.splitPropertiesPaths.add(splitPropertiesPath);

			for (String featureType : FEATURE_TYPES) {
				String featureGeneratorPropertiesPath = PROPERTIES_FEATURE_GENERATOR_PATH + "/" + CORPUS_NAME + "/"
						+ splitType + "/" + featureType + ".properties";
				this.featureGeneratorPropertiesPaths.add(featureGeneratorPropertiesPath);
			}
		}

		this.processor = new StudentEssaysProcessor();

	}

	public void run() throws ResourceInitializationException, IOException {

		this.processor.processCollection();

		// Splitting files

		for (String splitPropertiesPath : this.splitPropertiesPaths) {
			splitter = new TrainTestSplitter(splitPropertiesPath);
			splitter.split();
		}

		// Generating feature files

		for (String propertiesPath : featureGeneratorPropertiesPaths) {
			generator = new GenericFeatureFileGenerator(propertiesPath);
			generator.generatorFeatureFiles();
		}

		// Run Weka for each pair of feature files
		for (String splitType : SPLIT_TYPES) {
			for (String featureType : FEATURE_TYPES) {
				File[] files = this.featuresfilePath.listFiles();
				String trainingFeaturesPath = "";
				String testingFeaturesPath = "";
				String[] trainingFilePatterns = new String[] { CORPUS_NAME, splitType, featureType, "train" };
				String[] testingFilePatterns = new String[] { CORPUS_NAME, splitType, featureType, "test" };
				String extension = ".arff";

				// Search for training file
				trainingFeaturesPath = this.listFilesMatchingPatternNewest(this.featuresfilePath, trainingFilePatterns,
						extension)[0].getAbsolutePath();
				testingFeaturesPath = this.listFilesMatchingPatternNewest(this.featuresfilePath, testingFilePatterns,
						extension)[0].getAbsolutePath();

				System.out.println("\n\n\nNew Experiment....");
				System.out.println(trainingFeaturesPath);
				System.out.println(testingFeaturesPath);

				try {
					WekaClassifierManager.classify(trainingFeaturesPath, testingFeaturesPath);
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
	}

	// Get the list of files (newest to oldest) that satisfies the patterns
	private File[] listFilesMatchingPatternNewest(File folder, String[] patterns, String extension) {
		File[] files = folder.listFiles(new FilenameFilter() {
			@Override
			public boolean accept(File dir, String name) {
				boolean shouldAccept = false;
				if (name.endsWith(extension)) {
					for (String pattern : patterns) {
						if (!name.contains(pattern)) {
							shouldAccept = false;
							break;
						} else {
							shouldAccept = true;
							continue;
						}
					}

				}
				return shouldAccept;
			}
		});

		Arrays.sort(files, new Comparator<File>() {
			public int compare(File f1, File f2) {
				return Long.compare(f1.lastModified(), f2.lastModified());
			}
		});
		return files;
	}

	public static void main(String[] args) throws ResourceInitializationException, IOException {
		StudentEssaysExperimentRunner runner = new StudentEssaysExperimentRunner();
		runner.run();
	}
}
