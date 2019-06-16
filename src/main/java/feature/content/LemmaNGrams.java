package feature.content;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.jcas.JCas;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.feature.content.Lemma1Grams;
import de.aitools.ie.uima.feature.content.Lemma2Grams;
import de.aitools.ie.uima.feature.content.Lemma3Grams;

public class LemmaNGrams implements IFeatureType {
	
	private IFeatureType lemma1grams;
	private IFeatureType lemma2grams;
	private IFeatureType lemma3grams;
	
	

	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {	
		this.lemma1grams = new Lemma1Grams();
		this.lemma2grams = new Lemma2Grams();
		this.lemma3grams = new Lemma3Grams();
		this.lemma1grams.initializeFeatureDetermination(configurationProps);
		this.lemma2grams.initializeFeatureDetermination(configurationProps);
		this.lemma3grams.initializeFeatureDetermination(configurationProps);
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {
		this.lemma1grams.updateCandidateFeatures(jcas, start, end);
		this.lemma2grams.updateCandidateFeatures(jcas, start, end);
		this.lemma3grams.updateCandidateFeatures(jcas, start, end);
	}
	
	@Override
	public List<String> determineFeatures(Properties configurationProps, 
			Properties normalizationProps){
		List<String> featureNames = new ArrayList<String>();
		featureNames.addAll(lemma1grams.determineFeatures(
				configurationProps, normalizationProps));
		featureNames.addAll(lemma2grams.determineFeatures(
				configurationProps, normalizationProps));
		featureNames.addAll(lemma3grams.determineFeatures(
				configurationProps, normalizationProps));
		return featureNames;
	}
	
	
	
	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, 
			Properties configurationProps, Properties normalizationProps){
		this.lemma1grams = new Lemma1Grams();
		this.lemma2grams = new Lemma2Grams();
		this.lemma3grams = new Lemma3Grams();
		this.lemma1grams.initializeFeatureComputation(allFeatureNames, 
				configurationProps, normalizationProps);
		this.lemma2grams.initializeFeatureComputation(allFeatureNames, 
				configurationProps, normalizationProps);
		this.lemma3grams.initializeFeatureComputation(allFeatureNames, 
				configurationProps, normalizationProps);
	}
	
	
	
	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, 
			int end) {
		List<Double> values = new ArrayList<Double>();
		values.addAll(this.lemma1grams.computeNormalizedFeatureValues(
				jcas, start, end));
		values.addAll(this.lemma2grams.computeNormalizedFeatureValues(
				jcas, start, end));
		values.addAll(this.lemma3grams.computeNormalizedFeatureValues(
				jcas, start, end));
		return values;
	}
}
