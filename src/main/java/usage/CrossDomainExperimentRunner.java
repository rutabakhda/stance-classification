package usage;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import org.apache.uima.resource.ResourceInitializationException;
import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

public class CrossDomainExperimentRunner {
	
	private static final String[] FEATURE_TYPES = { "content-length_pos-ngrams_token-ngrams",
													//"content-length_pos-ngrams",
													//"content-length_token-ngrams",
													//"pos-ngrams_token-ngrams",
													//"content-length",
													//"pos-ngrams",
													//"token-ngrams"
	};
	
	private static final String PROPERTIES_FEATURE_GENERATOR_PATH = "src/main/resources/properties/feature_file_generator/cross-domain/";
	
	private static final String FEATURE_FILE_PATH = "data/cross-domain/debatepedia_sample-sbm/arff/";
	
	private static final String CORPUS1 = "debatepedia";
	
	private static final String CORPUS2 = "sample-sbm";
	
	
	private ArrayList<String> featureGeneratorPropertiesPaths;
	private DebatepediaProcessor processor1;
	private DebatepediaProcessor processor2;
	
	public CrossDomainExperimentRunner() throws ResourceInitializationException, IOException {
		
		this.featureGeneratorPropertiesPaths = new ArrayList<String>();
		
			for (String featureType : FEATURE_TYPES){
				String featureGeneratorPropertiesPath = PROPERTIES_FEATURE_GENERATOR_PATH + featureType + ".properties";
				this.featureGeneratorPropertiesPaths.add(featureGeneratorPropertiesPath);
			}
		
	}
	
	
	public void run(){
		
		// Process sample statement by member data
		String inputPath1 = "data/debatepedia/json/full";
		String outputPath1 = "data/debatepedia/processed/";
		String[] args1 = {inputPath1, outputPath1};
		this.processor1 = new DebatepediaProcessor();
//        this.processor1.processCollection(args1);
				
		// Process sample statement by member data
		String inputPath2 = "data/sample-sbm/json/";
		String outputPath2 = "data/sample-sbm/processed/";
		String[] args2 = {inputPath2, outputPath2};
		this.processor2 = new DebatepediaProcessor();
//		this.processor2.processCollection(args);
		
		// Generate feature files
//		for (String propertiesPath : this.featureGeneratorPropertiesPaths) {
//			generator = new GenericFeatureFileGenerator(propertiesPath);
//			generator.generatorFeatureFiles();
//		} 
		
		// Search for training file
		String extension = ".arff";
		File featureFileFolder = new File(FEATURE_FILE_PATH);
		String[] trainingFilePatterns = {FEATURE_TYPES[0], CORPUS1};
		String trainingFeaturesPath = this.listFilesMatchingPatternNewest(featureFileFolder, trainingFilePatterns, extension)[0].getAbsolutePath();
		String[] testingFilePatterns = {FEATURE_TYPES[0], CORPUS2};
		String testingFeaturesPath = this.listFilesMatchingPatternNewest(featureFileFolder, testingFilePatterns, extension)[0].getAbsolutePath();
		
		
		try {
			WekaClassifierManager.classify(trainingFeaturesPath, testingFeaturesPath);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	// Get the list of files (newest to oldest) that satisfies the patterns
		private File[] listFilesMatchingPatternNewest(File folder, String[] patterns, String extension) {
			File[] files = folder.listFiles(new FilenameFilter(){
		        @Override
		        public boolean accept(File dir, String name) {
		        	System.out.println(name);
		        	boolean shouldAccept = false;
		        	if(name.endsWith(extension)) {
		        		for(String pattern : patterns) {
		        			if(!name.contains(pattern)) {
		        				shouldAccept = false;
		        				break;
		        			}
		        			else {
		        				shouldAccept = true;
		        				continue;
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
	
	public static void main(String[] args) throws ResourceInitializationException, IOException{
		CrossDomainExperimentRunner runner = new CrossDomainExperimentRunner();
		runner.run();
		
	}
}