package usage;

import java.io.IOException;

import org.apache.uima.resource.ResourceInitializationException;

import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

/**
 * 
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class DebatepediaExperimentRunner {
	
	private static final String[] EXPERIMENT_PROPERTIES_PATHS = {
			
			"src/main/resources/properties/experiment/debatepedia/experiment-config_debatepedia_content-length-pos-ngrams.properties",
			"src/main/resources/properties/experiment/debatepedia/experiment-config_debatepedia_content-length-pos-token-ngrams.properties",
			"src/main/resources/properties/experiment/debatepedia/experiment-config_debatepedia_content-length-token-ngrams.properties",
			"src/main/resources/properties/experiment/debatepedia/experiment-config_debatepedia_content-length.properties",
			"src/main/resources/properties/experiment/debatepedia/experiment-config_debatepedia_pos-ngrams.properties",
			"src/main/resources/properties/experiment/debatepedia/experiment-config_debatepedia_pos-token-ngrams.properties",
			"src/main/resources/properties/experiment/debatepedia/experiment-config_debatepedia_token-ngrams.properties"
	};
	
	private static final String SPLITTER_PROPERTIES_PATH = "src/main/resources/properties/split/split-config_debatepedia.properties";
	
	private DebatepediaProcessingPipeline pipeline;
	
	private TrainTestSplitter splitter;
	
	private GenericFeatureFileGenerator generator;
	
	//TODO Weka Stuff
	
	
	
	public DebatepediaExperimentRunner() throws ResourceInitializationException, IOException {

		this.pipeline = new DebatepediaProcessingPipeline();
		this.splitter = new TrainTestSplitter(SPLITTER_PROPERTIES_PATH);
		//TODO Weka Stuff
		
	}
	
	
	public void run() throws ResourceInitializationException, IOException {
		
		//this.pipeline.processCollection(null);
		this.splitter.split();
		for (String propertiesPath : EXPERIMENT_PROPERTIES_PATHS) {
			this.generator = new GenericFeatureFileGenerator(propertiesPath);
			this.generator.generatorFeatureFiles();
		}
		//TODO run weka for each generated feature configuration + pipe output of weka to data/debatepedia/experiment-results/<name of input folder>.txt
		
	}

	
	
	public static void main(String[] args) throws ResourceInitializationException, IOException {
		DebatepediaExperimentRunner runner = new DebatepediaExperimentRunner();
		runner.run();
	}
}
