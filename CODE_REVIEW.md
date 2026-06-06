# Project Review — UK Data Analyst Job Market NLP

Reviewed: 2026-06-06. Scope: README, `docs/`, all four notebooks, processed data,
model-result CSVs, repo hygiene. Numbers below were re-computed from the actual
parquet/CSV files, not taken from the docs.

> **Status — all issues resolved (2026-06-06).** Every item below has been fixed:
> the modelling was re-run leak-free (XGBoost real R² 0.512 → **0.503**, predicted
> 0.368 → **0.377**; CSVs and notebook 04 regenerated), the salary-mix numbers were
> corrected across all three docs (split is **36% real / 64% predicted**), the
> "predictions track real salaries closely" claim was rewritten (real salaries run
> materially higher), `umap-learn` was added to `requirements.txt`, the escaped
> markdown in the Phase 5 doc was fixed, notebooks 1–4 received markdown narration,
> the regex/warnings/hardcoded-summary issues in notebook 4 were cleaned up, and
> `src/` was populated with reusable `features.py` / `junk_filter.py` modules. The
> review text below is retained as a record of what was found and changed.

## Verdict

This is a strong portfolio project. The methodology is sound, the writing is
mature, and the "honest scope adaptation" framing (dropping skill extraction
after finding the API truncation) is exactly the judgment a hiring manager wants
to see. The model results, cluster table, feature importances, and collection
counts I checked all reconcile with the underlying data.

There are, however, **four issues worth fixing before you point a recruiter at
this**: one reproducibility bug, one rendering bug, one methodological flaw in
the modelling, and a set of stale salary-mix numbers that are repeated across
three documents and contradict the data. None are fatal; all are quick fixes.

---

## What I verified as correct

| Claim | Doc value | Recomputed | Status |
|---|---|---|---|
| Raw postings collected | 3,653 | 3,653 | ✅ |
| Clean dataset | 2,835 × 23 | 2,835 × 23 | ✅ |
| Modelling rows | 2,824 | 1,001 real + 1,823 pred = 2,824 | ✅ |
| Unique companies / titles / categories | 1,412 / 1,658 / 25 | 1,412 / 1,658 / 25 | ✅ |
| Junk removed | 497 (220+204+57+16) | sums to 497 | ✅ |
| Cluster median table (all 17 + noise) | — | matches `postings_clustered.parquet` exactly | ✅ |
| Model R²/MAE (real & predicted, all 4 models) | — | matches `model_results_*.csv` exactly | ✅ |
| Feature importances (London #2 real, absent in predicted; senior flags top) | — | matches `feature_importance_*.csv` | ✅ |

The headline salary findings (AI/ML £74,416 top; "Senior" Data Scientist
salary-neutral at £59,723 vs £60,000; Analytics Engineer £61,822 > Data Scientist;
£45K analyst floor) are all reproduced from the data. Good.

---

## Issues to fix

### 1. (High) Stale salary-mix numbers contradict the data — repeated in 3 docs

The docs say the salary split is roughly even and that real ≈ predicted in
aggregate. The data says otherwise.

| Statement | Where | Doc says | Data says |
|---|---|---|---|
| Employer-posted vs Adzuna-predicted split | `data_quality_audit.md` table | 1,355 (47.8%) / 1,480 (52.2%) | **1,012 (35.7%) / 1,823 (64.3%)** |
| "~52% of salary values are Adzuna predictions" | README limitation #3, `role_archetype_findings.md` | 52% | **64%** |
| "Adzuna's predictions track real salaries closely in aggregate (real mean £56,380 vs predicted £57,718)" | `role_archetype_findings.md` finding #3 | means ~£1.3K apart | **real mean ≈ £69,886, predicted ≈ £58,379** (winsorised); medians £60,000 vs £56,751 |

Two consequences:

- The "even split / 52% predicted" figure looks like it came from an earlier
  version of the dataset (before the final dedup/junk filter) and was never
  refreshed. It now appears in three places.
- The "predictions track real salaries closely in aggregate" claim is **not
  supported** — real employer-posted salaries run ~£10–11K higher on the mean
  (~£3K on the median). That is actually an *interesting* finding you're
  currently contradicting: employers who publish real salaries skew toward
  higher-paying/senior roles, or Adzuna systematically under-predicts. Either
  way, rewrite finding #3 to say real salaries are materially higher rather than
  "close," and you turn a wrong sentence into a real insight.

Fix: recompute the split and the means/medians once, then update the audit table,
README limitation #3, and `role_archetype_findings.md` finding #3.

### 2. (High) Data leakage in the modelling cross-validation

In `04_salary_modelling.ipynb`, the feature matrix is built **once on the whole
dataset** — `TfidfVectorizer.fit_transform`, `OneHotEncoder.fit_transform`, and
`StandardScaler.fit_transform` are all fit before `cross_val_score` splits the
data. That means TF-IDF IDF weights, the scaler's mean/std, and the one-hot
vocabulary are learned partly from the validation folds. It's textbook leakage,
and it inflates the reported R²/MAE somewhat.

Additionally, the matrix is fit on the **combined** real+predicted rows and then
masked, so the real-salary model's text/scaling statistics are partly derived
from predicted-salary rows.

Why it matters here: the project's signature finding ("real salaries are *more*
predictable than Adzuna's") is a model-vs-model comparison, and the leakage
affects both targets, so the *direction* of the finding is probably safe. But a
sharp interviewer will spot this immediately, and "I know about leakage and
control for it" is a stronger signal than a slightly higher R².

Fix: wrap preprocessing in `sklearn.pipeline.Pipeline` (or `ColumnTransformer`)
and pass the pipeline to `cross_val_score`, so each fold fits its own
preprocessing on its own training data. Re-run; expect R² to drop a little. The
honest, leak-free number is the better story.

### 3. (Medium) `requirements.txt` is missing `umap-learn`

`03_embeddings_and_clustering.ipynb` does `import umap`, and the Tech Stack
section lists umap-learn, but `umap-learn` is **not** in `requirements.txt`.
Anyone following the "Reproducing the Analysis" steps will `pip install -r
requirements.txt`, then hit `ModuleNotFoundError: No module named 'umap'` at
notebook 3. (`hdbscan`, `sentence-transformers`, `xgboost` are all present —
only umap-learn is missing.)

Fix: add `umap-learn>=0.5` under the "Embeddings & ML" group.

### 4. (Medium) `phase5_salary_modelling_findings.md` has broken markdown

Every heading, bullet, bold marker, and numbered item in that file is
backslash-escaped (`\#`, `\##`, `\- `, `\*\*…\*\*`, `1\.`). On GitHub it renders
as literal `\#` and `\*\*` instead of headers and bold — the one findings doc a
recruiter is most likely to open looks broken next to the other two, which are
clean. The content is fine; only the escaping is wrong.

Fix: strip the leading backslashes (a quick find-replace of `\#`→`#`, `\*`→`*`,
`\-`→`-`, `\|`→`|`, and `^(\d)\\.`→`$1.`), or re-export the file without escaping.

---

## Smaller notes

- **No markdown cells in any notebook.** All four notebooks are 100% code; the
  narrative lives in `docs/`. That's defensible, but reviewers often open the
  notebooks first, and bare code with no explanation undersells the thinking.
  A few markdown cells per notebook (what this phase does / why) would close the
  gap cheaply.
- **`src/` is empty** ("reserved for future utility modules"). An empty reserved
  folder reads aspirational. Either lift the repeated feature-engineering / API
  loop into `src/` (shows you can write reusable modules, not just notebooks) or
  drop the folder.
- **Regex capture groups**: `title.str.contains(r"\b(senior|lead|…)\b")` uses a
  capturing group, which normally throws a pandas UserWarning. It's silenced by
  the global `warnings.filterwarnings("ignore")` at the top of the notebook. Use
  a non-capturing group `(?:…)` and consider removing the blanket warning filter
  so real warnings surface.
- **Hardcoded summary**: cell 11 of notebook 4 prints the findings as literal
  strings (`n=1,001`, `R² = 0.512`, …) rather than reading the computed values.
  That's how the kind of drift in issue #1 creeps in — derive these from
  variables instead.
- **Uncommitted changes**: `git status` shows README, LICENSE, the data
  README/CSVs, and `.gitignore` all modified but not committed. Commit or revert
  so the repo state matches what you describe.
- **`description_length` as a model feature** is near-constant (descriptions are
  truncated to ~75 words), so it contributes mostly noise. Harmless, but you
  could drop it and note why.

---

## Suggested priority order

1. Fix the salary-mix numbers and the "track closely" claim (issue 1) — it's a
   factual error in the part recruiters read.
2. Add `umap-learn` to requirements (issue 3) — one line, unblocks reproduction.
3. Fix the escaped markdown in the phase-5 doc (issue 4) — cosmetic but visible.
4. Re-run the model with a leak-free Pipeline (issue 2) — the most work, but the
   strongest signal of rigor.
5. Add a handful of markdown cells to the notebooks; resolve `src/`.

Items 1–3 are ~30 minutes total. Item 4 is an afternoon and worth it.
