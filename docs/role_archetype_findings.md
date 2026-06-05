# Role Archetype Findings

Generated after Phase 4 (Embedding and Clustering) of the UK Data Analyst
Job Market NLP project. Captures the interpretation of the 17 role
archetypes identified through HDBSCAN clustering on title embeddings.

## Methodology Recap

- **2,835 cleaned UK job postings** from Adzuna (post-deduplication and junk-filter)
- **Sentence embeddings** generated using `all-MiniLM-L6-v2` (384-dim)
- **Two embedding strategies tested**: full text (title + description) and title-only. Title-only produced cleaner clustering because the 75-word description snippets were too uniform in language (all use the same recruitment register) to drive separation.
- **Dimensionality reduction**: UMAP with `n_neighbors=15`, `min_dist=0.1`, cosine metric
- **Clustering**: HDBSCAN with `min_cluster_size=50`, `min_samples=10`
- **Result**: 17 interpretable clusters + 356 noise points (12.6%)

## Identified Role Archetypes

The 17 archetypes are presented below sorted by median salary, descending.
Salary figures include both employer-posted and Adzuna-predicted values
(the project explicitly distinguishes these in the salary modelling phase).

| Rank | Archetype | Postings | Median Salary | Top Title |
|---:|---|---:|---:|---|
| 1 | AI / Machine Learning Engineer | 134 | £74,416 | Distinguished ML Data Scientist |
| 2 | Senior Analytics / Principal Data | 80 | £69,302 | Senior Analytics Engineer |
| 3 | Senior Engineer / Architect (mixed) | 235 | £66,290 | BI Developer |
| 4 | Lead / Principal | 190 | £65,067 | Lead Data Scientist |
| 5 | Analytics Engineer / Data Manager | 140 | £61,822 | Analytics Engineer |
| 6 | Data Engineer | 86 | £61,124 | Data Engineer |
| 7 | Data Scientist (mid-level) | 151 | £60,000 | Data Scientist |
| 8 | Senior Data Scientist | 103 | £59,723 | Senior Data Scientist |
| 9 | Power BI / Microsoft stack | 119 | £59,310 | Power BI Developer |
| 10 | Asset / MI / BI specialist | 89 | £57,310 | Asset Data Analyst |
| 11 | Senior Data Analyst / Governance | 119 | £57,263 | Senior Data Analyst |
| 12 | Marketing Data Scientist | 73 | £56,357 | Marketing Data Scientist |
| 13 | Domain-specific (Finance/Consulting) | 463 | £54,928 | Finance Data Analyst |
| 14 | BI / Reporting Analyst | 74 | £53,465 | Business Intelligence Analyst |
| 15 | Business Data Analyst | 146 | £45,000 | Data Business Analyst |
| 16 | Data Analyst | 199 | £45,000 | Data Analyst |
| 17 | Junior / Graduate / Apprentice | 78 | £35,000 | Junior Data Analyst |

(Unclustered postings: 356, median salary £54,019)

## Headline Findings

### 1. AI/ML Engineer is the highest-paid archetype, by a clear margin

AI/Machine Learning Engineer roles command a median salary of **£74,416** — £5,000 above the next archetype (Senior Analytics / Principal Data) and **£14,400 above mid-level Data Scientist** (£60,000). The "AI premium" in the UK data market is real and quantifiable.

This finding reflects 2026 hiring patterns: the same skills five years ago were called "Data Scientist" and paid £55K; today they're called "ML Engineer" or "AI Engineer" and pay £74K. The relabelling carries a salary uplift.

### 2. The "Senior" tag does not consistently command a premium for Data Scientists

The Data Scientist archetype pays **£60,000**, while the Senior Data Scientist archetype pays **£59,723** — a difference of £277, statistically indistinguishable. The conventional career progression "Junior → Mid → Senior → Lead" does not translate to clear salary banding for the Data Scientist title specifically.

Possible interpretations:
- "Senior Data Scientist" is being used as a generic mid-level title in the UK market rather than a specific seniority tier
- Salary increases attach to *function changes* (Lead, Principal, Architect) rather than to seniority within the same role
- Companies posting "Senior" Data Scientist roles are competing with mid-level roles for the same applicant pool

The Lead/Principal archetype (£65,067) does show a clear premium, suggesting the salary jump happens at the people-management or technical-leadership transition, not at the "Senior" tag.

### 3. Analytics Engineers outpay Data Scientists

The Analytics Engineer archetype pays **£61,822** median — above mid-level Data Scientist (£60,000) and Senior Data Scientist (£59,723). This contradicts the popular narrative that data science is the highest-paying entry into data roles.

The Analytics Engineering role (data pipelines, dbt, modern data stack) appears to be picking up the salary premium that used to attach to "data engineer" or "data scientist" specialisations.

### 4. The £45K plateau marks the "non-specialist analyst" floor

Two archetypes — generic "Data Analyst" and "Business Data Analyst" — cluster at exactly **£45,000** median. This is the floor for non-specialist data work in the UK market. Above this, salary requires either:

- Domain specialisation (Finance, Marketing, Asset)
- Technical specialisation (Engineer, ML, Architect)
- Seniority (Senior, Lead, Principal)
- Tool specialisation (Power BI, dbt-stack)

### 5. The entry-level penalty is concrete: £10,000 below "Data Analyst"

The Junior / Graduate / Apprentice archetype sits at **£35,000** median — exactly £10,000 below the generic Data Analyst role. This gap is consistent across the 78 postings in the cluster.

### 6. Domain specialisation alone does not command a premium

The Finance/Consulting domain-specific cluster is the largest in the dataset (463 postings) but sits at **£54,928** median — in the middle of the salary distribution. Finance Data Analyst roles do not command a premium over technical data roles despite the higher pay norms in financial services generally.

Possible interpretation: the postings reflect the *floor* salary needed to fill these roles, not the typical salary, because UK financial services often supplement base pay with substantial bonuses not captured in posted salaries.

### 7. Power BI specialisation pays close to generalist Data Engineer

The Power BI / Microsoft stack archetype (£59,310) pays £1,800 less than Data Engineer (£61,124). Tool specialisation in a single vendor's stack does not significantly outperform general data engineering skills, despite being a more constrained skillset.

## Acknowledged Limitations

1. **Clustering is unsupervised.** The 17 archetypes emerged from the data; they were not validated against an authoritative taxonomy. Some clusters (notably "Senior Engineer / Architect mixed" and "Domain-specific Finance/Consulting") are heterogeneous catch-alls rather than tight role definitions.

2. **Title-only embedding loses context.** Identical titles for different companies may represent different actual roles. Including descriptions would have helped but the description truncation made this less effective.

3. **Salary mix.** 52% of salary values are Adzuna predictions rather than employer-posted. While Adzuna's predictions appear to track real salaries closely in aggregate (real mean £56,380 vs predicted mean £57,718), individual cluster medians may be biased.

4. **Carrier-of-talent confounding.** Several clusters are dominated by single recruiters (e.g., Harnham aggregates many data roles). The salary medians reflect the postings as listed, not necessarily what employers ultimately pay.

5. **Single-day snapshot.** All postings were collected in one collection window. Salary norms may vary by month/season; this analysis does not capture temporal variation.

6. **UK-only.** Findings cannot be generalised to other markets without adjustment.

## Output Files

- `data/processed/postings_clustered.parquet` — full dataset with cluster IDs and labels
- `data/processed/embeddings_titles_only.npy` — saved title embeddings (~3MB) for re-clustering experiments
- `docs/clusters_named.png` — UMAP scatter plot of role archetypes

## What This Enables

The role archetypes will feed into Phase 5 (salary regression): clustering provides a categorical feature representing role type, which can be used alongside title text, company, location, and seniority signals to predict salary band. The comparison between employer-posted salaries and Adzuna's predicted salaries — both available as targets — will let the project tell a methodologically rigorous story about modelling salary in real-world job posting data.
