package feature.position;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.uima.cas.FSIterator;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.tcas.Annotation;
import org.apache.uima.jcas.tcas.DocumentAnnotation;

import de.aitools.ie.uima.feature.IFeatureType;
import de.aitools.ie.uima.type.argumentation.ArgumentativeDiscourseUnit;

public class ArgumentativeDiscourseUnitPosition implements IFeatureType {
	
	private static final String FEATURE_AFFIX = "ArgumentativeDiscourseUnitPosition_";

	private List<String> featureNames;
	
	@Override
	public void initializeFeatureDetermination(Properties configurationProps) {
		this.featureNames = new ArrayList<String>();
		this.featureNames.add(FEATURE_AFFIX + "1stArgumentativeDiscourseUnitInText");
		this.featureNames.add(FEATURE_AFFIX + "2ndArgumentativeDiscourseUnitInText");
		this.featureNames.add(FEATURE_AFFIX + "lastArgumentativeDiscourseUnitInText");
		this.featureNames.add(FEATURE_AFFIX + "relArgumentativeDiscourseUnitInText");
	}

	@Override
	public void updateCandidateFeatures(JCas jcas, int start, int end) {}

	
	@Override
	public List<String> determineFeatures(Properties configurationProps, Properties normalizationProps) {
		return featureNames;
	}

	
	@Override
	public void initializeFeatureComputation(List<String> allFeatureNames, Properties configurationProps, Properties normalizationProps) {}

	
	@Override
	public List<Double> computeNormalizedFeatureValues(JCas jcas, int start, int end) {
		
		Annotation relevantSpan = new Annotation(jcas, 0, jcas.getDocumentText().length());
		
		FSIterator<Annotation> relevantSpanIter = jcas.getAnnotationIndex(DocumentAnnotation.type).iterator();
		if (relevantSpanIter.hasNext()){
			relevantSpan = relevantSpanIter.next();
		}
		
		double units = 0.0;
		double unitIndex = 0.0;
		
		FSIterator<Annotation> unitIter = 
				jcas.getAnnotationIndex(ArgumentativeDiscourseUnit.type).subiterator(relevantSpan);
			while (unitIter.hasNext()){
				Annotation unit = unitIter.next();
				units++;
				if (unit.getBegin() <= start && unit.getEnd() >= end){
					unitIndex = units;
				}
			}
			
		List<Double> featureValues = new ArrayList<Double>();	
		
		if (units == 0.0) {
			featureValues.add(0.0);
			featureValues.add(0.0);
			featureValues.add(0.0);
			featureValues.add(0.0);
		} else if (units == 1.0) {
			featureValues.add(1.0);
			featureValues.add(0.0); 
			featureValues.add(1.0); 
			featureValues.add(1.0); 
		} else {
			if (unitIndex == 1.0) {
				featureValues.add(1.0);
			} else {
				featureValues.add(0.0);
			}
			if (unitIndex == 2.0) {
				featureValues.add(1.0);
			} else {
				featureValues.add(0.0);
			}
			if (unitIndex == units) {
				featureValues.add(1.0);
			} else {
				featureValues.add(0.0);
			}
			featureValues.add(unitIndex / units);
		}	
	
		return featureValues;
	}

}
