"""Reusable utilities for the UK Data Analyst Job Market NLP project.

These functions are the shared logic behind the notebooks (junk filtering,
title/region feature engineering, salary outlier handling). They live here so the
same definitions can be imported rather than copy-pasted across notebooks.
"""

from .features import (
    extract_region,
    add_title_features,
    salary_midpoint,
    apply_salary_outliers,
)
from .junk_filter import is_junk, COURSE_RECRUITERS

__all__ = [
    "extract_region",
    "add_title_features",
    "salary_midpoint",
    "apply_salary_outliers",
    "is_junk",
    "COURSE_RECRUITERS",
]
