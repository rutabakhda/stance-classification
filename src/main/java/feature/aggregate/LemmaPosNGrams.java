package feature.aggregate;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.jcas.JCas;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.feature.content.TokenNGrams;
import de.aitools.ie.uima.feature.style.POSNGrams;
import feature.content.LemmaNGrams;

/**
 * Implements an aggregate feature type, which consists of TokenNGram and PosNGram features.
 * @author lukas.peter.trautner@uni-weimar.de
 *
 */
public class LemmaPosNGrams implements IFeatureType {
	
	
	private IFeatureType posNgrams;
	
	private IFeatureType lemmaNGrams;
	
	
	

	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {
		this.posNgrams = new POSNGrams();
		this.lemmaNGrams = new LemmaNGrams();
		
		this.posNgrams.initializeFeatureDetermination(configurationProps);
		this.lemmaNGrams.initializeFeatureDetermination(configurationProps);
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {
		this.posNgrams.updateCandidateFeatures(jcas, start, end);
		this.lemmaNGrams.updateCandidateFeatures(jcas, start, end);
	}

	@Override
	public List<String> determineFeatures(Properties configurationProps, Properties normalizationProps) {
		List<String> featureNames = new ArrayList<String>();
		featureNames.addAll(this.posNgrams.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.lemmaNGrams.determineFeatures(configurationProps, normalizationProps));
		return featureNames;
	}

	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, Properties configurationProps, Properties normalizationProps) {
		this.posNgrams = new POSNGrams();
		this.lemmaNGrams = new LemmaNGrams();
		
		this.posNgrams.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.lemmaNGrams.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
	}

	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, int end) {
		List<Double> featureValues = new ArrayList<Double>();
		
		featureValues.addAll(this.posNgrams.computeNormalizedFeatureValues(jcas, start, end));
		featureValues.addAll(this.lemmaNGrams.computeNormalizedFeatureValues(jcas, start, end));

		return featureValues;
	}

}
