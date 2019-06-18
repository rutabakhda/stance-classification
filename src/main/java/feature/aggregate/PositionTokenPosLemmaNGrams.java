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
import feature.position.ArgumentativeDiscourseUnitPosition;

public class PositionTokenPosLemmaNGrams implements IFeatureType {
	
	private IFeatureType position;
	private IFeatureType token;
	private IFeatureType pos;
	private IFeatureType lemma;
	

	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {
		this.token = new TokenNGrams();
		this.pos = new POSNGrams();
		this.position = new ArgumentativeDiscourseUnitPosition();
		this.lemma = new LemmaNGrams();
		
		this.token.initializeFeatureDetermination(configurationProps);
		this.pos.initializeFeatureDetermination(configurationProps);
		this.position.initializeFeatureDetermination(configurationProps);
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {
		this.token.updateCandidateFeatures(jcas, start, end);
		this.pos.updateCandidateFeatures(jcas, start, end);
		this.position.updateCandidateFeatures(jcas, start, end);
		this.lemma.updateCandidateFeatures(jcas, start, end);
	}

	@Override
	public List<String> determineFeatures(Properties configurationProps, Properties normalizationProps) {
		List<String> featureNames = new ArrayList<String>();
		featureNames.addAll(this.token.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.pos.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.position.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.lemma.determineFeatures(configurationProps, normalizationProps));

		return featureNames;
	}

	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, Properties configurationProps,
			Properties normalizationProps) {
		this.token = new LemmaNGrams();
		this.pos = new TokenNGrams();
		this.position = new ArgumentativeDiscourseUnitPosition();
		this.lemma = new LemmaNGrams();

		this.token.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.pos.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.position.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.lemma.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
	}

	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, int end) {
		List<Double> values = new ArrayList<Double>();
		values.addAll(this.token.computeNormalizedFeatureValues(jcas, start, end));
		values.addAll(this.pos.computeNormalizedFeatureValues(jcas, start, end));
		values.addAll(this.position.computeNormalizedFeatureValues(jcas, start, end));
		values.addAll(this.lemma.computeNormalizedFeatureValues(jcas, start, end));

		return values;
	}

}
