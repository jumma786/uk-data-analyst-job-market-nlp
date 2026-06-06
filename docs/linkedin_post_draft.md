# LinkedIn post — draft

> Draft only — not part of the analysis. Delete or gitignore before pushing if you
> don't want it in the repo. Swap in your real GitHub/dashboard links before posting.

---

## Main version (~280 words)

I analysed 2,835 UK data-role job postings to answer a simple question: what actually moves salary in the data job market? A few findings surprised me.

𝗔𝗜 is the premium, and it's real. "AI / Machine Learning Engineer" is the highest-paid archetype at a £74,416 median — £14K above a mid-level Data Scientist. The same skills that were "Data Science" five years ago now carry an AI label and a pay rise.

"𝗦𝗲𝗻𝗶𝗼𝗿" 𝗶𝘀𝗻'𝘁 𝘄𝗵𝗲𝗿𝗲 𝘁𝗵𝗲 𝗺𝗼𝗻𝗲𝘆 𝗷𝘂𝗺𝗽𝘀. "Senior Data Scientist" (£59,723) pays essentially the same as mid-level Data Scientist (£60,000). The real step-up happens at Lead/Principal (£65K) — the title that matters is the one that changes your function, not the one that adds "Senior".

𝗔𝗻𝗮𝗹𝘆𝘁𝗶𝗰𝘀 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿 (£61,822) 𝗼𝘂𝘁𝗽𝗮𝘆𝘀 𝗗𝗮𝘁𝗮 𝗦𝗰𝗶𝗲𝗻𝘁𝗶𝘀𝘁. The modern data stack is quietly picking up the premium data science used to own.

And the part I'm proudest of: I tried to model salary honestly. A leak-free XGBoost explains ~50% of real employer-posted salaries — and SHAP shows the single biggest driver is **location**: being in London swings a prediction by ~£9K on average. (It's also the signal Adzuna's own salary estimates seem to underweight.)

The honest caveat: the model is off by ~£17K on average, so it's a lens for understanding drivers, not career advice. And one of my three original questions — skill extraction — had to be dropped when I discovered the API truncates descriptions. I documented that pivot openly rather than pretending it didn't happen.

Full write-up, interactive dashboard, and reproducible notebooks 👇
[GitHub link]

#DataAnalytics #DataScience #NLP #MachineLearning #UKJobs #Python

---

## Short / punchy version (~120 words)

I scraped and analysed 2,835 UK data job postings. The salary story isn't what the careers advice says:

→ AI/ML Engineer tops the market at £74,416 — the "AI premium" is real (+£14K vs Data Scientist)
→ "Senior" Data Scientist pays the same as mid-level (£59.7K vs £60K). The jump is at Lead/Principal.
→ Analytics Engineer (£61.8K) outpays Data Scientist
→ Generic "Data Analyst" sits at a hard £45K floor

The methodology nerd in me: a leak-free model explains ~50% of real salaries, and SHAP says **location** is the #1 driver — London is worth ~£9K. One of my three original questions got cut when I found the API truncates descriptions; I documented the pivot instead of hiding it.

Notebooks + interactive dashboard 👇
[GitHub link]

#DataAnalytics #DataScience #Python #NLP

---

## Alternative hooks (first line A/B options)

- "The careers advice says data science is the highest-paying data job. 2,835 UK postings say otherwise."
- "I built a salary model good enough to be useful and honest enough to tell you when it isn't."
- "'Senior Data Scientist' and 'Data Scientist' pay the same in the UK. I have the data."
- "What's a London postcode worth on a UK data salary? About £9,000."

## Posting tips

- Lead with one hook line, then a blank line — LinkedIn truncates after ~3 lines, so the hook must earn the "see more" click.
- Put the GitHub/dashboard link as the first comment as well; in-body links can suppress reach.
- The bold/underlined characters above are Unicode (𝗯𝗼𝗹𝗱) so they survive LinkedIn's plain-text editor. Use sparingly.
- Best to attach the dashboard thumbnail or the SHAP plot as the post image.

---

# Audience-tailored versions

Two rewrites of the same project for two different feeds. Pick based on who you most
want to reach — or post the recruiter version now and the peer version a week later with
a different angle.

## A. For recruiters & hiring managers (~250 words)

What does a Data Analyst actually do when the data fights back? I built a project to show you.

I set out to analyse the UK data job market from 2,835 live postings. Three questions: what skills are in demand, what role types exist, and what drives salary. Partway in, I found the data source truncates every job description — so my skills question was no longer answerable honestly. Rather than fudge it, I re-scoped the project, documented exactly why, and delivered the two questions the data *could* support. That decision is the part I'd want a hiring manager to read first.

What the finished analysis shows about the market:
• AI/ML Engineer is the top-paid role (£74,416 median) — the AI premium is real
• "Senior Data Scientist" pays the same as mid-level; the salary jump is at Lead/Principal
• Generic "Data Analyst" sits at a firm £45K floor
• Location is the single biggest salary driver — a London role is worth ~£9K

What it shows about how I work: I collect data responsibly (rate-limited API, error handling), I audit it before trusting it, I model carefully (no data leakage, honest accuracy caveats), and I communicate findings in plain English with an interactive dashboard a non-technical stakeholder can read.

I'm a Data Analyst in Birmingham, open to roles where that mix of rigour and clarity is useful.

Project, dashboard and notebooks 👇
[GitHub link]

#DataAnalytics #Hiring #OpenToWork #DataScience #Python

## B. For data peers & practitioners (~260 words)

A methodology result that genuinely surprised me: real employer-posted salaries were *more* predictable than the job board's own salary estimates.

Setup: 2,835 UK data postings, title embeddings (all-MiniLM-L6-v2) → UMAP → HDBSCAN for 17 role archetypes, then two XGBoost salary models — one on employer-posted salaries, one on the platform's predicted salaries.

The findings worth arguing about:

1) Leak-free CV matters. My first pass fit TF-IDF + scaling on the full set before splitting — classic leakage. Wrapping preprocessing in a Pipeline so it fits per-fold dropped R² by ~1–2 points. The honest number (real R² ≈ 0.50, predicted ≈ 0.38) is the one I kept.

2) Real > predicted predictability. Our features explain ~50% of real-salary variance but only ~38% of the platform's own predictions — its model clearly uses signals we don't have.

3) SHAP > gain importance for this. Tree-gain ranked a noisy "12-month FTC" token #1; SHAP (in £) ranked London #1 at ~£9K average impact, contractor status next, then "analyst" pulling pay *down*. The platform's predicted-salary model, notably, underweights London entirely.

4) Log target: small win, mostly for the linear model (Ridge MAE £20,078 → £19,129); XGBoost barely moved — it already handles the skew.

Caveats I'd want torn apart: single-day snapshot, 64% of salaries are platform estimates, MAE ~£17K, clusters unvalidated against a taxonomy.

Notebooks are reproducible — would love a second pair of eyes on the leakage and SHAP choices.
[GitHub link]

#DataScience #MachineLearning #MLOps #NLP #Python #SHAP
