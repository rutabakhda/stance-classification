package feature.aggregate;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.jcas.JCas;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.feature.style.POSNGrams;
import feature.content.LemmaNGrams;
import feature.length.ContentLength;
import feature.position.ArgumentativeDiscourseUnitPosition;

public class LengthPositionLemmaPosNGrams implements IFeatureType {
	
	private IFeatureType length;
	private IFeatureType position;
	private IFeatureType lemma;
	private IFeatureType pos;
	

	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {
		this.length = new ContentLength();
		this.position = new ArgumentativeDiscourseUnitPosition();
		this.lemma = new LemmaNGrams();
		this.pos = new POSNGrams();
		
		this.length.initializeFeatureDetermination(configurationProps);
		this.position.initializeFeatureDetermination(configurationProps);
		this.lemma.initializeFeatureDetermination(configurationProps);
		this.pos.initializeFeatureDetermination(configurationProps);
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {
		this.length.updateCandidateFeatures(jcas, start, end);
		this.position.updateCandidateFeatures(jcas, start, end);
		this.lemma.updateCandidateFeatures(jcas, start, end);
		this.pos.updateCandidateFeatures(jcas, start, end);
	}

	@Override
	public List<String> determineFeatures(Properties configurationProps, Properties normalizationProps) {
		List<String> featureNames = new ArrayList<String>();
		featureNames.addAll(this.length.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.position.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.lemma.determineFeatures(configurationProps, normalizationProps));
		featureNames.addAll(this.pos.determineFeatures(configurationProps, normalizationProps));
		return featureNames;
	}

	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, Properties configurationProps,
			Properties normalizationProps) {
		this.length = new ContentLength();
		this.position = new ArgumentativeDiscourseUnitPosition();
		this.lemma = new LemmaNGrams();
		this.pos = new POSNGrams();
		
		this.length.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.position.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.lemma.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);
		this.pos.initializeFeatureComputation(allFeatureNames, configurationProps, normalizationProps);

	}

	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, int end) {
		List<Double> values = new ArrayList<Double>();
		values.addAll(this.length.computeNormalizedFeatureValues(jcas, start, end));
		values.addAll(this.position.computeNormalizedFeatureValues(jcas, start, end));
		values.addAll(this.lemma.computeNormalizedFeatureValues(jcas, start, end));
		values.addAll(this.pos.computeNormalizedFeatureValues(jcas, start, end));
		return values;
	}

}
