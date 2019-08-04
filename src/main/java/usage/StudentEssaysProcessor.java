package usage;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.CASException;
import org.apache.uima.cas.FSIterator;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;
import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;

import de.aitools.ie.uima.io.UIMAAnnotationFileWriter;
import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;
import de.aitools.ie.uima.type.argumentation.MetadataAAE;

/**
 * 
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class StudentEssaysProcessor {

	private static final String INPUT_COLLECTION_DIR = "data/student-essays/original/";

	private static final String ANALYSIS_ENGINE_PATH = "src/main/resources/uima/aggregates/PosTokenTagger.xml";

	private static final String OUTPUT_COLLECTION_DIR = "data/student-essays/processed/";

	private static final String COLLECTION_READER_PATH = "../aitools4-ie-uima/conf/uima-descriptors/collection-readers/" + "UIMAAnnotationFileReader.xml";
	
	private static final String STATISTIC_PATH = "output/student-essays/statistics.txt";
	
	private static final String TOPICS_PATH = "output/student-essays/topics.txt";

	// -------------------------------------------------------------------------
	// PROCESSING
	// -------------------------------------------------------------------------

	/**
	 * Main processing method
	 * 
	 * @throws IOException
	 */
	public void processCollection() throws IOException {

		// Statistics
		// Number of documents
		// Number of majorclaim / claim-for / premise / claim-against => number of
		// premise / conclusion
		// Number of topics

		// Information to Extract
		// Argument Discourse Unit - id / content / unittype

		// Output
		// Topics - write to file
		// Statistics - write to file

		// Output folder structure
		// topic-index > essay-index
		// adu-xmi-id
		
		// Initialize UIMA engines
		CollectionReader cr = this.createCollectionReader(COLLECTION_READER_PATH, INPUT_COLLECTION_DIR);
		AnalysisEngine ae = this.createAnalysisEngine(ANALYSIS_ENGINE_PATH);
		// Initialize output file writer
		UIMAAnnotationFileWriter xmiWriter = new UIMAAnnotationFileWriter();
		List<String> allTopics = new ArrayList<String>();
		Integer majorClaimCounter = 0;
		Integer claimForCounter = 0;
		Integer premiseCounter = 0;
		Integer claimAgainstCounter = 0;
		Integer numberOfDocumentCounter = 0;
		Integer numberOfTopicCounter = 0;
		Integer numberOfInstanceCounter = 0;

		// Iterate with collection reader over collection and process each text
		// with analysis engine
		System.out.println("Processing collection...");
		try {
			// Create CAS object only once to avoid memory overhead
			CAS aCAS = ae.newCAS();

			// Stepwise process each text managed by the collection reader
			while (cr.hasNext()) {
				// Store current text in JCas object
				cr.getNext(aCAS);
				JCas jcas = aCAS.getJCas();
				// Increment document counter
				numberOfDocumentCounter++;

				// Iterate over sentences
				FSIterator<Annotation> iter = jcas.getAnnotationIndex(ArgumentativeDiscourseUnit.type).iterator();
				AnnotationIndex<Annotation> annotationIndex = jcas.getAnnotationIndex(MetadataAAE.type);

				MetadataAAE metadataAAE = (MetadataAAE) annotationIndex.iterator().next();
				String topic = metadataAAE.getTopic();
				Integer topicIndex;
				if (!allTopics.contains(topic)) {
					allTopics.add(topic);
					numberOfTopicCounter++;
				}
				topicIndex = allTopics.indexOf(topic);
				String filename = metadataAAE.getFilename();
//				String side = metadataAAE.getTwoSided();

				while (iter.hasNext()) {
					ArgumentativeDiscourseUnit adu = (ArgumentativeDiscourseUnit)iter.next();

					String sentence = adu.getCoveredText();
					String aduType = adu.getUnitType();

					// unit type to only premise and conclusion
					if (aduType.contentEquals("premise")) {
						premiseCounter++;
					} else {
						if (aduType.contentEquals("majorclaim")) {
							majorClaimCounter++;
							aduType = "conclusion";
						} else if (aduType.contentEquals("claim-for")) {
							claimForCounter++;
							aduType = "premise";
						} else if (aduType.contentEquals("claim-against")) {
							claimAgainstCounter++;
							aduType = "premise";
						}
						
					}
					// Some prints
					write2XMI(ae, xmiWriter, aduType, sentence, topicIndex, filename, ++numberOfInstanceCounter);
					System.out.println(sentence + ", " + aduType + ", " + numberOfInstanceCounter);
				}
			}
		} catch (Exception ex) {
			ex.printStackTrace();
		}

		writeTopicsToFile(allTopics, TOPICS_PATH);
		writeStatisticToFile(majorClaimCounter, premiseCounter, claimAgainstCounter, claimForCounter,
				numberOfDocumentCounter, numberOfTopicCounter, STATISTIC_PATH);
		System.out.println("\nfinished\n");

		// Destroy UIMA engines
		cr.destroy();
		ae.destroy();
	}

	private void writeStatisticToFile(Integer majorClaimCounter, Integer premiseCounter, Integer claimAgainstCounter,
			Integer claimForCounter, Integer numberOfDocumentCounter, Integer numberOfTopicCounter, String pathToFile)
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
		bufferedWriter.write("majorclaims:" + String.valueOf(majorClaimCounter));
		bufferedWriter.newLine();
		bufferedWriter.write("claim-for:" + String.valueOf(claimForCounter));
		bufferedWriter.newLine();
		bufferedWriter.write("claim-against:" + String.valueOf(claimAgainstCounter));
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
			Integer topicIndex, String fileName, Integer aduId)
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

		String outputDir = OUTPUT_COLLECTION_DIR + "topic" + "-" + String.format("%03d", topicIndex) + "/" + fileName
				+ "/";
		// Write sentence with ADU annotation to file
		xmiWriter.write(cas, outputDir, "document-" + String.format("%04d", aduId) + ".txt");
	}

	// -------------------------------------------------------------------------
	// INITIALIZATION
	// -------------------------------------------------------------------------

	/**
	 * Returns the collection reader in the file with the given path to be used to
	 * iterate over the input directory with the given path.
	 * 
	 * @param crPath   The path of the collection reader
	 * @param inputDir The path of the input directory
	 * @return The collection reader.
	 */
	private CollectionReader createCollectionReader(String crPath, String inputDir) {
		System.out.print("Initializing \"" + crPath + "\"...");
		long count = System.currentTimeMillis();
		CollectionReader cr = null;
		try {
			// Create collection reader from XML descriptor
			XMLInputSource xmlInputSource = new XMLInputSource(crPath);
			ResourceSpecifier specifier = UIMAFramework.getXMLParser().parseResourceSpecifier(xmlInputSource);
			cr = UIMAFramework.produceCollectionReader(specifier);

			// Change parameter values and, therefore, reconfigure reader
			cr.setConfigParameterValue("InputDirectory", inputDir);
			cr.setConfigParameterValue("IncludeSubdirectories", true);
			cr.reconfigure();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
		count = System.currentTimeMillis() - count;
		System.out.println("\nfinished in " + (count / 1000.0) + "s\n");
		return cr;
	}

	/**
	 * Creates and returns the analysis engine that refers to the specified
	 * descriptor file path.
	 * 
	 * @param aePath The path of descriptor file the analysis engine
	 * @return The analysis engine
	 */
	private AnalysisEngine createAnalysisEngine(String aePath) {
		System.out.print("Initializing \"" + aePath + "\"...");
		long count = System.currentTimeMillis();
		AnalysisEngine ae = null;
		try {
			// Create analysis engine from XML descriptor
			XMLInputSource xmlInputSource = new XMLInputSource(aePath);
			ResourceSpecifier specifier = UIMAFramework.getXMLParser().parseResourceSpecifier(xmlInputSource);
			ae = UIMAFramework.produceAnalysisEngine(specifier);
		} catch (Exception ex) {
			ex.printStackTrace();
		}
		count = System.currentTimeMillis() - count;
		System.out.println("\nfinished in " + (count / 1000.0) + "s\n");
		return ae;
	}

	// -------------------------------------------------------------------------
	// MAIN
	// -------------------------------------------------------------------------

	/**
	 * Starts the collection processing.
	 * 
	 * @param args Not used
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
		StudentEssaysProcessor processor = new StudentEssaysProcessor();
		processor.processCollection();
	}

}
