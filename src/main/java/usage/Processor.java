package usage;

import java.io.File;
import java.io.FileOutputStream;

import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.FSIterator;
import org.apache.uima.cas.impl.XmiCasSerializer;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;


public class Processor {
	
	
	private static final String INPUT_COLLECTION_DIR = "data/student-essays/original/";

	private static final String ANALYSIS_ENGINE_PATH = "src/main/resources/uima/aggregates/PosTokenTagger.xml";

	private static final String OUTPUT_COLLECTION_DIR = "data/student-essays/all/";

	private static final String COLLECTION_READER_PATH = "../aitools4-ie-uima/conf/uima-descriptors/collection-readers/" + "UIMAAnnotationFileReader.xml";
	
	public void process() {
		
		AnalysisEngine ae = this.createAnalysisEngine(ANALYSIS_ENGINE_PATH);
		CollectionReader cr = this.createCollectionReader(COLLECTION_READER_PATH, INPUT_COLLECTION_DIR);
		try {
			CAS aCAS = ae.newCAS();
			int i = 0;
			while (cr.hasNext()) {
				cr.getNext(aCAS);
				JCas jcas = aCAS.getJCas();
				ae.process(jcas);
				
				
				String fileName = "/" + "essay-" + Integer.toString(i) + ".xmi";
				File output = new File(OUTPUT_COLLECTION_DIR + fileName);
				FileOutputStream outputStream = new FileOutputStream(output);
				XmiCasSerializer.serialize(jcas.getCas(), outputStream);
				i++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		


	}
	
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

	public static void main(String[] args) {
		Processor p = new Processor();
		p.process();

	}

}
