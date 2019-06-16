package usage;


import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

/**
 * 
 * Imports the GenericFeatureFileGenerator from the aitools4-ie-uima library.
 * Creates features based on the specified experiment properties file.
 * @author lukas.peter.trautner@uni-weimar.de
 * 
 */
public class FeatureFileGenerator {
	
	public static final String[] PROPERTY_PATHS = {
			
			"src/main/resources/properties/experiment/experiment-config_debatepedia_statistics.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			//"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			
			/**
			"src/main/resources/properties/experiment/experiment-config_student-essays_statistics.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_position.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_lemma-ngrams.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_length.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_token-ngrams.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_pos-ngrams.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_pos-token-ngrams.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_pos-lemma-ngrams.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_position-pos-lemma-ngrams.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_position-length-pos-lemma-ngrams.properties",
			*/
	};
	
	
	public static void main(String[] args) {
		
		for (String path : PROPERTY_PATHS) {
			
		
		
		
		    	Thread thread = new Thread(() -> {
		    		new GenericFeatureFileGenerator(path).generatorFeatureFiles();
		    	});
		    	thread.start();
		}
	}
	
}
