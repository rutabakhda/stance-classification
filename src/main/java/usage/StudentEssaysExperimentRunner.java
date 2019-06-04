package usage;

import java.io.IOException;

import org.apache.uima.resource.ResourceInitializationException;

import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

/**
 * 
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class StudentEssaysExperimentRunner {
	
	private static final String[] EXPERIMENT_PROPERTIES_PATHS = {
			
			"src/main/resources/properties/experiment/student_essays/experiment-config_student-essays_content-length-pos-ngrams.properties",
			"src/main/resources/properties/experiment/student_essays/experiment-config_student-essays_content-length-pos-token-ngrams.properties",
			"src/main/resources/properties/experiment/student_essays/experiment-config_student-essays_content-length-token-ngrams.properties",
			"src/main/resources/properties/experiment/student_essays/experiment-config_student-essays_content-length.properties",
			"src/main/resources/properties/experiment/student_essays/experiment-config_student-essays_pos-ngrams.properties",
			"src/main/resources/properties/experiment/student_essays/experiment-config_student-essays_pos-token-ngrams.properties",
			"src/main/resources/properties/experiment/student_essays/experiment-config_student-essays_token-ngrams.properties"
	};
	
	private static final String SPLITTER_PROPERTIES_PATH = "src/main/resources/properties/split/split-config_student-essays.properties";
	
	private StudentEssaysProcessingPipeline pipeline;
	
	private TrainTestSplitter splitter;
	
	private GenericFeatureFileGenerator generator;
	
	//TODO Weka Stuff
	
	
	
	public StudentEssaysExperimentRunner() throws ResourceInitializationException, IOException {

		this.pipeline = new StudentEssaysProcessingPipeline();
		this.splitter = new TrainTestSplitter(SPLITTER_PROPERTIES_PATH);
		//TODO Weka Stuff
		
	}
	
	
	public void run() throws ResourceInitializationException, IOException {
		
		this.pipeline.processCollection();
		this.splitter.split();
		for (String propertiesPath : EXPERIMENT_PROPERTIES_PATHS) {
			this.generator = new GenericFeatureFileGenerator(propertiesPath);
			this.generator.generatorFeatureFiles();
		}
		//TODO run weka
		
	}

	
	
	public static void main(String[] args) throws ResourceInitializationException, IOException {
		StudentEssaysExperimentRunner runner = new StudentEssaysExperimentRunner();
		runner.run();
	}
}
