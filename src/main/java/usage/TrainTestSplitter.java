package usage;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;


import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.FSIterator;
import org.apache.uima.cas.impl.XmiCasDeserializer;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;
import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.FileUtils;
import org.apache.uima.util.XMLInputSource;


import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;

/**
 * 
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class TrainTestSplitter {
	
	
	private static final String PROPERTIES_PATH = "src/main/resources/properties/split/split-config_debatepedia-test.properties";
	
	
	private static final String PARAM_INPUT_DIRECTORY = "input_directory";
	
	private static final String PARAM_OUTPUT_DIRECTORY = "output_directory";
	
	private static final String PARAM_PERCENT_TRAINING_SET = "percent_training_set";
	
	private static final String PARAM_BY_TOPIC_BOOLEAN = "by-topic";
	
	//private static final String PARAM_ANNOTATION_TYPE = "annotation_type";
	
	//private static final String PARAM_ANNOTATION_FEATURE_TYPE = "annotation_feature_type";
	
	//private static final String PARAM_CLASS_1_ANNOTATION_FEATURE_VALUE = "class_1_annotation_feature_value";
	
	//private static final String PARAM_CLASS_2_ANNOTATION_FEATURE_VALUE = "class_2_annotation_feature_value";
	
	
	private static final String FILE_EXTENSION = ".xmi";
	
	
	private File inputDirectory;

	private File outputDirectory;
	
	private double percentTrainingSet;
	
	private File trainingSetDirectory;
	
	private File testSetDirectory;
	
	private ArrayList<File> files;
	
	private boolean byTopic;
	
	private ArrayList<File> trainingSet;
	private ArrayList<File> testingSet;
	
	
	/**
	 * 
	 * @throws ResourceInitializationException
	 * @throws IOException
	 */
	public TrainTestSplitter() throws ResourceInitializationException, IOException {
		this.initialize(PROPERTIES_PATH);
	}

	
	/**
	 * 
	 * @param propertiesPath
	 * @throws ResourceInitializationException
	 * @throws IOException
	 */
	public TrainTestSplitter(String propertiesPath) throws ResourceInitializationException, IOException {
		this.initialize(propertiesPath);
	}
	
	
	/**
	 * 
	 * @param propertiesPath
	 * @throws ResourceInitializationException
	 */
	private void initialize(String propertiesPath) throws ResourceInitializationException {
		try {
			InputStream input = new FileInputStream(propertiesPath);
            Properties configurationProps = new Properties();
            configurationProps.load(input);
            String inputPath = configurationProps.getProperty(PARAM_INPUT_DIRECTORY);
            String outputPath = configurationProps.getProperty(PARAM_OUTPUT_DIRECTORY);
            this.byTopic = Boolean.parseBoolean(configurationProps.getProperty(PARAM_BY_TOPIC_BOOLEAN));
            this.percentTrainingSet = Double.parseDouble(configurationProps.getProperty(PARAM_PERCENT_TRAINING_SET));
            this.inputDirectory = new File(inputPath);
            this.outputDirectory = new File(outputPath);
            this.trainingSet = new ArrayList<File>();
            this.testingSet = new ArrayList<File>();
            this.createDirectories();
            if (!inputDirectory.exists() || !inputDirectory.isDirectory()) {
            	throw new ResourceInitializationException();
            }
            this.getAllFiles();
            //this.fullSetSize = this.files.size();
            //this.trainingSetSize = computeTrainingSetSize(this.fullSetSize);
		} catch (Exception e) {
			e.printStackTrace();
			throw new ResourceInitializationException();
		} 
	}
	
	
	/**
	 * 
	 * @throws ResourceInitializationException
	 * @throws IOException
	 */
	public void split() throws ResourceInitializationException, IOException {
		
		// By Topic Split
		if (this.byTopic) {
			System.out.println("Split by Topic");
			int fileLength = this.files.size();
			int trainLength = (int)Math.round(fileLength * this.percentTrainingSet);
			int testLength = fileLength - trainLength;
			File[] trainList = new File[trainLength];
			File[] testList = new File[testLength];
			File[] files = this.files.toArray(new File[fileLength]);
			System.arraycopy(files, 0, trainList, 0, trainLength);
			System.arraycopy(files, trainLength, testList, 0, testLength);
			System.out.println("\ntrain " + String.valueOf(trainList.length));
			for (File f : trainList) {
				System.out.print("," + f.getName());
			}
			System.out.println("\ntest " + String.valueOf(testList.length));
			for (File f : testList) {
				System.out.print("," + f.getName());
			}
			System.out.println();
			// Construct training set and test set
			for (File file : trainList) {
				if(file.isDirectory()) {
					this.trainingSet.addAll(this.getAllFilesWithExtensions(file, FILE_EXTENSION));
				}
			}
			for (File file : testList) {
				if(file.isDirectory()) {
					this.testingSet.addAll(this.getAllFilesWithExtensions(file, FILE_EXTENSION));
				}
			}
		}
		
		// Random Split
		else {
			System.out.println("Split by Random");
			ArrayList<File> files = this.getAllFilesWithExtensions(inputDirectory, FILE_EXTENSION);
			int trainLength = (int)Math.round(files.size() * this.percentTrainingSet);
			int testLength = files.size() - trainLength;
			File[] trainList = new File[trainLength];
			File[] testList = new File[testLength];
			System.arraycopy(files.toArray(), 0, trainList, 0, trainLength);
			System.arraycopy(files.toArray(), trainLength, testList, 0, testLength);
			this.trainingSet = new ArrayList<File>(Arrays.asList(trainList));
			this.testingSet = new ArrayList<File>(Arrays.asList(testList));
		}

		// Look at the statistics 
		
		AnalysisEngine analysisEngine = this.createAnalysisEngine();
		CAS cas = analysisEngine.newCAS();
		System.out.print("\n\ntraining set: " + Integer.toString(this.countADUType(cas, trainingSet, "conclusion")) + " conclusion, " +
				Integer.toString(this.countADUType(cas, trainingSet, "premise")) + " premise");
		System.out.println("\ntesting set: " + Integer.toString(this.countADUType(cas, testingSet, "conclusion")) + " conclusion, " +
				Integer.toString(this.countADUType(cas, testingSet, "premise")) + " premise");
		
		// Copying ... 
		this.copyAll(trainingSet, this.trainingSetDirectory);
		this.copyAll(testingSet, this.testSetDirectory);
	
	}
	
	public ArrayList<File> getAllFilesWithExtensions(File dir, String extension) {
		ArrayList<File> allFiles = new ArrayList<File>();
		File[] files = dir.listFiles();
		for (File file : files) {
			if (file.isDirectory()) {
				allFiles.addAll(getAllFilesWithExtensions(file, extension));
			} else {
				if(this.checkExtension(file, extension)) {
					allFiles.add(file);
				}
			}
		}
		return allFiles;
	}

	
    private boolean checkExtension(File file, String matchingExtension) {
        String extension = "";
        if (file != null && file.exists()) {
            String name = file.getName();
            extension = name.substring(name.lastIndexOf("."));
            if(extension.contentEquals(matchingExtension)) {
            	return true;
            }
        }
        return false;
    }
	
	private int countADUType(CAS cas, List<File> files, String matchType) {
		int count = 0;
		for (File file : files) {
	    	try (FileInputStream is = new FileInputStream(file);){
	    		cas.reset();
				XmiCasDeserializer.deserialize(is, cas);
				JCas jcas = cas.getJCas();
				Annotation span = new Annotation(jcas, 0, jcas.getDocumentText().length() + 1);
				//TODO specify annotation and classes by property file
				FSIterator<Annotation> iter = 
						jcas.getAnnotationIndex(ArgumentativeDiscourseUnit.type).subiterator(span);
				ArgumentativeDiscourseUnit unit = (ArgumentativeDiscourseUnit) iter.get();
				String type = unit.getUnitType();
				if (type.equals(matchType)) {
					count++;
				}
			} catch (Exception e) {
				e.printStackTrace();
			} 
		}
		return count;
	}
	/**
	 * 
	 * @param instancesConclusions
	 * @param destinationDirectory
	 * @throws IOException
	 */
	private void copyAll(ArrayList<File> instances, File destinationDirectory) throws IOException {
		// Clean the destination folder
		FileUtils.deleteAllFiles(destinationDirectory); 
		for (File instance : instances) {
			this.copy(instance, destinationDirectory);
		}
	}
	
	
	/**
	 * 
	 * @param indices
	 * @param instances
	 * @param inputDirectory
	 * @param outputDirectory
	 * @throws IOException
	 */
	private void copy(File instance, File outputDirectory) throws IOException {
		String fileName = instance.getName();
		File inputDirectory = new File(instance.getParent());
		Path copied = Paths.get(outputDirectory.getAbsolutePath() + "/" + fileName);
		Path original = Paths.get(inputDirectory.getAbsolutePath() + "/" + fileName);
		Files.copy(original, copied, StandardCopyOption.REPLACE_EXISTING);
	}
	
	/**
	 * 
	 */
	private void getAllFiles() {
		this.files = new ArrayList<File>();
		for (File file : this.inputDirectory.listFiles()) {
//			System.out.println(file.getName());
			this.files.add(file);
		}
	}
	
	
	/**
	 * 
	 * @throws IOException
	 */
	private void createDirectories() throws IOException {
		File outputDirectory = this.outputDirectory;
		File trainingDirectory = new File(outputDirectory.getAbsolutePath() + "/training");
		File testDirectory = new File(outputDirectory.getAbsolutePath() + "/test");
		if (!outputDirectory.exists()) {
			outputDirectory.mkdirs();
		}
		if (trainingDirectory.exists()) {
			this.emptyDirectory(trainingDirectory);
		} else {
			trainingDirectory.mkdirs();
		}
		if (testDirectory.exists()) {
			this.emptyDirectory(testDirectory);
		} else {
			testDirectory.mkdirs();
		}
		
		this.trainingSetDirectory = trainingDirectory;
		this.testSetDirectory = testDirectory;
		
	}
	
	
	/**
	 * 
	 * @param directory
	 * @throws IOException
	 */
	private void emptyDirectory(File directory) throws IOException {
		
		for (File file : directory.listFiles()) {
			if (file.isFile()) {
				if (!file.delete()) throw new IOException();
			} else {
				this.emptyDirectory(file);
				if (!file.delete()) throw new IOException();
			}
			
		}
	}
	
	
	
	/*
	 * Creates an analysis engine.
	 * 
	 * @param aePath the path of the anlyis engine
	 * @return the analysis engine
	 */
	private AnalysisEngine createAnalysisEngine() {
		String aePath = "../aitools4-ie-uima/conf/uima-descriptors/primitive-AEs/template/DummyAnalysisEngine.xml";
		AnalysisEngine analysisEngine = null;
		try {
			XMLInputSource xmlInputSource = new XMLInputSource(aePath);
			ResourceSpecifier specifier = UIMAFramework.getXMLParser().parseResourceSpecifier(xmlInputSource);
			analysisEngine = UIMAFramework.produceAnalysisEngine(specifier);
			analysisEngine.reconfigure();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return analysisEngine;
	}
	
	
	
	public static void main(String[] args) throws ResourceInitializationException, IOException {
	
		TrainTestSplitter splitter = new TrainTestSplitter();
		splitter.split();
	}
}
