package usage;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.CASException;
import org.apache.uima.cas.impl.XmiCasSerializer;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;
import org.json.JSONArray;
import org.json.JSONObject;

import com.github.javaparser.ast.expr.ThisExpr;

import de.aitools.ie.uima.io.UIMAAnnotationFileWriter;
import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;

/**
 * 
 * Implements the uima annotation pipeline used for the debatepedia corpus.
 * 
 * @author lukas.peter.trautner@uni-weimar.de
 * 
 */
public class DebatepediaProcessor {

	private static final String INPUT_COLLECTION_DIR = "data/debatepedia/json/full";

	private static final String ANALYSIS_ENGINE_PATH = "src/main/resources/uima/aggregates/PosTokenTagger.xml";

	private static final String OUTPUT_COLLECTION_DIR = "data/debatepedia/processed/";

	private static final Pattern JSON = Pattern.compile(".json$");
	
	private static final String STATISTIC_PATH = "output/debatepedia/statistics.txt";
	private static final String TOPICS_PATH = "output/debatepedia/topics.txt";

	private File inputDirectory;
	private File outputDirectory;

	/**
	 * TODO java documentation
	 * 
	 * @param args
	 */
	public void processCollection(String[] args) {
		// Initialize output file writer
		UIMAAnnotationFileWriter xmiWriter = new UIMAAnnotationFileWriter();

		AnalysisEngine analysisEngine = this.createAnalysisEngine(ANALYSIS_ENGINE_PATH);
		
		// Create input and output directory from arguments
		List<String> allTopics = new ArrayList<String>();
		Integer numberOfDocumentCounter = 0;
		Integer numberOfTopicCounter = 0;
		Integer numberOfInstanceCounter = 0;
		Integer premiseCounter = 0;
		Integer conclusionCounter = 0; 
		
		if (args != null && args.length > 0 && args[0].length() > 0) {
			this.inputDirectory = new File(args[0]);
		} else {
			this.inputDirectory = new File(INPUT_COLLECTION_DIR);
		}
		if (!this.inputDirectory.isDirectory()) {
			throw new RuntimeException();
		}
		System.out.println("input directory: " + this.inputDirectory.getAbsolutePath());
		
		if (args != null && args.length > 1 && args[1].length() > 0) {
			this.outputDirectory= new File(args[1]);
		} else {
			this.outputDirectory = new File(OUTPUT_COLLECTION_DIR);
		}
		if (!this.outputDirectory.isDirectory()) {
			throw new RuntimeException();
		}
		System.out.println("output directory: " + this.outputDirectory.getAbsolutePath());
		

		for (File inputFile : this.inputDirectory.listFiles()) {

			String fileName = inputFile.getName();
			System.out.println("filename: " + fileName);
			Matcher fileMatcher = JSON.matcher(fileName);

			if (!fileMatcher.find()) {
				continue;
			}

			String json = this.readJsonFile(inputFile);

			if (!json.equals("")) {
				try {
					JSONArray argumentativeDiscourseUnits = new JSONArray(json);

					int count = 0;
					for (int i = 0; i < argumentativeDiscourseUnits.length(); i++) {
						numberOfDocumentCounter++;
						
						JSONObject argumentativeDiscourseUnit = argumentativeDiscourseUnits.getJSONObject(i);
						String type = argumentativeDiscourseUnit.getString("unitType");

						String content = argumentativeDiscourseUnit.getString("content");
						
						// topic
						String topic = argumentativeDiscourseUnit.getString("topic");
						Integer topicIndex;
						if (!allTopics.contains(topic)) {
							allTopics.add(topic);
							numberOfTopicCounter++;
						}
						topicIndex = allTopics.indexOf(topic);
						
						if(type.contentEquals("premise")) {
							premiseCounter++;
						}
						else if (type.contentEquals("conclusion")) {
							conclusionCounter++;
						}
//						XmiCasSerializer.serialize(jcas.getCas(), outputStream);
						// Some prints
						write2XMI(analysisEngine, xmiWriter, type, content, topicIndex, ++numberOfInstanceCounter);
						
						count++;
						if (count % 100 == 0) {
							System.out.print(".");
						}
					}
				} catch (Exception e) {
					e.printStackTrace();
				}

			} else {
				continue;
			}
		}
		try {
			writeStatisticToFile(conclusionCounter, premiseCounter, numberOfDocumentCounter, numberOfTopicCounter, STATISTIC_PATH);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			writeTopicsToFile(allTopics, TOPICS_PATH);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	

	private void writeStatisticToFile(Integer conclusionCounter, Integer premiseCounter, 
			Integer numberOfDocumentCounter, Integer numberOfTopicCounter, String pathToFile)
			throws IOException {
		File fout = new File(pathToFile);
		
		fout.getParentFile().mkdirs();
		fout.createNewFile(); // if file already exists will do nothing

		FileOutputStream fosFileOutputStream = new FileOutputStream(fout, false);

		BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(fosFileOutputStream));
		bufferedWriter.write("documents:" + String.valueOf(numberOfDocumentCounter));
		bufferedWriter.newLine();
		bufferedWriter.write("topics:" + String.valueOf(numberOfTopicCounter));
		bufferedWriter.newLine();
		bufferedWriter.write("premise:" + String.valueOf(premiseCounter));
		bufferedWriter.newLine();
		bufferedWriter.write("conclusion:" + String.valueOf(conclusionCounter));
		bufferedWriter.newLine();

		bufferedWriter.close();

	}

	private void writeTopicsToFile(List<String> allTopics, String pathToFile) throws IOException {
		File fout = new File(pathToFile);
		
		fout.getParentFile().mkdirs();
		fout.createNewFile(); // if file already exists will do nothing

		FileOutputStream fosFileOutputStream = new FileOutputStream(fout, false);

		BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(fosFileOutputStream));
		for (int i = 0; i < allTopics.size(); i++) {
			bufferedWriter.write(allTopics.get(i));
			bufferedWriter.newLine();
		}
		bufferedWriter.close();
	}
	
	
	private void write2XMI(AnalysisEngine ae, UIMAAnnotationFileWriter xmiWriter, String aduType, String sentence,
			Integer topicIndex, Integer aduId)
			throws ResourceInitializationException, CASException, AnalysisEngineProcessException {
		// Create new cas for the sentence
		CAS cas = ae.newCAS();
		cas.setDocumentText(sentence);
		JCas jcas = cas.getJCas();
		// Create ADU and add to count
		ArgumentativeDiscourseUnit au = new ArgumentativeDiscourseUnit(jcas);
		// Set begin and end
		au.setBegin(0);
		au.setEnd(sentence.length() - 1);
		// Set unitType - Conclusion / Premise
		au.setUnitType(aduType);
		au.addToIndexes();
		ae.process(cas);

		String outputDir = this.outputDirectory.getAbsolutePath() + "/" + "topic" + "-" + String.format("%03d", topicIndex) + "/" 
				+ "/";
		// Write sentence with ADU annotation to file
		xmiWriter.write(cas, outputDir, "document-" + String.format("%04d", aduId) + ".txt");
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
	 * Creates an analysis engine.
	 * 
	 * @param aePath the path of the anlyis engine
	 * @return the analysis engine
	 */
	private AnalysisEngine createAnalysisEngine(String aePath) {

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
		DebatepediaProcessor pipeline = new DebatepediaProcessor();
		pipeline.processCollection(args);
		System.out.println("done");
	}

}
