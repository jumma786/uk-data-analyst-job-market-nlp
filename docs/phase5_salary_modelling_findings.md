\# Phase 5 — Salary Modelling Findings



Captures the salary prediction modelling phase of the UK Data Analyst Job

Market NLP project. Two models trained side by side — one on employer-posted

salaries, one on Adzuna's predicted salaries — to compare what each set of

salaries reflects.



\## Methodology



\### Targets



Two target variables, modelled independently:



1\. \*\*Real (employer-posted) salaries\*\* — 1,001 postings where `salary\_is\_predicted = False`. These are salary figures published by the employer themselves.

2\. \*\*Adzuna predicted salaries\*\* — 1,823 postings where `salary\_is\_predicted = True`. These are Adzuna's own model-generated estimates.



Both target variables use `salary\_midpoint = (salary\_min + salary\_max) / 2`.



\### Outlier handling



Before training:



\- \*\*8 low outliers removed\*\* (< £15K). All were employer-posted data entry errors (£1, £25, £400 — almost certainly day rates entered as annual salaries, or empty fields filled with placeholder digits).

\- \*\*6 high outliers capped at £200K\*\* (winsorising). These included one US-pharma VP role, one Investment Banking role, and several freelance day-rates annualised. Cap chosen to retain genuine UK senior role salaries without letting US/freelance figures distort the model.

\- \*\*3 rows with missing salary\_midpoint\*\* dropped.



Final modelling dataset: \*\*2,824 rows\*\*.



\### Features (267 total)



Three feature groups:



| Group | n | Source |

|---|---:|---|

| Categorical (one-hot encoded) | 62 | Cluster archetype, region (top 15 + "Other"), category label, contract type, contract time |

| Text (TF-IDF) | 200 | Title text, 1-2 word n-grams, min\_df=5, top 200 by frequency |

| Numeric (scaled) | 5 | Title word count, has\_senior flag, has\_junior flag, description length, n\_keywords\_matched |



Title text only — not description text. Earlier work (Phase 4) established that the truncated 75-word description snippets carry too little role-distinguishing signal compared to titles.



\### Models compared



Four models trained on each target with identical 5-fold cross-validation:



| Model | Configuration |

|---|---|

| Baseline (DummyRegressor) | Predicts the training-set mean |

| Ridge Regression | alpha=1.0, L2 regularisation |

| Random Forest | 200 trees, max\_depth=15 |

| XGBoost | 300 trees, max\_depth=6, learning\_rate=0.1 |



\### Evaluation metrics



\- \*\*R²\*\* — proportion of salary variance explained

\- \*\*MAE (Mean Absolute Error)\*\* — average £ error in predictions

\- Both reported as mean ± std across the 5 CV folds



\## Results



\### Real (employer-posted) salaries



| Model | R² | MAE |

|---|---:|---:|

| Baseline (predict mean) | -0.011 ± 0.011 | £28,280 ± £1,996 |

| Ridge Regression | 0.459 ± 0.078 | £19,502 ± £839 |

| Random Forest | 0.495 ± 0.043 | £17,123 ± £976 |

| \*\*XGBoost\*\* | \*\*0.512 ± 0.068\*\* | \*\*£16,925 ± £773\*\* |



\### Adzuna-predicted salaries



| Model | R² | MAE |

|---|---:|---:|

| Baseline (predict mean) | -0.008 ± 0.004 | £13,039 ± £667 |

| Ridge Regression | 0.357 ± 0.056 | £10,044 ± £750 |

| Random Forest | 0.354 ± 0.079 | £10,018 ± £842 |

| \*\*XGBoost\*\* | \*\*0.368 ± 0.074\*\* | \*\*£9,730 ± £794\*\* |



\## Findings



\### 1. Real employer-posted salaries are \*more\* predictable than Adzuna's own predictions



This was unexpected. The initial hypothesis was that Adzuna's predictions would be more learnable — being themselves model-generated, they should follow tractable patterns derived from features available in the data.



The opposite is true. XGBoost explains \*\*51.2% of variance in real salaries\*\* but only \*\*36.8% of variance in Adzuna's predictions\*\*. The MAE improvement over baseline is 40% for real salaries versus 25% for Adzuna's predictions.



Likely explanation: Adzuna's prediction model uses signals not in this dataset — possibly internal click-through data, posting history, employer profiles, finer-grained location precision, or industry-specific calibrations. Our feature set captures roughly half the variance in real salary data, but only a third of the variance in Adzuna's model output.



This finding inverts the conventional assumption about model-vs-model comparison and is itself a methodological observation worth flagging.



\### 2. Adzuna's prediction model appears to underweight UK location



In the real-salaries model, `region\_grouped\_London` is the \*\*#2 most important feature\*\* (4.6% importance). In the Adzuna-predictions model, London does not appear in the top 20 features at all.



This suggests Adzuna's prediction model either:



\- Treats location through a separate sub-model not captured by feature importance

\- Applies location adjustments at a different stage (post-hoc rather than as a feature)

\- Underweights UK regional pay differences



Without access to Adzuna's model internals this cannot be confirmed, but the discrepancy is meaningful and worth noting in any analysis using their predicted salaries.



\### 3. Title seniority flags are the strongest single salary predictor



Both models put `title\_has\_senior` (7.2% in predicted, 5.7% in real) and `title\_has\_junior` (4.5% in predicted, 3.2% in real) at or near the top of their importance rankings. The single most powerful predictor of UK data salary is whether the word "Senior" (or "Lead", "Principal", "Head", "Director", "Manager", "Chief") appears in the job title.



This is intuitive but worth quantifying. Models with all 267 features available consistently pick the simplest possible heuristic — "is this a senior title or not?" — as a primary signal.



\### 4. Real salaries reward specific terms; Adzuna predictions reward generic role labels



Looking past the seniority flags, the top features diverge meaningfully:



\*\*Real salaries top terms (after seniority):\*\*



\- "software", "power", "staff", "data architect", "management", "remote"



\*\*Adzuna prediction top terms (after seniority):\*\*



\- "analyst", "president", "head", "intern", "senior data", "science engineer", "scientist ai"



Real salaries surface specific tools and senior-role-type terms. Adzuna's model surfaces generic role types and seniority titles. This suggests employer salaries are calibrated against specific skill/tool combinations, while Adzuna's predictions calibrate against role-category averages.



\### 5. Random Forest barely beats Ridge Regression



On real salaries: 0.495 vs 0.459 (3.6 R² points).

On Adzuna predictions: 0.354 vs 0.357 (Ridge actually wins by 0.3 points).



This tells us most of the salary signal in this dataset is \*\*linear\*\* — each feature shifts salary by an approximately fixed amount, with limited interaction effects. The non-linear interactions Random Forest captures don't add meaningful predictive power.



Practical implication: a simpler linear model would be defensible for this problem. The XGBoost win of 1.5-1.7 R² points over Random Forest is real but small.



\### 6. Cluster labels are not dominant features



Despite Phase 4 producing 17 distinct role archetypes via clustering, only one cluster label appears in the top 20 features of either model (`cluster\_str\_12`, the AI/ML cluster, in Adzuna predictions).



This is a slightly humbling finding for the clustering work: the unsupervised clusters tell an interesting story about role types, but the \*direct salary signal\* lives in title text and seniority flags rather than the cluster IDs. The clusters describe the role landscape; they don't predict salary on their own.



\### 7. MAE of £17K means the model is useful for analysis, not for individual salary advice



The XGBoost real-salaries model predicts to within \*\*£16,925\*\* on average. For a dataset with mean salary £62K, this is 27% relative error.



Honest implication: this model is appropriate for \*understanding salary drivers\* (which features matter, how much each contributes) but \*\*not\*\* for \*individual career advice\* (whether to take a £55K offer). A person looking at a £60K role would want predictions accurate to £2-3K — this model is off by £17K on average. Any portfolio framing should make this distinction explicit rather than overclaiming.



\## Acknowledged Limitations



1\. \*\*Sample size for real salaries.\*\* Only 1,001 postings have employer-posted salaries. This is a meaningful sample but not large; CV folds use \~200 postings each for evaluation.

2\. \*\*No external salary data.\*\* The model has no access to Glassdoor, Indeed, LinkedIn salary data, or government wage statistics. Predictions are entirely based on the posting text and metadata.

3\. \*\*Salary distribution is not normal.\*\* Salaries are right-skewed (long tail above £100K) even after winsorising. Linear-in-log models might fit better but were not attempted in scope.

4\. \*\*Feature importance from XGBoost is noisy.\*\* With 267 features, each contributes 5-7% at most. Importance rankings should be read directionally rather than precisely.

5\. \*\*No SHAP analysis.\*\* Feature importance gives global ranking but not local explanations. A SHAP analysis would identify which features drive a specific posting's predicted salary; this was out of scope for the project.



\## Output Files



\- `data/processed/model\_results\_real.csv` — 5-fold CV results, real salaries

\- `data/processed/model\_results\_predicted.csv` — 5-fold CV results, Adzuna predictions

\- `data/processed/feature\_importance\_real.csv` — full 267-feature importance ranking, real model

\- `data/processed/feature\_importance\_predicted.csv` — full 267-feature importance ranking, Adzuna model

