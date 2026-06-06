"""Junk-posting filter used in Phase 3 cleaning.

Removes course adverts disguised as jobs and keyword false positives (engineering /
sales roles that stem-matched the search terms). Documented in
``docs/data_quality_audit.md``.
"""
from __future__ import annotations

# Three recruiters that flood Adzuna with training-course advertorials posing as
# job postings. They alone accounted for ~220 of the removed listings.
COURSE_RECRUITERS = ("IT Career Switch", "ITOL Recruit", "IT Online Learning")

_DATA_TITLE_TERMS = ("analytics", "data", "analyst", "scientist",
                     "business intelligence", "bi developer")
_DATA_ROLE_TERMS = ("analytics", "data scientist", "data analyst")
_NOISE_TITLES = ("Employment Adviser", "Principal Fire Engineer")


def is_junk(row) -> bool:
    """Return True if a posting should be removed as non-data junk.

    Mirrors the filter logic in notebook 02. Expects a mapping/Series with
    ``company_name``, ``category_label`` and ``title`` keys.
    """
    if row["company_name"] in COURSE_RECRUITERS:
        return True

    title = str(row["title"]).lower()

    # Engineering false positives ("Fire Engineer" etc.) with no data term in title
    if row["category_label"] == "Engineering Jobs" and not any(
            t in title for t in _DATA_TITLE_TERMS):
        return True

    # Sales false positives with no genuine data-role term in title
    if row["category_label"] == "Sales Jobs" and not any(
            t in title for t in _DATA_ROLE_TERMS):
        return True

    if row["title"] in _NOISE_TITLES:
        return True

    return False
