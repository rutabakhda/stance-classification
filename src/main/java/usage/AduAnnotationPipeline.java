package usage;


import java.io.File;
import java.io.FileOutputStream;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.impl.XmiCasSerializer;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;

import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;


public class AduAnnotationPipeline {
	
	private static final Pattern ARGUMENTATIVE = Pattern.compile("^Argumentative[\\s]*");
	
	
	private static final Pattern NON_ARGUMENTATIVE = Pattern.compile("^Non-Argumentative[\\s]*");
	
	
	private static final String INPUT_COLLECTION_DIR = 
			"data/demo/webis-debate-16";
	
	private static final String COLLECTION_READER_PATH = 
			"../aitools4-ie-uima/conf/uima-descriptors/collection-readers/UIMAPlainTextReader.xml";
	
	private static final String ANALYSIS_ENGINE_PATH = 
			"src/main/resources/uima/aggregates/PosTokenTagger.xml";

	private static final String OUTPUT_COLLECTION_DIR = 
			"data/demo/processed/webis-debate-16";
	
	
	
	private void processCollection() {
		CollectionReader collectionReader = this.createCollectionReader(COLLECTION_READER_PATH, INPUT_COLLECTION_DIR);
		AnalysisEngine analysisEngine = this.createAnalysisEngine(ANALYSIS_ENGINE_PATH);
		try {
			CAS aCas = analysisEngine.newCAS();
			int i = 0;
			while (collectionReader.hasNext()) {
				collectionReader.getNext(aCas);
				
				String[] lines = aCas.getDocumentText().split("\n");
				for (int j = 0; j < lines.length; j++) {
					String line = lines[j];
					
					Matcher argMatcher = ARGUMENTATIVE.matcher(line);
					Matcher nonArgMatcher = NON_ARGUMENTATIVE.matcher(line);
					JCas jcas = null;
					
					if(argMatcher.find()) {
						String docText = line.substring(argMatcher.end());
						CAS cas = analysisEngine.newCAS();
						cas.setDocumentText(docText);
						cas.setDocumentLanguage("english");
						jcas = cas.getJCas();
						ArgumentativeDiscourseUnit adu = new ArgumentativeDiscourseUnit(jcas, 0, jcas.getDocumentText().length());
						adu.setUnitType("Argumentative");
						adu.addToIndexes(jcas);
						
					} else if (nonArgMatcher.find()) {
						String docText = line.substring(nonArgMatcher.end());
						CAS cas = analysisEngine.newCAS();
						cas.setDocumentText(docText);
						cas.setDocumentLanguage("english");
						jcas = cas.getJCas();
						ArgumentativeDiscourseUnit adu = new ArgumentativeDiscourseUnit(jcas, 0, jcas.getDocumentText().length());
						adu.setUnitType("Non-Argumentative");
						adu.addToIndexes(jcas);
						
					} else {
						System.out.println("No type matched");
					}
					
					
					
					analysisEngine.process(jcas);
					if (!new File(OUTPUT_COLLECTION_DIR + "/document-" + Integer.toString(i)).exists())
						new File(OUTPUT_COLLECTION_DIR + "/document-" + Integer.toString(i)).mkdirs();
					String fileName = "/" + "document-" + Integer.toString(i) + "/" + "unit-" + Integer.toString(j) + ".xmi";
					File output = new File(OUTPUT_COLLECTION_DIR + fileName);
					FileOutputStream outputStream = new FileOutputStream(output);
					XmiCasSerializer.serialize(jcas.getCas(), outputStream);
				}
				i++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		collectionReader.destroy();
		analysisEngine.destroy();
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
		AduAnnotationPipeline pipe = new AduAnnotationPipeline();
		pipe.processCollection();
	}

}
