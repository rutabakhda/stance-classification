package feature.aggregate;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.jcas.JCas;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.feature.content.TokenNGrams;
import feature.length.ContentLength;

/**
 * This class implements an aggregate feature type, which consists
 * of TokenNGramand Content Length features.
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class ContentLengthTokenNGrams implements IFeatureType {
	
	
	private IFeatureType tokenNgrams;
	
	private IFeatureType contentLength;
	
	
	

	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {
		this.tokenNgrams = new TokenNGrams();
		this.contentLength = new ContentLength();
		
		this.tokenNgrams.initializeFeatureDetermination(configurationProps);
		this.contentLength.initializeFeatureDetermination(configurationProps);
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {
		this.tokenNgrams.updateCandidateFeatures(jcas, start, end);
		this.contentLength.updateCandidateFeatures(jcas, start, end);
	}

	@Override
	public List<String> determineFeatures(Properties configurationProps, Properties normalizationProps) {
		List<String> featureNames = new ArrayList<String>();
		featureNames.addAll(this.tokenNgrams.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.contentLength.determineFeatures(configurationProps, normalizationProps));
		return featureNames;
	}

	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, Properties configurationProps, Properties normalizationProps) {
		this.tokenNgrams = new TokenNGrams();
		this.contentLength = new ContentLength();
		
		this.tokenNgrams.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.contentLength.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
	}

	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, int end) {
		List<Double> featureValues = new ArrayList<Double>();
		
		featureValues.addAll(this.tokenNgrams.computeNormalizedFeatureValues(jcas, start, end));
		featureValues.addAll(this.contentLength.computeNormalizedFeatureValues(jcas, start, end));

		return featureValues;
	}

}
