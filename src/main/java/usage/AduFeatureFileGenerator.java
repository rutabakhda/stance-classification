package usage;

import de.aitools.ie.uima.usage.GenericFeatureFileGenerator;

public class AduFeatureFileGenerator {
	
	public static final String PROPERTIES_PATH = "src/main/resources/properties/aduArffGenerator.properties";
	
	
	public static void main(String[] args) {
		
		new GenericFeatureFileGenerator(PROPERTIES_PATH).generatorFeatureFiles();
	}
	
}
