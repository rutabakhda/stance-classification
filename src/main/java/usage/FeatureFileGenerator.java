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
		String propertiesPath;
		if (args.length>=1 && args[0].length()>10) {//TODO: bugs in the length comparison, put 10 at the moment
			propertiesPath = args[0];
		} else {
			propertiesPath = PROPERTIES_PATH;
		}
		new GenericFeatureFileGenerator(propertiesPath).generatorFeatureFiles();
	}
	
}
