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
	
	//public static final String PROPERTIES_PATH = "src/main/resources/properties/experiment/experiment-config_webis-debate-16.properties";
	public static final String PROPERTIES_PATH = "src/main/resources/properties/experiment/experiment-config_debatepedia.properties";
	
	
	public static void main(String[] args) {
		
		new GenericFeatureFileGenerator(PROPERTIES_PATH).generatorFeatureFiles();
	}
	
}
