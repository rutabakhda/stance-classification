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
			
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			"src/main/resources/properties/experiment/experiment-config_debatepedia_.properties",
			
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			"src/main/resources/properties/experiment/experiment-config_student-essays_.properties",
			
			
	};
	
	
	public static void main(String[] args) {
		
		for (String path : PROPERTY_PATHS)
			new GenericFeatureFileGenerator(path).generatorFeatureFiles();
	}
	
}
