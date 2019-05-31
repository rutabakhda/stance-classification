package feature.length;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.cas.FSIterator;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.type.core.Token;

/**
 * This class denotes a feature type that captures the length of a 
 * text in different ways. All lengths lie in the range 0 to 1. 
 * Where necessary, normalization is done based on the maximum length values 
 * found in a training set. 
 * 
 *  In particular, the following length values are computed:
 * <UL>
 *   <LI>The number of characters</LI> 
 *   <LI>The number of tokens</LI> 
 * </UL>
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class ContentLength implements IFeatureType {
	
	// -------------------------------------------------------------------------
	// CONSTANTS
	// -------------------------------------------------------------------------

	/**
	 * The name of this feature type. Can be used as the value of the respective
	 * parameter in calls of the two initialization methods of the superclass of 
	 * this type.
	 * 
	 * Feature type names should be unique, so don't use this name for any other 
	 * feature type. 
	 */
	public static final String FEATURE_TYPE_NAME = "ContentLength_";
	
	
	// -------------------------------------------------------------------------
	// NAMES OF OUTPUT PARAMETERS
	// -------------------------------------------------------------------------

	/**
	 * Name of the output parameter that specifies
	 * the maximum number of characters in a text from a text collection in order
	 * to consider it for feature computations.
	 */
	private static final String PARAM_MAX_ABS_CHAR_OCCURRENCE =
		"output_contentlength_maxcharoccurrence";
	
	/**
	 * Name of the output parameter that specifies
	 * the maximum number of tokens in a text from a text collection in order
	 * to consider it for feature computations.
	 */
	private static final String PARAM_MAX_ABS_TOKEN_OCCURRENCE =
		"output_contentlength_maxtokenoccurrence";
	
	
	// -------------------------------------------------------------------------
	// OUTPUT PARAMETER VALUES
	// -------------------------------------------------------------------------

	/**
	 * The maximum number of characters in a text from the training text 
	 * collection. Used for normalization.
	 */
	private double maxAbsCharOccurrence;
	
	/**
	 * The maximum number of tokens in a text from the training text collection.
	 * Used for normalization.
	 */
	private double maxAbsTokenOccurrence;
	

	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {
		this.maxAbsCharOccurrence = 0;
		this.maxAbsTokenOccurrence = 0;
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {
		Annotation relevantSpan = new Annotation(jcas, start, end);
		int characters = relevantSpan.getEnd() - relevantSpan.getBegin();
		if (characters > this.maxAbsCharOccurrence) {
			this.maxAbsCharOccurrence = characters;
		}
		
		int tokens = 0;
		FSIterator<Annotation> tokenIter = jcas.getAnnotationIndex(Token.type).subiterator(relevantSpan);
		while (tokenIter.hasNext()) {
			tokenIter.next();
			tokens++;
		}
		if (tokens > this.maxAbsTokenOccurrence) {
			this.maxAbsTokenOccurrence = tokens;
		}
	}

	@Override
	public List<String> determineFeatures(Properties configurationProps, Properties normalizationProps) {
		// Set normalization parameter values
		normalizationProps.setProperty(PARAM_MAX_ABS_CHAR_OCCURRENCE, String.valueOf(this.maxAbsCharOccurrence));
		normalizationProps.setProperty(PARAM_MAX_ABS_TOKEN_OCCURRENCE, String.valueOf(this.maxAbsTokenOccurrence));
		
		// Create feature names and return them
		List<String> featureNames = new ArrayList<String>();
		featureNames.add(FEATURE_TYPE_NAME + "characters");
		featureNames.add(FEATURE_TYPE_NAME + "tokens");
		return featureNames;
	}

	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, Properties configurationProps, Properties normalizationProps) {
		// No need to load feature names here, since exactly the same 
		// features are computed in all cases
				
		// Set parameters for normalization
		this.maxAbsCharOccurrence = Double.parseDouble(normalizationProps.getProperty(PARAM_MAX_ABS_CHAR_OCCURRENCE));
		this.maxAbsTokenOccurrence = Double.parseDouble(normalizationProps.getProperty(PARAM_MAX_ABS_TOKEN_OCCURRENCE));
	}

	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, int end) {
		// Count annotations in relevant span
		Annotation relevantSpan = new Annotation(jcas, start, end);
		int characters = relevantSpan.getEnd() - relevantSpan.getBegin();
		int tokens = 0;
		FSIterator<Annotation> tokenIter = jcas.getAnnotationIndex(Token.type).subiterator(relevantSpan);
		while (tokenIter.hasNext()) {
			tokenIter.next();
			tokens++;
		}
		
		// Compute feature values
		List<Double> featureValues = new ArrayList<Double>();
		
		if (this.maxAbsCharOccurrence == 0.0) {
			featureValues.add(0.0);
		} else if (characters > this.maxAbsCharOccurrence) {
			featureValues.add(1.0);
		} else {
			featureValues.add(characters / this.maxAbsCharOccurrence);
		}
		
		if (this.maxAbsTokenOccurrence == 0.0) {
			featureValues.add(0.0);
		} else if (tokens > this.maxAbsTokenOccurrence) {
			featureValues.add(1.0);
		} else {
			featureValues.add(tokens / this.maxAbsTokenOccurrence);
		}
		return featureValues;
	}

}
