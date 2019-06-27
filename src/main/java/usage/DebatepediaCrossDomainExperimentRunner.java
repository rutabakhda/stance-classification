package usage;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;

import org.apache.uima.resource.ResourceInitializationException;
import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

public class DebatepediaCrossDomainExperimentRunner {
	
	String[] FEATURE_TYPES = {
		"content-length_pos-ngrams_token-ngrams",
		"content-length_pos-ngrams",
		"content-length_token-ngrams",
		"pos-ngrams_token-ngrams",
		"content-length",
		"pos-ngrams",
		"token-ngrams"
	};
	String PROPERTIES_FEATURE_GENERATOR_PATH = "src/main/resources/properties/feature_file_generator/cross-domain/debatepedia_sample-sbm/";
	String FEATURE_FILE_PATH = "data/cross-domain/debatepedia_sample-sbm/arff/";
	String CORPUS1 = "debatepedia";
	String CORPUS2 = "sample-sbm";
	private ArrayList<String> featureGeneratorPropertiesPaths;
	private DebatepediaProcessor processor1;
	private DebatepediaProcessor processor2;
	
	public DebatepediaCrossDomainExperimentRunner() throws ResourceInitializationException, IOException {
		
		this.featureGeneratorPropertiesPaths = new ArrayList<String>();
		
			for (String featureType : FEATURE_TYPES){
				String featureGeneratorPropertiesPath = PROPERTIES_FEATURE_GENERATOR_PATH + featureType + ".properties";
				this.featureGeneratorPropertiesPaths.add(featureGeneratorPropertiesPath);
			}
		
	}
	
	
	public void run() throws Exception{
		
		// Process debatepedia to xmi
		String inputPath1 = "data/debatepedia/json/full";
		String outputPath1 = "data/debatepedia/processed/";
		String[] args1 = {inputPath1, outputPath1};
		this.processor1 = new DebatepediaProcessor();
        //this.processor1.processCollection(args1);
				
		// Process sample statement by member to xmi
		String inputPath2 = "data/sample-sbm/json/";
		String outputPath2 = "data/sample-sbm/processed/";
		String[] args2 = {inputPath2, outputPath2};
		this.processor2 = new DebatepediaProcessor();
		//this.processor2.processCollection(args2);
		
		// Generate feature files for training and testing
		for (String propertiesPath : this.featureGeneratorPropertiesPaths) {
			System.out.println(propertiesPath);
			GenericFeatureFileGenerator generator = new GenericFeatureFileGenerator(propertiesPath);
			generator.generatorFeatureFiles();
		} 
		
		/*
		String extension = ".arff";
		File featureFileFolder = new File(FEATURE_FILE_PATH);
		for (String featureType: FEATURE_TYPES) {
			String trainingFeaturesPath = this.listFilesMatchingPatternNewest(featureFileFolder, featureType, CORPUS1, extension)[0].getAbsolutePath();
			String testingFeaturesPath = this.listFilesMatchingPatternNewest(featureFileFolder, featureType, CORPUS2, extension)[0].getAbsolutePath();
			
			System.out.println("\n\n\nTRAINING ON "+ featureType);
			System.out.println("training file: " + trainingFeaturesPath);
			System.out.println("testing file: "+ testingFeaturesPath);
			WekaClassifierManager.classify(trainingFeaturesPath, testingFeaturesPath);
			System.out.println("===================\n\n\n");
		}
		*/
		
		
	}
	
	private static String getDate() {
		Date date = new Date();
		Timestamp ts = new Timestamp(date.getTime());
		SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
		return formatter.format(ts);
	}
	
	private File[] listFilesMatchingPatternNewest(File folder, String featureType,
			String corpusName, String extension) {
		File[] files = folder.listFiles(new FilenameFilter(){
	        @Override
	        public boolean accept(File dir, String name) {
	        	boolean shouldAccept = false;
	        	if(name.endsWith(extension)) {
	        		if(name.startsWith(featureType+"_2019")) {
	        			shouldAccept = true;
	        			for(String pattern: new String[]{corpusName}) {
	        				if (!name.contains(pattern)) {
	        					shouldAccept = false;
	        					break;
	        				}
	        				else {
	        					continue;
	        				}
	        			}
	        		}
	        		
	        	}
	            return shouldAccept; 
	        }}
		);
		
	
		Arrays.sort(files, new Comparator<File>() {
		    public int compare(File f1, File f2) {
		        return Long.compare(f1.lastModified(), f2.lastModified());
		    }
		});
		return files;
	}
	
	public static void main(String[] args) throws Exception{
		DebatepediaCrossDomainExperimentRunner runner = new DebatepediaCrossDomainExperimentRunner();
		runner.run();
		
	}
}