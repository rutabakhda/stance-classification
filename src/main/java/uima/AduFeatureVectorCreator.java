package uima;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.FSIterator;
import org.apache.uima.cas.Feature;
import org.apache.uima.cas.Type;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;
import org.apache.uima.resource.ResourceSpecifier;
import org.apache.uima.util.XMLInputSource;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.io.PathTools;

public class AduFeatureVectorCreator {


	// -------------------------------------------------------------------------
	// PARAMETERS OF THE FEATURE VECTOR CREATOR
	// -------------------------------------------------------------------------

	/**
	 * The path of root directory of the training files to be processed.
	 */
	private static final String TRAINING_SET_PATH = 
//			"this/is/my/training/set/path/";
			"data/demo/processed/webis-debate-16/";

	/**
	 * The path of root directory of the validation files to be processed.
	 */
	private static final String VALIDATION_SET_PATH = 
//			"this/is/my/validation/set/path/";
			"data/demo/processed/webis-debate-16/";
	/**
	 * The path of root directory of the test files to be processed.
	 */
	private static final String TEST_SET_PATH = 
//			"this/is/my/test/set/path/";
			"data/demo/processed/webis-debate-16/";
	/**
	 * The path of the XMI file of the collection reader to be used to iterate
	 * over all files to be processed.
	 */
	private static final String COLLECTION_READER_PATH = 
//			"this/is/myCollectionReader.xml";
			"../aitools4-ie-uima/conf/uima-descriptors/collection-readers/"
			+ "UIMAAnnotationFileReader.xml";

	/**
	 * The path of the XMI file of the analysis engine to be used to process
	 * the files.
	 */
	private static final String ANALYSIS_ENGINE_PATH = 
//			"this/is/myAnalysisEngine.xml";
			"../aitools4-ie-uima/conf/uima-descriptors/primitive-AEs/template/"
			+ "DummyAnalysisEngine.xml";
	
	/**
	 * The fully qualified Java class name of the feature type to be used for
	 * feature computation.
	 */
	private static final String FEATURE_TYPE_CLASS = 
//			"de.aitools.ie.uima.feature.this.is.MyFeatureType";
			"uima.ArgumentativeDiscourseUnitFeatures";
	
	/**
	 * The path of the properties file to be used for the configuration of the
	 * feature type.
	 */
	public static final String FEATURE_CONFIG_PROPS = 
//			"properties/feature-config_my-config.properties";
			"src/main/resources/properties/aduFeatureCreator.properties";
	
	/**
	 * The fully qualified Java class name of the annotation type that 
	 * represents the target class type.
	 */
	private static final String CLASS_ANNOTATION_TYPE = 
//			"this.is.my.ClassAnnotationType";
			"de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit";

	/**
	 * The name of the feature of the annotation type that contains the class
	 * value. If the annotation type (or its child classes) represent the class
	 * values themselves, set this annotation feature to the empty string.
	 */
	private static final String CLASS_ANNOTATION_FEATURE = 
//			"thisIsMyClassAnnotationFeature";
			"unitType";

	
	// -------------------------------------------------------------------------
	// REFERENCES
	// -------------------------------------------------------------------------

	/**
	 * The (usually aggregate) feature type to be used
	 */
	private IFeatureType featureType;

	/**
	 * The feature config properties.
	 */
	private Properties featureProps;
	
	/**
	 * The feature normalization properties
	 */
	private Properties normalizationProps;

	
	
	// -------------------------------------------------------------------------
	// CONSTRUCTOR
	// -------------------------------------------------------------------------
	
	/**
	 * Initializes the generator
	 */
	public AduFeatureVectorCreator(){
		// Load feature type and its config parameters	
		this.featureType = null;
		this.featureProps = new Properties();
		String path = PathTools.getAbsolutePath(FEATURE_CONFIG_PROPS);
		try (BufferedInputStream stream = new BufferedInputStream(
					new FileInputStream(path));){
			this.featureType = (IFeatureType) Class.forName(FEATURE_TYPE_CLASS, 
					true, this.getClass().getClassLoader()).newInstance();
			this.featureProps.load(stream);
		} catch (Exception e){
			e.printStackTrace();
		}
		
		// Initialize feature normalization properties
		this.normalizationProps = new Properties();
	}

	
	
	// -------------------------------------------------------------------------
	// MAIN GENERATION METHODS
	// -------------------------------------------------------------------------
	
	/**
	 * Generates all feature vectors based on the defined parameters of this
	 * class.
	 * 
	 */
	public void generatorFeatureVectors(){
		// First determine feature set on training set
		this.featureType.initializeFeatureDetermination(this.featureProps);
		this.updateCandidateFeatures();
		List<String> featureNames = this.featureType.determineFeatures(
				this.featureProps, this.normalizationProps);
		System.out.println("Features: " + featureNames.size() + "\n");

		// Then compute feature vectors on training set
		this.featureType.initializeFeatureComputation(
				featureNames, this.featureProps, this.normalizationProps);
		List<List<Double>> trainingVectors = new ArrayList<List<Double>>();
		List<String> trainingClasses = new ArrayList<String>();
		this.computeNormalizedFeatureValues(TRAINING_SET_PATH, trainingVectors, 
				trainingClasses);		
		System.out.println("Training vectors: " + trainingVectors.size() 
				+ "\n");
		
		// Then compute feature vectors on the other sets
		List<List<Double>> validationVectors = new ArrayList<List<Double>>();
		List<String> validationClasses = new ArrayList<String>();
		this.computeNormalizedFeatureValues(VALIDATION_SET_PATH, 
				validationVectors, validationClasses);	
		System.out.println("Validation vectors: " + validationVectors.size() 
				+ "\n");
		List<List<Double>> testVectors = new ArrayList<List<Double>>();
		List<String> testClasses = new ArrayList<String>();
		this.computeNormalizedFeatureValues(TEST_SET_PATH, testVectors, 
				testClasses);
		System.out.println("Test vectors: " + testVectors.size() + "\n");	
	}

	/**
	 * Updates the candidate features once for each text from the training set.
	 * 
	 */
	private void updateCandidateFeatures(){
		System.out.print("Determine feature set...");
		// Load engines
		CollectionReader cr = this.createCollectionReader(TRAINING_SET_PATH);
		AnalysisEngine ae = this.createAnalysisEngine();	
  		// Process training set
  		int processed = 0;
  		try{
  			// Iterate over all texts
  			CAS aCAS = ae.newCAS();
  			while (cr.hasNext()){  				
  				// Get and preprocess current text
  				cr.getNext(aCAS);
  				JCas jcas = aCAS.getJCas();
  				ae.process(jcas);	
  				// Update candidate features once for each class annotation
  				Type type = jcas.getTypeSystem().getType(CLASS_ANNOTATION_TYPE);
  				FSIterator<Annotation> classIter = 
  					jcas.getAnnotationIndex(type).iterator();
  				while (classIter.hasNext()){
  					Annotation classAnnotation = classIter.next();
					this.featureType.updateCandidateFeatures(jcas, 
							classAnnotation.getBegin(), 
							classAnnotation.getEnd());	
  				}
				// Print progress
  				if (processed++ % 10 == 0) System.out.print(".");	
  			}
  		} catch (Exception ex){
  			ex.printStackTrace();
  		}
		// Destroy engines
		cr.destroy();
		ae.destroy();
		System.out.println("finished");
	}
	
	/**
	 * Computes and stores one feature vector and its associated class value in
	 * the given lists for each text from the corpus at the given path.
	 * 
	 * @param corpusPath The corpus path
	 * @param featureVectors The list of feature vectors
	 * @param classValues The list of class values
	 */
	private void computeNormalizedFeatureValues(String corpusPath, 
			List<List<Double>> featureVectors, List<String> classValues){
		System.out.print("Compute normalized feature values on " + corpusPath + 
				"...");
		// Load engines
		CollectionReader cr = this.createCollectionReader(corpusPath);
		AnalysisEngine ae = this.createAnalysisEngine();
		// Process corpus
  		int processed = 0;
  		try{
  			// Iterate over all texts
  			CAS aCAS = ae.newCAS();
  			while (cr.hasNext()){  				
  				// Get and preprocess current text
  				cr.getNext(aCAS);
  				JCas jcas = aCAS.getJCas();
  				ae.process(jcas);	
  				// Compute one feature vector for each class annotation
  				Type type = jcas.getTypeSystem().getType(CLASS_ANNOTATION_TYPE);
  				FSIterator<Annotation> classIter = 
  					jcas.getAnnotationIndex(type).iterator();
  				while (classIter.hasNext()){
  					Annotation classAnnotation = classIter.next();
					featureVectors.add(this.featureType.
							computeNormalizedFeatureValues(jcas, 
									classAnnotation.getBegin(), 
									classAnnotation.getEnd()));			
					classValues.add(this.getClassValue(classAnnotation));
  				}
				// Print progress
  				if (processed++ % 10 == 0) System.out.print(".");	
  			}
  		} catch (Exception ex){
  			ex.printStackTrace();
  		}
		// Destroy engines
		cr.destroy();
		ae.destroy();
		System.out.println("finished");
	}

	
	// -------------------------------------------------------------------------
	// INTERNAL HELPERS
	// -------------------------------------------------------------------------

	/**
	 * Returns the collection reader to be used to iterate over the input 
	 * directory with the given path. 
	 * 
	 * @param inputDir The path of the input directory
	 * @return The collection reader.
	 */
	private CollectionReader createCollectionReader(String inputDir){
		CollectionReader cr = null;
		try{
			XMLInputSource xmlInputSource = new XMLInputSource(
					COLLECTION_READER_PATH);
			ResourceSpecifier specifier = 
				UIMAFramework.getXMLParser().parseResourceSpecifier(
						xmlInputSource);
			cr = UIMAFramework.produceCollectionReader(specifier);
			cr.setConfigParameterValue("InputDirectory", inputDir);
			cr.setConfigParameterValue("IncludeSubdirectories", true);
			cr.reconfigure();
		} catch (Exception ex){
			ex.printStackTrace();
		}
		return cr;
	}

	/**
	 * Creates and returns the analysis engine to be used.
	 * 
	 * @return The analysis engine
	 */
	private AnalysisEngine createAnalysisEngine(){
		AnalysisEngine ae = null;
		try{
			XMLInputSource xmlInputSource = new XMLInputSource(
					ANALYSIS_ENGINE_PATH);
			ResourceSpecifier specifier = 
				UIMAFramework.getXMLParser().parseResourceSpecifier(
						xmlInputSource);
			ae = UIMAFramework.produceAnalysisEngine(specifier);
			ae.reconfigure();
		} catch (Exception ex){
			ex.printStackTrace();
		}
		return ae;
	}
	
	/**
	 * Returns the class value that refers to the given class annotation. 
	 * 
	 * @param classAnnotation The class annotation
	 * @return The class value
	 */
	private String getClassValue(Annotation classAnnotation){
		String clazz = null;
		// Use annotation type if feature is null
		if ("".equals(CLASS_ANNOTATION_FEATURE)){
			clazz = classAnnotation.getClass().getSimpleName();
		}
		// Otherwise use feature value
		else {
			List<Feature> features = classAnnotation.getType().getFeatures();
			for (Feature feature : features) {
				if (feature.getShortName().equals(CLASS_ANNOTATION_FEATURE)){
					clazz = classAnnotation.getFeatureValueAsString(feature);
					break;
				}
			}
		}
		return clazz;
	}
	
	
	// -------------------------------------------------------------------------
	// MAIN
	// -------------------------------------------------------------------------
	
	/**
	 * Starts the generation of feature files
	 * @param args Not used
	 */
	public static void main(String [] args){
		new AduFeatureVectorCreator().generatorFeatureVectors();
	}
}
