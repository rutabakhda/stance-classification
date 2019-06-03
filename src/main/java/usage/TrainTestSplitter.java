package usage;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Array;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Properties;
import java.util.Random;

import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.FSIterator;
import org.apache.uima.cas.impl.XmiCasDeserializer;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;
import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;

import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;

/**
 * 
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class TrainTestSplitter {
	
	
	private static final String PROPERTIES_PATH = "src/main/resources/properties/split/split_debatepedia-test.properties";
	
	
	private static final String PARAM_INPUT_DIRECTORY = "input_directory";
	
	private static final String PARAM_OUTPUT_DIRECTORY = "output_directory";
	
	private static final String PARAM_PERCENT_TRAINING_SET = "percent_training_set";
	
	//private static final String PARAM_ANNOTATION_TYPE = "annotation_type";
	
	//private static final String PARAM_ANNOTATION_FEATURE_TYPE = "annotation_feature_type";
	
	//private static final String PARAM_CLASS_1_ANNOTATION_FEATURE_VALUE = "class_1_annotation_feature_value";
	
	//private static final String PARAM_CLASS_2_ANNOTATION_FEATURE_VALUE = "class_2_annotation_feature_value";
	
	
	private static final String FILE_EXTENSION = ".xmi";
	
	
	private File inputDirectory;

	private File outputDirectory;
	
	private double percentTrainingSet;
	
	private int fullSetSize;
	
	private int trainingSetSize;
	
	private File trainingSetDirectory;
	
	private File testSetDirectory;
	
	private ArrayList<File> files;
	
	
	
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
            this.percentTrainingSet = Double.parseDouble(configurationProps.getProperty(PARAM_PERCENT_TRAINING_SET));
            this.inputDirectory = new File(inputPath);
            this.outputDirectory = new File(outputPath);
            this.createDirectories();
            if (!inputDirectory.exists() || !inputDirectory.isDirectory()) {
            	throw new ResourceInitializationException();
            }
            this.getAllFiles();
            this.fullSetSize = this.files.size();
            this.trainingSetSize = computeTrainingSetSize(this.fullSetSize);
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
		AnalysisEngine analysisEngine = this.createAnalysisEngine();
	
		ArrayList<File> instancesConclusions = new ArrayList<File>();
		ArrayList<File> instancesPremises = new ArrayList<File>();
		CAS cas = analysisEngine.newCAS();
		for (File file : this.files) {
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
				System.out.println(file.getName());
				if (type.equals("conclusion")) {
					instancesConclusions.add(file);
				} else if (type.equals("premise")) {
					instancesPremises.add(file);
				} else {
					System.out.println("No conclusion or premise at file " + file.getAbsolutePath());
				}
			} catch (Exception e) {
				e.printStackTrace();
			} 
		}
		this.copyAll(instancesConclusions, instancesPremises);
	}
	
	
	/**
	 * 
	 * @param instancesConclusions
	 * @param instancesPremises
	 * @throws IOException
	 */
	private void copyAll(ArrayList<File> instancesConclusions, ArrayList<File> instancesPremises) throws IOException {
		
		Random randomGenerator = new Random(123456789);
		ArrayList<Integer> indices = new ArrayList<Integer>();
		int numTrainingConclusions = (int)(this.percentTrainingSet * instancesConclusions.size());
		int numTrainingPremises = this.trainingSetSize - numTrainingConclusions;
		
		this.sampleIndices(instancesConclusions.size(), numTrainingConclusions, indices, randomGenerator);
		this.copy(indices, instancesConclusions, this.inputDirectory, this.trainingSetDirectory);
		indices.clear();
		this.sampleIndices(instancesPremises.size(), numTrainingPremises, indices, randomGenerator);
		this.copy(indices, instancesPremises, this.inputDirectory, this.trainingSetDirectory);
		this.copy(instancesConclusions, this.inputDirectory, this.testSetDirectory);
		this.copy(instancesPremises, this.inputDirectory, this.testSetDirectory);
	}
	
	
	/**
	 * 
	 * @param indices
	 * @param instances
	 * @param inputDirectory
	 * @param outputDirectory
	 * @throws IOException
	 */
	private void copy(ArrayList<Integer> indices, ArrayList<File> instances, File inputDirectory, File outputDirectory) throws IOException {
		Collections.sort(indices, Collections.reverseOrder());
		for (int i : indices) {
			File file = instances.remove(i);
			String fileName = file.getName();
		    Path copied = Paths.get(outputDirectory.getAbsolutePath() + "/" + fileName);
		    Path original = Paths.get(inputDirectory.getAbsolutePath() + "/" + fileName);
		    Files.copy(original, copied, StandardCopyOption.REPLACE_EXISTING);
		}
	}
	
	
	/**
	 * 
	 * @param instances
	 * @param inputDirectory
	 * @param outputDirectory
	 * @throws IOException
	 */
	private void copy(ArrayList<File> instances, File inputDirectory, File outputDirectory) throws IOException {
		for (File file : instances) {
			String fileName = file.getName();
		    Path copied = Paths.get(outputDirectory.getAbsolutePath() + "/" + fileName);
		    Path original = Paths.get(inputDirectory.getAbsolutePath() + "/" + fileName);
		    Files.copy(original, copied, StandardCopyOption.REPLACE_EXISTING);
		}
	}
	
	
	/**
	 * 
	 * @param range
	 * @param numIndices
	 * @param indices
	 * @param randomGenerator
	 */
	private void sampleIndices(int range, int numIndices, ArrayList<Integer> indices, Random randomGenerator) {
		for (int i = 0; i < numIndices; i++) {
			int rand = randomGenerator.nextInt(range);
			while (indices.contains(new Integer(rand))) {
				rand = randomGenerator.nextInt(range);
			}
			indices.add(new Integer(rand));
		}
	}
	
	
	/**
	 * 
	 */
	private void getAllFiles() {
		this.files = new ArrayList<File>();
		for (File file : this.inputDirectory.listFiles()) {
			if (file.getAbsolutePath().indexOf(FILE_EXTENSION) == file.getAbsolutePath().length() - 4) {
				files.add(file);
			}
		}
	}
	
	
	/**
	 * 
	 * @param fileCount
	 * @return
	 */
	private int computeTrainingSetSize(int fileCount) {
		int trainingSetSize = (int)(fileCount * percentTrainingSet);
		return trainingSetSize;
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
