# The UK Data Analyst Job Market: An NLP Analysis

An end-to-end NLP project analysing **2,824 UK job postings** for data
roles, collected from the Adzuna API in June 2026. Uses sentence-transformer
embeddings, UMAP dimensionality reduction, and HDBSCAN clustering to
identify role archetypes; uses XGBoost regression to model salary against
posting features.

The project was scoped to answer three questions, then re-scoped to two
after an API data quality finding. The story of how and why this happened
is documented openly in `docs/data_quality_audit.md` — that audit narrative
is itself part of the project.

---

## Headline Findings

1. **AI/ML Engineer is the highest-paid archetype in the UK data market** — median £74,416. £14K above mid-level Data Scientist. The "AI premium" is real and quantifiable.
2. **"Senior Data Scientist" does not pay more than mid-level Data Scientist** — £59,723 vs £60,000. The "Senior" tag is salary-neutral within this role. Salary jumps happen at the Lead/Principal transition (£65K), not at "Senior".
3. **Analytics Engineer (£61,822) outpays Data Scientist (£60,000)** — contradicts the popular narrative about data science being the highest-paying data career.
4. **The £45K plateau marks the non-specialist analyst floor** — generic "Data Analyst" and "Business Data Analyst" cluster at exactly £45K.
5. **Real (employer-posted) salaries are *more* predictable than Adzuna's own predictions** — XGBoost achieves R² 0.512 on real salaries versus 0.368 on Adzuna's predictions. Our features capture more of the real-salary signal than they do of Adzuna's model.
6. **Adzuna's prediction model appears to underweight UK location** — London is the #2 feature for real salaries (4.6% importance) but does not appear in the top 20 features of the model predicting Adzuna's predictions.

Full discussion in `docs/role_archetype_findings.md` and `docs/phase5_salary_modelling_findings.md`.

---

## The Audit Story

The project began with three research questions:

1. What skills are required for UK data analyst roles in 2026?
2. What distinct role archetypes exist beneath the "data analyst" umbrella?
3. How does salary vary by role type and posting characteristics?

After data collection, exploratory analysis surfaced a finding that
forced re-scoping:

**Adzuna's API returns truncated descriptions on the free tier.** Every
posting's description is cut off mid-sentence at approximately 75 words.
This was confirmed by:

- Inspecting description word counts — too uniform a distribution (22-94 words, mean 75.6, std 6.1) to be natural text
- Inspecting the last 80 characters of multiple postings — all end with "..."
- Cross-validating with the Reed API — same truncation pattern confirmed

Full descriptions are gated behind enterprise tiers and were not
obtainable for this project. Rather than pivot to a different data source
or paywall, the project was re-scoped to **drop Question 1** (skill
extraction requires full text) and refocus on the two questions that work
on 75-word openers: role clustering and salary modelling.

This is documented openly. Recruiters reading this README see a project
that adapted honestly to a real-world constraint rather than one that
pretended a constraint did not exist.

---

## Methodology

### Phase 2 — Data Collection

- 3,653 postings collected via Adzuna UK Jobs API
- 5 role-relevant keywords: `data analyst`, `data scientist`, `analytics engineer`, `business intelligence analyst`, `BI developer`
- 76 API calls used (30% of free-tier daily quota)
- Zero collection errors

### Phase 3 — Cleaning and Junk Filter

Deduplication: 3,653 → 3,332 unique postings (321 duplicates from keyword overlap).

**Junk filter removed 497 postings (14.9%):**

- 220 course adverts disguised as job postings (3 known training-course recruiters)
- 204 engineering false positives (Fire Engineer, Structural Engineer — keyword stem-matched "analytics engineer")
- 57 sales false positives
- 16 miscellaneous noise (Employment Adviser, etc.)

Final clean dataset: 2,835 postings × 23 columns.

Outlier handling (before modelling): 8 low outliers removed (< £15K, data entry errors), 6 high outliers capped at £200K (winsorising), 3 missing-salary rows dropped → **2,824 modelling rows**.

### Phase 4 — Embeddings and Clustering

- Sentence embeddings with `all-MiniLM-L6-v2` (384-dim)
- Title-only embedding (not title + description) — description snippets too uniform in language to drive separation
- UMAP reduction (`n_neighbors=15`, `min_dist=0.1`, cosine metric)
- HDBSCAN clustering (`min_cluster_size=50`, `min_samples=10`)
- Result: **17 interpretable role archetypes** + 12.6% noise

The clustering went through three iterations before producing this result. First attempt (title + description, default UMAP) produced 3 clusters with one containing 84% of the data — too coarse. Second attempt (tight parameters) produced 52 micro-clusters — too fragmented. Third attempt (title-only embedding, default parameters) produced the 17-cluster result used in the analysis.

This iteration is normal in unsupervised work and is documented honestly.

### Phase 5 — Salary Modelling

Two regression models trained side by side:

- **Real (employer-posted) salaries**: 1,001 postings, target = salary_midpoint
- **Adzuna predicted salaries**: 1,823 postings, target = salary_midpoint

Features: 267 columns across three groups:

- 62 categorical (cluster, region, category, contract type, contract time) — one-hot encoded
- 200 text features — TF-IDF on title text, 1-2 word n-grams, min_df=5
- 5 numeric — title word count, seniority flags, description length, n_keywords_matched

Four models compared with 5-fold cross-validation:

| Model | Real R² | Real MAE | Adzuna R² | Adzuna MAE |
|---|---:|---:|---:|---:|
| Baseline (predict mean) | -0.011 | £28,280 | -0.008 | £13,039 |
| Ridge Regression | 0.459 | £19,502 | 0.357 | £10,044 |
| Random Forest | 0.495 | £17,123 | 0.354 | £10,018 |
| **XGBoost** | **0.512** | **£16,925** | **0.368** | **£9,730** |

XGBoost won both targets, but only marginally. Random Forest barely beats Ridge, indicating most of the salary signal is linear.

The XGBoost real-salary MAE of £16,925 is appropriate for understanding salary drivers, not for individual career advice. Anyone considering a £60K role would want predictions accurate to £2-3K, not £17K. The model is honest about what it can and cannot tell you.

---

## Repository Structure

```
UK-Job-Postings-NLP/
├── README.md
├── requirements.txt
├── .gitignore
├── .env                          # Adzuna credentials (gitignored)
├── data/
│   ├── raw/                      # Raw Adzuna API responses (gitignored)
│   └── processed/                # Cleaned + clustered datasets, embeddings
├── notebooks/
│   ├── 01_data_collection.ipynb       # Adzuna API → raw JSON
│   ├── 02_data_exploration.ipynb      # Cleaning, junk filter, audit work
│   ├── 03_embeddings_and_clustering.ipynb  # Sentence transformers → UMAP → HDBSCAN
│   └── 04_salary_modelling.ipynb      # Feature engineering, XGBoost
├── docs/
│   ├── data_quality_audit.md          # Audit narrative + truncation finding
│   ├── role_archetype_findings.md     # 17 archetypes + salary hierarchy
│   ├── phase5_salary_modelling_findings.md  # Model comparison + feature importance
│   ├── clusters_named.png             # UMAP scatter of role archetypes
│   └── umap_by_category.png           # UMAP scatter by Adzuna category
└── src/                                # (reserved for future utility modules)
```

---

## Reproducing the Analysis

### Prerequisites

- Python 3.11+
- Free Adzuna API credentials from https://developer.adzuna.com (`app_id` and `app_key`)
- Approximately 3 GB of disk space (PyTorch via sentence-transformers)

### Setup

```bash
git clone https://github.com/jumma786/uk-data-analyst-job-market-nlp.git
cd uk-data-analyst-job-market-nlp
pip install -r requirements.txt
```

### Configure credentials

Create a `.env` file in the repo root:

```
ADZUNA_APP_ID=your_id_here
ADZUNA_APP_KEY=your_key_here
```

### Run the notebooks

Run in order:

1. `01_data_collection.ipynb` — collects 3,653 postings via 76 API calls (~5 minutes)
2. `02_data_exploration.ipynb` — cleans and filters down to 2,835 postings
3. `03_embeddings_and_clustering.ipynb` — embeds and clusters (~5 minutes including sentence-transformer model download)
4. `04_salary_modelling.ipynb` — trains 4 models on 2 targets with 5-fold CV (~5 minutes)

The Adzuna API returns live data, so your collection results will not match this README's exact numbers. The methodology and code are reproducible; the specific findings reflect the UK market on 03 June 2026.

---

## Tech Stack

- **Data collection**: requests, python-dotenv, Adzuna UK Jobs API
- **Processing**: pandas, numpy, scikit-learn
- **NLP**: sentence-transformers (all-MiniLM-L6-v2)
- **Dimensionality reduction**: umap-learn
- **Clustering**: hdbscan
- **Regression**: scikit-learn (Ridge, Random Forest, DummyRegressor), XGBoost
- **Visualisation**: matplotlib

---

## Acknowledged Limitations

This project is honest about what it can and cannot show:

1. **Truncated descriptions.** Analysis works on 75-word opener snippets. Skill extraction was dropped because it requires full text.
2. **Single-day snapshot.** Data was collected on 03 June 2026. Seasonal/monthly variation not captured.
3. **Salary mix.** 52% of salary values are Adzuna predictions; the analysis explicitly distinguishes between these and employer-posted figures.
4. **MAE of £17K** on the real-salary model means predictions are useful for analytical insight, not individual career advice.
5. **17 clusters are unsupervised.** They were not validated against an authoritative role taxonomy. Some clusters are catch-alls (notably "Domain-specific Finance/Consulting" at 463 postings).
6. **UK-only.** Findings cannot be generalised beyond the UK market.
7. **Feature importance from XGBoost is noisy** with 267 features. Importance rankings should be read directionally rather than precisely.

---

## What This Project Demonstrates

For someone reviewing this as part of a job application, this project shows:

- **API-based data collection** with rate limiting, error handling, and credentials management
- **Real-world data quality audit work** — identifying and documenting issues (truncation, junk, outliers) rather than hiding them
- **Honest scope adaptation** — when an API limitation invalidated one of three research questions, the project re-scoped openly rather than fabricating workarounds
- **Sentence-transformer embeddings** for text representation
- **Unsupervised clustering** (UMAP + HDBSCAN) with iterative parameter tuning
- **Multi-model regression comparison** (baseline → linear → tree → boosted) with proper 5-fold cross-validation
- **Methodological self-criticism** — the counter-intuitive finding that real salaries are more predictable than Adzuna's predictions is highlighted rather than buried
- **End-to-end reproducibility** — anyone with an Adzuna account can re-run the entire pipeline from these notebooks

---

## Author

Jumma Mohammad Teli — Data Analyst, Birmingham, UK.

[LinkedIn](https://linkedin.com/in/jumma-mohammad) · [GitHub](https://github.com/jumma786) · jummamohammad477@gmail.com

## License

MIT
