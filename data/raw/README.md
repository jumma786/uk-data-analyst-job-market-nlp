\# Raw Data



This folder contains raw API responses from Adzuna's UK Jobs API.



\## File



`adzuna\_raw\_YYYYMMDD\_HHMMSS.json` — full JSON response from 5 paginated keyword searches across 76 API calls. 3,653 postings before deduplication.



\## Why this file is not in Git



The raw API data is gitignored to:



1\. Respect Adzuna's API terms of service regarding data republishing

2\. Keep the repository lean (data files are regenerable, code is not)

3\. Encourage anyone reproducing this work to run their own collection (Adzuna's catalogue changes daily; this snapshot is from June 2026)



\## How to regenerate



Run `notebooks/01\_data\_collection.ipynb`. Requires an Adzuna API key set in `.env` at the project root.



The 76 API calls use roughly 30% of Adzuna's free-tier daily quota (250 calls).

