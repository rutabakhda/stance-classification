package usage;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.impl.XmiCasSerializer;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;
import org.json.JSONArray;
import org.json.JSONObject;

import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;

/**
 * 
 * Implements the uima annotation pipeline used for the debatepedia corpus.
 * @author lukas.peter.trautner@uni-weimar.de
 * 
 */
public class DebatepediaProcessingPipeline {
	
	private static final String INPUT_COLLECTION_DIR = 
			"data/debatepedia/json";
	
	private static final String ANALYSIS_ENGINE_PATH = 
			"src/main/resources/uima/aggregates/PosTokenTagger.xml";

	private static final String OUTPUT_COLLECTION_DIR = 
			"data/debatepedia/xmi";
	
	private static final Pattern JSON = Pattern.compile(".json$");
	
	
	/**
	 *  TODO java documentation
	 */
	private void processCollection() {
		
		AnalysisEngine analysisEngine = this.createAnalysisEngine(ANALYSIS_ENGINE_PATH);
		
		File inputDirectory = new File(INPUT_COLLECTION_DIR);
		
		if (!inputDirectory.isDirectory()) {
			throw new RuntimeException();
		}
		
		
		for (File inputFile : inputDirectory.listFiles()) {
			
			String fileName = inputFile.getName();
			Matcher fileMatcher = JSON.matcher(fileName);
			
			if (!fileMatcher.find()) {
				continue;
			}
			
			String json = this.readJsonFile(inputFile);
			
			if (!json.equals("")) {
				try {
					JSONArray argumentativeDiscourseUnits = new JSONArray(json);
					File outputDirectory = this.createOutputDirectory(fileName);
					
					for (int i = 0; i < argumentativeDiscourseUnits.length(); i++) {
						CAS cas = analysisEngine.newCAS();
						JCas jcas = cas.getJCas();
						
						JSONObject argumentativeDiscourseUnit = argumentativeDiscourseUnits.getJSONObject(i);
						String type = argumentativeDiscourseUnit.getString("unitType");
						String content = argumentativeDiscourseUnit.getString("content");
						
						jcas.setDocumentText(content);
						jcas.setDocumentLanguage("english");
						ArgumentativeDiscourseUnit unit = new ArgumentativeDiscourseUnit(jcas, 0, jcas.getDocumentText().length());
						unit.setUnitType(type);
						unit.addToIndexes(jcas);
						analysisEngine.process(jcas);
						
						File outputFile = new File(outputDirectory.getAbsolutePath() + "/debatepedia-adu-" + Integer.toString(i) + ".xmi");
						FileOutputStream outputStream = new FileOutputStream(outputFile);
						XmiCasSerializer.serialize(jcas.getCas(), outputStream);
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
	
			} else {
				continue;
			}
		}
	}
	

	/**
	 * TODO java documentation
	 * 
	 * @param inputFile
	 * @return
	 */
	private String readJsonFile(File inputFile) {
		String content = "";
		try {  
			BufferedReader reader = new BufferedReader(new FileReader(inputFile));
			String line = reader.readLine();
			while (line != null) {
				content = content + line;
				line = reader.readLine();
			}
			reader.close();
		} catch (Exception e) {
			throw new RuntimeException();
		}
		return content;
	}
	
	
	/**
	 * 
	 * TODO java documentation
	 * 
	 * @param fileName
	 * @return
	 */
	private File createOutputDirectory(String fileName) {
		String outputDirName = fileName.replace(".json", "");
		File outputDir = new File(OUTPUT_COLLECTION_DIR + "/" + outputDirName);
		if (!(outputDir.exists() || outputDir.mkdirs())) throw new RuntimeException();
		return outputDir;
	}
	
	
	/**
	 * Creates an analysis engine.
	 * @param aePath the path of the anlyis engine
	 * @return the analysis engine
	 */
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
	

}
