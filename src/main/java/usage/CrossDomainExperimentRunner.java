package usage;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.uima.resource.ResourceInitializationException;

import com.github.javaparser.ast.expr.ThisExpr;

import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

public class CrossDomainExperimentRunner {
	
	private DebatepediaProcessor processor;
	private GenericFeatureFileGenerator generator;
	String[] FEATURE_TYPES = {
			"content-length_pos-ngrams_token-ngrams",
//			"content-length_pos-ngrams",
//			"content-length_token-ngrams",
//			"pos-ngrams_token-ngrams",
//			"content-length",
//			"pos-ngrams",
//			"token-ngrams"
	};
	String PROPERTIES_FEATURE_GENERATOR_PATH = "src/main/resources/properties/feature_file_generator/cross-domain/";
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
        this.processor1.processCollection(args1);
				
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
	}
	
	public static void main(String[] args) throws ResourceInitializationException, IOException{
		CrossDomainExperimentRunner runner = new CrossDomainExperimentRunner();
		runner.run();
		
	}
}