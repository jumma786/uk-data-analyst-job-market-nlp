"""Feature-engineering helpers shared across the analysis notebooks.

Kept deliberately dependency-light (pandas / numpy only) so they can be imported
from any notebook without pulling in the modelling stack.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Title tokens that signal seniority / juniority. Used to build binary flags that
# turn out to be the single strongest salary predictors (see Phase 5 findings).
SENIOR_PATTERN = r"\b(?:senior|lead|principal|head|director|manager|chief)\b"
JUNIOR_PATTERN = r"\b(?:junior|graduate|trainee|apprentice|entry)\b"


def extract_region(loc_area) -> str:
    """Return the region from an Adzuna ``location_area`` list.

    Adzuna nests location as ``["UK", "<region>", "<town>", ...]``; the second
    element is the region. Falls back gracefully when the field is missing.
    """
    if not isinstance(loc_area, (list, np.ndarray)):
        return "Unknown"
    if len(loc_area) >= 2:
        return loc_area[1]
    return loc_area[0] if len(loc_area) > 0 else "Unknown"


def add_title_features(df: pd.DataFrame, title_col: str = "title") -> pd.DataFrame:
    """Add title-derived columns: word count and seniority / junior flags.

    Uses non-capturing regex groups so pandas does not emit a match-group warning.
    Returns a copy; does not mutate the input.
    """
    out = df.copy()
    titles = out[title_col].fillna("")
    out["title_word_count"] = titles.str.split().str.len()
    out["title_has_senior"] = titles.str.lower().str.contains(
        SENIOR_PATTERN, regex=True).astype(int)
    out["title_has_junior"] = titles.str.lower().str.contains(
        JUNIOR_PATTERN, regex=True).astype(int)
    return out


def salary_midpoint(df: pd.DataFrame) -> pd.Series:
    """Midpoint of ``salary_min`` and ``salary_max`` (NaN-safe)."""
    return (df["salary_min"] + df["salary_max"]) / 2.0


def apply_salary_outliers(df: pd.DataFrame,
                          low: float = 15_000,
                          cap: float = 200_000,
                          col: str = "salary_midpoint") -> pd.DataFrame:
    """Drop low data-entry errors (< ``low``), winsorise highs at ``cap``, and
    drop rows with no salary. Returns a filtered copy.
    """
    out = df[df[col] >= low].copy()
    out.loc[out[col] > cap, col] = cap
    return out[out[col].notna()].copy()
