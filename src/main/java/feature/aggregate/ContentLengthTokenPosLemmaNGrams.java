package feature.aggregate;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.jcas.JCas;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.feature.content.TokenNGrams;
import de.aitools.ie.uima.feature.style.POSNGrams;
import feature.content.LemmaNGrams;
import feature.length.ContentLength;

/**
 * This class implements an aggregate feature type, which consists
 * of TokenNGram, PosNGram and Content Length features.
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class ContentLengthTokenPosLemmaNGrams implements IFeatureType {
	
	
	private IFeatureType tokenNgrams;
	
	private IFeatureType posNgrams;
	
	private IFeatureType contentLength;
	
	private IFeatureType lemmaNGrams;
	
	
	

	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {
		this.tokenNgrams = new TokenNGrams();
		this.posNgrams = new POSNGrams();
		this.contentLength = new ContentLength();
		this.lemmaNGrams = new LemmaNGrams();
		
		this.tokenNgrams.initializeFeatureDetermination(configurationProps);
		this.posNgrams.initializeFeatureDetermination(configurationProps);
		this.contentLength.initializeFeatureDetermination(configurationProps);
		this.lemmaNGrams.initializeFeatureDetermination(configurationProps);
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {
		this.tokenNgrams.updateCandidateFeatures(jcas, start, end);
		this.posNgrams.updateCandidateFeatures(jcas, start, end);
		this.contentLength.updateCandidateFeatures(jcas, start, end);
		this.lemmaNGrams.updateCandidateFeatures(jcas, start, end);
	}

	@Override
	public List<String> determineFeatures(Properties configurationProps, Properties normalizationProps) {
		List<String> featureNames = new ArrayList<String>();
		featureNames.addAll(this.tokenNgrams.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.posNgrams.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.contentLength.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.lemmaNGrams.determineFeatures(configurationProps, normalizationProps));
		return featureNames;
	}

	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, Properties configurationProps, Properties normalizationProps) {
		this.tokenNgrams = new TokenNGrams();
		this.posNgrams = new POSNGrams();
		this.contentLength = new ContentLength();
		this.lemmaNGrams = new LemmaNGrams();

		this.tokenNgrams.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.posNgrams.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.contentLength.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.lemmaNGrams.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);

	}

	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, int end) {
		List<Double> featureValues = new ArrayList<Double>();
		
		featureValues.addAll(this.tokenNgrams.computeNormalizedFeatureValues(jcas, start, end));
		featureValues.addAll(this.posNgrams.computeNormalizedFeatureValues(jcas, start, end));
		featureValues.addAll(this.contentLength.computeNormalizedFeatureValues(jcas, start, end));
		featureValues.addAll(this.lemmaNGrams.computeNormalizedFeatureValues(jcas, start, end));

		return featureValues;
	}

}
