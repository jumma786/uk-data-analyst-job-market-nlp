# Data Collection & Quality Audit

Generated: 2026-06-03

## Collection Summary

Source: Adzuna UK Jobs API (free tier)
Strategy: Single-day bulk collection, 5 role-relevant keywords, paginated to API maximum.

| Keyword | Postings collected |
|---|---|
| data analyst | 1,000 (Adzuna page limit reached) |
| data scientist | 1,000 (Adzuna page limit reached) |
| analytics engineer | 1,000 (Adzuna page limit reached) |
| business intelligence analyst | 86 (exhausted) |
| BI developer | 567 (exhausted) |
| **Total raw** | **3,653** |

API calls made: 76 / 250 daily quota (30.4%).
Zero collection errors.

## Deduplication

3,653 raw postings → **3,332 unique postings** (321 duplicates removed).
Duplicates occurred where a posting matched multiple search keywords. The keyword overlap itself was preserved as a feature (`found_under_keywords`, `n_keywords_matched`).

## Critical Data Quality Finding: Description Truncation

Both Adzuna and Reed APIs return only the *opening snippet* of each job posting on their standard tiers — approximately 75-100 words per posting, ending mid-sentence with an ellipsis.

Full descriptions are gated behind enterprise tiers and were not obtainable for this project. This finding was confirmed by:

1. Inspecting Adzuna description length distribution (uniform 22-94 word range, mean 75.6, std 6.1 — too uniform for real text).
2. Inspecting trailing characters (every description ends with "...").
3. Cross-validating with Reed API (same truncation pattern: 72-word snippets).

### Scope Implication

The project was originally scoped around three questions: skill extraction, role clustering, and salary prediction. The truncation finding required scoping out the **skill extraction** question (skill lists typically appear deeper in job posts than the first 80 words). The final project focuses on:

- Role archetype clustering (works on snippets — they carry tone, positioning, target audience signal)
- Salary patterns by role type and posting characteristics

The README explicitly names this limitation rather than concealing it.

## Junk Detection & Removal

After deduplication, 497 of 3,332 postings (14.9%) were identified as non-data postings and removed.

### Categories of junk identified

**1. Course advertisers posing as job postings (220 postings, 6.6%)**

Three companies — **IT Career Switch**, **ITOL Recruit**, and **IT Online Learning** — flooded Adzuna with advertorials disguised as job posts. All open with sales-pitch language ("Are you looking to benefit from a new career in Data Analysis?") rather than employer language. Titles often contained "Trainee" or "No Experience Needed". Quantitatively obvious: these three companies alone posted 220 listings, more than the next legitimate company by an order of magnitude.

**2. Engineering keyword false positives (204 postings, 6.1%)**

Adzuna's full-text search matched "analytics **engineer**" against "Fire **Engineer**", "Structural **Engineer**", "Quality **Engineer**", etc. Removed where category was "Engineering Jobs" AND title contained no data-related terms.

**3. Sales keyword false positives (57 postings, 1.7%)**

Sales roles mentioning "data" or "analytics" peripherally (e.g., "Sales Specialist – Analytical Instruments", "Recruitment Manager"). Removed where category was "Sales Jobs" AND title contained no genuine data role terms.

**4. Other identified noise (16 postings, 0.5%)**

Including 16 "Employment Adviser" roles that matched "BI developer" via "Business Intelligence" appearing in their descriptions, and 12 "Principal Fire Engineer" roles.

### Filter logic (documented in code)

```python
def is_junk(row):
    # Filter 1: Known course-advertising recruiters
    if row["company_name"] in ["IT Career Switch", "ITOL Recruit", "IT Online Learning"]:
        return True

    # Filter 2: Engineering Jobs without data-related title terms
    if row["category_label"] == "Engineering Jobs":
        title_lower = str(row["title"]).lower()
        if not any(term in title_lower for term in ["analytics", "data", "analyst", "scientist", "business intelligence", "bi developer"]):
            return True

    # Filter 3: Sales Jobs without data role title terms
    if row["category_label"] == "Sales Jobs":
        title_lower = str(row["title"]).lower()
        if not any(term in title_lower for term in ["analytics", "data scientist", "data analyst"]):
            return True

    # Filter 4: Specific noise titles identified during exploration
    if row["title"] in ["Employment Adviser", "Principal Fire Engineer"]:
        return True

    return False
```

## Final Analytical Dataset

| Metric | Value |
|---|---|
| Unique postings | 2,835 |
| Unique companies | 1,412 |
| Unique titles | 1,658 |
| Categories represented | 25 |
| Postings with employer-posted salary | 1,012 (35.7%) |
| Postings with Adzuna-predicted salary | 1,823 (64.3%) |
| Date range | All collected in single window, 03 June 2026 |

Output file: `data/processed/postings_clean.parquet` (820 KB)

## Documented Methodological Caveats

1. **Single-day snapshot.** The dataset reflects UK Adzuna's active listings on one date. Seasonal or weekly variation is not captured.
2. **Truncated descriptions.** Analysis works on ~75-word snippets, not full posts.
3. **Salary mix.** ~64% of salary values are Adzuna predictions, not employer-posted. Analysis distinguishes between these.
4. **Recruiter aggregator bias.** ~10% of postings come from data-specialist recruiter Harnham, who aggregate roles across many employers. These were retained as legitimate but represent recruiter coverage, not raw employer demand.
