package usage;


/**
 * 
 * Implements the uima annotation pipeline used for the debatepedia corpus.
 * @author lukas.peter.trautner@uni-weimar.de
 * 
 */
public class DebatepediaProcessingPipeline {
	
	//TODO
	/**
	private static final String INPUT_COLLECTION_DIR = 
			"data/demo/webis-debate-16";
	
	private static final String COLLECTION_READER_PATH = 
			"../aitools4-ie-uima/conf/uima-descriptors/collection-readers/UIMAPlainTextReader.xml";
	
	private static final String ANALYSIS_ENGINE_PATH = 
			"src/main/resources/uima/aggregates/PosTokenTagger.xml";

	private static final String OUTPUT_COLLECTION_DIR = 
			"data/demo/processed/webis-debate-16";
	
	
	
	
	
	private void processCollection() {
		//CollectionReader collectionReader = this.createCollectionReader(COLLECTION_READER_PATH, INPUT_COLLECTION_DIR);
		//AnalysisEngine analysisEngine = this.createAnalysisEngine(ANALYSIS_ENGINE_PATH);
		
		File inputFile = new File("/home/weci2587/claim-detection/json/idebate.json");
		try {
			
			JsonFactory jsonFac = new JsonFactory();
			JsonParser parser = jsonFac.createParser(inputFile);
			
			
			
			
			
		
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		//collectionReader.destroy();
		//analysisEngine.destroy();
	}
	
	
	
	private CollectionReader createCollectionReader(String crPath, String inputDir) {
		
		CollectionReader collectionReader = null;
		try {
			XMLInputSource xmlInputSource = new XMLInputSource(crPath);
			ResourceSpecifier specifier = UIMAFramework.getXMLParser().parseResourceSpecifier(xmlInputSource);
			collectionReader = UIMAFramework.produceCollectionReader(specifier);
			collectionReader.setConfigParameterValue("InputDirectory", inputDir);
			collectionReader.setConfigParameterValue("IncludeSubdirectories", true);
			collectionReader.reconfigure();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return collectionReader;
	}
	
	
	
	private AnalysisEngine createAnalysisEngine (String aePath) {
		
		AnalysisEngine analysisEngine = null;
		try {
			XMLInputSource xmlInputSource = new XMLInputSource(aePath);
			ResourceSpecifier specifier = UIMAFramework.getXMLParser().parseResourceSpecifier(xmlInputSource);
			analysisEngine = UIMAFramework.produceAnalysisEngine(specifier);
			analysisEngine.reconfigure();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return analysisEngine;
	}

		
		
	public static void main(String[] args) {
		DebatepediaProcessingPipeline pipeline = new DebatepediaProcessingPipeline();
		pipeline.processCollection();
	}
	*/

}
