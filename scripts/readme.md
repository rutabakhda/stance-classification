### ADU Classification
```./scripts/adu_classification.sh >&1 | tee  "output/$(date +"%Y-%m-%d_%T").log"```

### ADU 5 fold Validation
```./scripts/adu_classification.sh kfold >&1 | tee  "output/$(date +"%Y-%m-%d_%T").log"```

### ADU Random Split Classification
```./scripts/adu_classification.sh random >&1 | tee  "output/$(date +"%Y-%m-%d_%T").log"```