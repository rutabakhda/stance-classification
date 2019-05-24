package usage;

import java.io.File;
import java.io.FileOutputStream;
import java.util.regex.Matcher;

import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.impl.XmiCasSerializer;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParser;

import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;

@SuppressWarnings("unused")
public class JsonProcessingPipeline {
	
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
		JsonProcessingPipeline pipeline = new JsonProcessingPipeline();
		pipeline.processCollection();
	}

}
