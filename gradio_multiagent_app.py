# ---- extracted from notebook cell 1 ----
# Standard library
import io
import json
import math
import os
import re
import sys
import traceback
import unicodedata
from typing import Any, Callable, Iterable, Optional
from datetime import date
import concurrent.futures

# Data & ML
import numpy as np  
import pandas as pd
from scipy import stats

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

# Visualization
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import seaborn as sns

# App / API
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI


# ---- extracted from notebook cell 286 ----
load_dotenv()

MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MISTRAL_API_KEY  = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL    = "mistral-small-latest"

_client = OpenAI(base_url=MISTRAL_BASE_URL, api_key=MISTRAL_API_KEY)

# Paths 
PROJECT_ROOT = os.getcwd()
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
ALLARMI_CSV = os.path.join(RAW_DIR, "ALLARMI.csv")
TIPOLOGIA_CSV = os.path.join(RAW_DIR, "TIPOLOGIA_VIAGGIATORE.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
FINDINGS_JSON = os.path.join(OUTPUT_DIR, "findings.json")
COLUMN_PROFILES_JSON = os.path.join(OUTPUT_DIR, "column_profiles.json")
CLEANING_PLAN_JSON   = os.path.join(OUTPUT_DIR, "cleaning_plan.json")   # NEW: slim JSON for cleaning agent
SCOPE_MANIFEST_JSON = os.path.join(OUTPUT_DIR, "scope_manifest.json")

# Profiling 
DOMINANT_FORMAT_SAMPLE_SIZE = 200


# ---- extracted from notebook cell 288 ----
DEFAULT_CLEANING_MISSING_TOKENS = {
    "", " ", "na", "n/a", "null", "none", "nan", "unknown", "undefined",
    "-", "--", "not available", "missing", "n.d.", "nd"
}


def _strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _collapse_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def to_snake_case(name: str) -> str:
    name = "" if name is None else str(name)
    name = _strip_accents(name).strip()

    # Separate camelCase / PascalCase boundaries
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)

    # Replace non-alphanumeric runs with underscore
    name = re.sub(r"[^0-9A-Za-z]+", "_", name)

    # Collapse underscores and trim
    name = re.sub(r"_+", "_", name).strip("_").lower()

    if not name:
        name = "unnamed_column"

    # If the name starts with a digit, prefix it to keep it identifier-like
    if re.match(r"^\d", name):
        name = f"col_{name}"

    return name


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [to_snake_case(col) for col in out.columns]
    return out


def deduplicate_column_names(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    seen = {}
    new_cols = []

    for col in out.columns:
        if col not in seen:
            seen[col] = 0
            new_cols.append(col)
        else:
            seen[col] += 1
            new_cols.append(f"{col}__{seen[col]}")

    out.columns = new_cols
    return out


def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().copy()


def standardize_missing_values(
    df: pd.DataFrame,
    missing_tokens: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    out = df.copy()
    tokens = {str(x).strip().lower() for x in (missing_tokens or DEFAULT_CLEANING_MISSING_TOKENS)}

    for col in out.columns:
        out[col] = out[col].apply(
            lambda x: pd.NA
            if isinstance(x, str) and x.strip().lower() in tokens
            else x
        )
    return out


def normalize_text_values(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    def _norm(x):
        if pd.isna(x):
            return x
        if isinstance(x, str):
            return _collapse_spaces(x).lower()
        return x

    for col in out.columns:
        out[col] = out[col].apply(_norm)

    return out


def load_cleaning_plan(plan_json_path: str, dataset_key: str) -> dict:
    with open(plan_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(dataset_key, {})


# ---- extracted from notebook cell 290 ----
COLUMN_ROLES = {

    # numeric
    "identifier_numeric",   # numeric IDs without arithmetic meaning (preserve as string to keep leading zeros)
    "count",                # non-negative integer counts (e.g. number of flights)
    "measure",              # continuous measurements (weight, distance, price)
    "percentage",           # percentage value
    "year",                 # year (e.g. 2024)
    "month_number",         # month as 01-12
    "day_number",           # day as 01-31

    # string / code
    "identifier",           # generic identifier (could be alphanumeric)
    "category",             # categorical variable (e.g. "low", "medium", "high")
    "free_text",            # free text / operator notes
    "flag_binary",          # binary flag (yes/no, 0/1, alto/basso)

    # temporal
    "date",                 # date without time
    "datetime",             # date + time

    # special
    "unknown",              # LLM cannot classify
}


ROLE_TO_EXPECTED_DTYPE = {
    "identifier_numeric": "string",      # keep as string to preserve leading zeros
    "count":              "Int64",       # nullable integer
    "measure":            "Float64",     # nullable float
    "percentage":         "Float64",
    "year":               "Int64",
    "month_number":       "Int64",
    "day_number":         "Int64",

    "identifier":         "string",
    "category":           "string",
    "free_text":          "string",
    "flag_binary":        "string",

    "date":               "datetime64[ns]",
    "datetime":           "datetime64[ns]",

    "unknown":            "string",      # safe default
}


def resolve_expected_dtype(role: str) -> str:
    if role in ROLE_TO_EXPECTED_DTYPE:
        return ROLE_TO_EXPECTED_DTYPE[role]
    if isinstance(role, str) and role.startswith("custom:"):
        return "string"
    return "string"


# ---- extracted from notebook cell 292 ----
def _to_native(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _to_native(v) for k, v in value.items()}
    if isinstance(value, (np.ndarray, list, tuple)):
        return [_to_native(v) for v in value]
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        if math.isnan(float(value)):
            return None
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value


def _safe_load_json(path: str) -> dict:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _safe_write_json(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_to_native(data), f, ensure_ascii=False, indent=2)


# ---- extracted from notebook cell 294 ----
def get_dataframe_shape(df: pd.DataFrame) -> dict:
    rows, cols = df.shape
    return {"rows": int(rows), "columns": int(cols)}


def get_dataframe_dtypes(df: pd.DataFrame) -> dict:
    return {col: str(dtype) for col, dtype in df.dtypes.items()}


def get_column_missing_stats(df: pd.DataFrame) -> dict:
    result = {}
    for col in df.columns:
        mask = df[col].isna()
        result[col] = {
            "null_count": int(mask.sum()),
            "non_null_count": int((~mask).sum()),
            "missing_percentage": round(float(mask.mean() * 100), 2),
        }
    return result


# ---- extracted from notebook cell 296 ----
def _value_format_label(value: Any) -> str:
    if value is None:
        return "missing"

    s = str(value).strip()

    if s == "":
        return "empty"

    if s.isdigit():
        return "digit"

    try:
        float(s.replace(",", "."))
        return "float"
    except Exception:
        pass

    if s.isalpha():
        return "alpha"

    has_alpha = any(c.isalpha() for c in s)
    has_digit = any(c.isdigit() for c in s)
    if has_alpha and has_digit:
        return "alphanumeric"

    return "generic"


def detect_dominant_format(
    series: pd.Series,
    sample_size: int = DOMINANT_FORMAT_SAMPLE_SIZE,
) -> dict:

    head_sample = series.head(sample_size)
    clean = head_sample.dropna()

    if clean.empty:
        return {
            "label": None,
            "share_pct": 0.0,
            "sample_size": 0,
        }

    labels = clean.map(_value_format_label)
    counts = labels.value_counts(dropna=False)
    total = int(counts.sum())

    return {
        "label": str(counts.index[0]),
        "share_pct": round(float(counts.iloc[0] / total * 100), 2),
        "sample_size": total,
    }


def collect_non_conforming_samples(
    series: pd.Series,
    dominant_label: str,
    sample_size: int = DOMINANT_FORMAT_SAMPLE_SIZE,
    max_samples: int = 100,
) -> dict:

    head_sample = series.head(sample_size)
    clean = head_sample.dropna()

    if clean.empty or dominant_label is None:
        return {"share_pct": 0.0, "samples": []}

    labels = clean.map(_value_format_label)
    non_conforming_mask = labels != dominant_label
    non_conforming_values = clean.loc[non_conforming_mask]

    total = int(len(clean))
    n_non_conforming = int(non_conforming_mask.sum())

    unique_samples = []
    for v in non_conforming_values.tolist():
        native_v = _to_native(v)
        if native_v not in unique_samples:
            unique_samples.append(native_v)
        if len(unique_samples) >= max_samples:
            break

    return {
        "share_pct": round(float(n_non_conforming / total * 100), 2) if total else 0.0,
        "samples": unique_samples,  
    }


def _try_numeric(series: pd.Series) -> pd.Series:

    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")

    s = series.astype("string").str.strip()
    s = s.str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


# ---- extracted from notebook cell 298 ----
TRANSFORMATION_ACTIONS = {
    "none",        # all values already conform
    "extract",     # extract substring matching a pattern (params: regex)
    "map",         # map non-conforming values to canonical ones (params: mapping, canonical_values)
    "set_null",    # explicitly null out broken placeholders
}


def _build_enrichment_prompt(deterministic_profile: dict) -> str:
    return f"""
You are a data profiling assistant.

Given the deterministic profile of ONE column, enrich it with:
1. a ROLE from the closed vocabulary
2. a declarative TRANSFORMATION_RULE
3. a brief human-readable DESCRIPTION

ROLES:
{sorted(COLUMN_ROLES)}

If none fits, return "custom:<short_snake_case_name>".

ROLE TO EXPECTED DTYPE:
{json.dumps(ROLE_TO_EXPECTED_DTYPE, indent=2)}

TRANSFORMATION ACTIONS:
{sorted(TRANSFORMATION_ACTIONS)}

A transformation_rule MUST have this structure:
{{
  "action": "<one of the actions above>",
  "target_format": "<expected value format>",
  "params": {{...}},
  "description": "<what the rule does>"
}}

Params examples:
- extract: {{"regex": "\\\\d+"}}
- map: {{"mapping": {{"<raw_value>": "<canonical_value>"}}, "canonical_values": ["<canonical_value>"]}}
- set_null: {{}}
- none: {{}}

Infer params from sample values and non-conforming samples.
Do NOT assume a fixed format.

NUMERIC SUMMARY ANALYSIS:
If "numeric_summary" exists, use it.
Non-conforming samples detect format anomalies, not numerically implausible values.

Expected ranges:
- year: 1900-2100
- month_number: 1-12
- day_number: 1-31
- count: >= 0
- percentage: 0-100
- measure: reason from mean and median

If min or max fall outside the expected range:
- use "extract" only if the invalid value appears recoverable
- use "set_null" if it cannot be recovered
- never use "map" for numerically implausible values

COLUMN PROFILE:
{json.dumps(deterministic_profile, ensure_ascii=False, indent=2)}

Return ONLY a JSON object with EXACTLY these keys:
{{
  "role": "<role from vocabulary or custom:...>",
  "transformation_rule": {{...}},
  "description": "<1-2 sentences>"
}}
""".strip()


def _parse_llm_enrichment_response(response_text: str) -> dict:
    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _fallback_enrichment(deterministic_profile: dict, error: str) -> dict:
    return {
        "role": "unknown",
        "role_source": "fallback",
        "expected_dtype": "string",
        "transformation_rule": {
            "action": "none",
            "target_format": deterministic_profile.get("dominant_format", {}).get("label"),
            "params": {},
            "description": "Fallback: no transformation applied (LLM enrichment failed).",
        },
        "description": f"LLM enrichment failed: {error}",
    }


def _validate_and_fix_enrichment(
    enrichment: dict,
    deterministic_profile: dict,
) -> dict:
    fixes = []

    role = enrichment.get("role", "unknown")
    expected_dtype = enrichment.get("expected_dtype")
    rule = enrichment.get("transformation_rule") or {}
    action = rule.get("action", "none")
    params = rule.get("params") or {}

    dominant = (deterministic_profile.get("dominant_format") or {}).get("label")
    dominant_share = (deterministic_profile.get("dominant_format") or {}).get("share_pct", 0)

    NUMERIC_ROLES = {
        "identifier_numeric", "count", "measure", "percentage",
        "year", "month_number", "day_number",
    }
    if dominant in {"alpha", "generic"} and dominant_share >= 80 and role in NUMERIC_ROLES:
        n_unique = deterministic_profile.get("n_unique_non_null", 0)
        row_count = deterministic_profile.get("row_count", 1)
        unique_ratio = n_unique / max(row_count, 1)

        new_role = "category" if unique_ratio < 0.05 else "free_text"
        new_dtype = resolve_expected_dtype(new_role)

        fixes.append(
            f"role '{role}' is numeric but dominant_format is '{dominant}' at "
            f"{dominant_share}% (textual evidence overrides). "
            f"Reassigned to '{new_role}', dtype to '{new_dtype}'."
        )
        role = new_role
        expected_dtype = new_dtype
        action = "none"
        params = {}

    fixed_rule = {
        "action": action,
        "target_format": rule.get("target_format", dominant),
        "params": params,
        "description": rule.get("description", ""),
    }

    out = dict(enrichment)
    out["role"] = role
    out["expected_dtype"] = expected_dtype
    out["transformation_rule"] = fixed_rule
    if fixes:
        out["validator_fixes"] = fixes
    return out


def enrich_column_profile_with_llm(
    deterministic_profile: dict,
    llm_callable: Optional[Callable[[str], str]] = None,
) -> dict:
    if llm_callable is None:
        return _fallback_enrichment(deterministic_profile, "no llm_callable provided")

    prompt = _build_enrichment_prompt(deterministic_profile)

    try:
        raw = llm_callable(prompt)
        parsed = _parse_llm_enrichment_response(str(raw))
    except Exception as e:
        return _fallback_enrichment(deterministic_profile, str(e))

    # Validate role
    role = parsed.get("role", "unknown")
    if role in COLUMN_ROLES:
        role_source = "llm"
    elif isinstance(role, str) and role.startswith("custom:"):
        role_source = "custom"
    else:
        role = "unknown"
        role_source = "fallback"

    expected_dtype = resolve_expected_dtype(role)

    rule = parsed.get("transformation_rule") or {}
    if not isinstance(rule, dict) or rule.get("action") not in TRANSFORMATION_ACTIONS:
        rule = {
            "action": "none",
            "target_format": deterministic_profile.get("dominant_format", {}).get("label"),
            "params": {},
            "description": "LLM returned an invalid transformation_rule; defaulted to 'none'.",
        }
    rule.setdefault("params", {})
    rule.setdefault("target_format", deterministic_profile.get("dominant_format", {}).get("label"))
    rule.setdefault("description", "")

    enrichment = {
        "role": role,
        "role_source": role_source,
        "expected_dtype": expected_dtype,
        "transformation_rule": rule,
        "description": str(parsed.get("description", "")).strip(),
    }

    enrichment = _validate_and_fix_enrichment(enrichment, deterministic_profile)
    return enrichment


# ---- extracted from notebook cell 300 ----
def profile_single_column(
    df: pd.DataFrame,
    column_name: str,
    llm_callable: Optional[Callable[[str], str]] = None,
    sample_size: int = DOMINANT_FORMAT_SAMPLE_SIZE,
) -> dict:
    series = df[column_name]
    non_missing = series.dropna()

    sample_values = [_to_native(v) for v in non_missing.head(5).tolist()]

    dominant = detect_dominant_format(series, sample_size=sample_size)
    non_conforming = collect_non_conforming_samples(
        series,
        dominant_label=dominant["label"],
        sample_size=sample_size,
        max_samples=100,
    )

    missing_stats = get_column_missing_stats(df[[column_name]])[column_name]

    deterministic_profile = {
        "column_name": column_name,
        "dtype": str(series.dtype),
        "row_count": int(len(series)),
        "null_count": missing_stats["null_count"],
        "non_null_count": missing_stats["non_null_count"],
        "missing_percentage": missing_stats["missing_percentage"],
        "n_unique_non_null": int(non_missing.nunique(dropna=True)),
        "unique_ratio_non_null": round(
            float(non_missing.nunique(dropna=True) / max(len(non_missing), 1)), 4
        ),
        "sample_values": sample_values,
        "dominant_format": dominant,
        "non_conforming": non_conforming,
    }

    numeric = _try_numeric(non_missing)
    if len(non_missing) > 0 and numeric.notna().mean() >= 0.9:
        numeric = numeric.dropna()
        if not numeric.empty:
            deterministic_profile["numeric_summary"] = {
                "min": _to_native(numeric.min()),
                "max": _to_native(numeric.max()),
                "mean": _to_native(round(float(numeric.mean()), 4)),
                "median": _to_native(round(float(numeric.median()), 4)),
                "std": _to_native(round(float(numeric.std(ddof=1)), 4)) if len(numeric) > 1 else None,
            }

    enrichment = enrich_column_profile_with_llm(
        deterministic_profile=deterministic_profile,
        llm_callable=llm_callable,
    )

    full_profile = {**deterministic_profile, **enrichment}
    return _to_native(full_profile)


def profile_all_columns(
    df: pd.DataFrame,
    llm_callable: Optional[Callable[[str], str]] = None,
    sample_size: int = DOMINANT_FORMAT_SAMPLE_SIZE,
) -> dict:
    return {
        col: profile_single_column(df, col, llm_callable=llm_callable, sample_size=sample_size)
        for col in df.columns
    }


def build_cleaning_plan(rich_profile_per_column: dict) -> dict:

    plan = {}
    for col_name, profile in rich_profile_per_column.items():
        dominant = profile.get("dominant_format", {}) or {}
        plan[col_name] = {
            "column_name": col_name,
            "expected_dtype": profile.get("expected_dtype", "string"),
            "dominant_format": dominant.get("label"),
            "transformation_rule": profile.get("transformation_rule", {
                "action": "none",
                "target_format": dominant.get("label"),
                "params": {},
                "description": "",
            }),
        }
    return plan


def build_dataset_column_profiles(
    df: pd.DataFrame,
    dataset_name: str,
    rich_json_path: str,
    slim_json_path: str,
    llm_callable: Optional[Callable[[str], str]] = None,
    sample_size: int = DOMINANT_FORMAT_SAMPLE_SIZE,
    findings_root_key: str = "column_profiles",
) -> dict:

    findings = _safe_load_json(rich_json_path)

    dataset_summary = {
        "dataset_name": dataset_name,
        "shape": get_dataframe_shape(df),
        "dtypes": get_dataframe_dtypes(df),
    }

    columns_payload = profile_all_columns(
        df,
        llm_callable=llm_callable,
        sample_size=sample_size,
    )

    findings.setdefault(findings_root_key, {})
    findings[findings_root_key][dataset_name] = {
        "dataset_summary": dataset_summary,
        "columns": columns_payload,
    }
    _safe_write_json(rich_json_path, findings)

    slim_all = _safe_load_json(slim_json_path)
    slim_all[dataset_name] = build_cleaning_plan(columns_payload)
    _safe_write_json(slim_json_path, slim_all)

    return findings[findings_root_key][dataset_name]

def build_slim_profiles_for_data_agent(
    column_profiles_path: str = COLUMN_PROFILES_JSON,
) -> dict:

    with open(column_profiles_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    profiles_root = raw.get("column_profiles", raw)

    slim = {}
    for dataset_name, dataset_block in profiles_root.items():
        if not isinstance(dataset_block, dict):
            continue

        columns_block = dataset_block.get("columns", {})
        if not columns_block:
            continue

        slim_cols = {}
        for col_name, col_profile in columns_block.items():
            slim_cols[col_name] = {
                "role": col_profile.get("role", "unknown"),
                "description": col_profile.get("description", ""),
                "sample_values": col_profile.get("sample_values", [])[:5],
            }
        slim[dataset_name] = slim_cols

    return slim

def format_column_profiles_for_prompt(
    profiles_json_path: str = COLUMN_PROFILES_JSON,
    dataset_names: Optional[list[str]] = None,
    max_sample_values: int = 5,
) -> str:
    
    if not os.path.exists(profiles_json_path):
        return f"[column_profiles.json not found at {profiles_json_path}]"

    try:
        with open(profiles_json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        return f"[failed to read column_profiles.json: {e}]"

    profiles_root = raw.get("column_profiles", raw)
    if not isinstance(profiles_root, dict) or not profiles_root:
        return "[column_profiles.json is empty or malformed]"

    if dataset_names is not None:
        selected = {k: v for k, v in profiles_root.items() if k in dataset_names}
    else:
        selected = profiles_root

    if not selected:
        return "[no matching datasets in column_profiles.json]"

    lines = []
    for ds_name, ds_block in selected.items():
        if not isinstance(ds_block, dict):
            continue
        columns = ds_block.get("columns", {})
        if not columns:
            continue

        lines.append(f"=== DATASET: {ds_name} ===")
        for col_name, col_profile in columns.items():
            role = col_profile.get("role", "unknown")
            desc = col_profile.get("description", "") or "(no description)"
            samples = col_profile.get("sample_values", [])[:max_sample_values]
            samples_str = ", ".join(str(s) for s in samples) if samples else "(no samples)"
            lines.append(
                f"- {col_name} | role={role} | desc={desc} | samples=[{samples_str}]"
            )
        lines.append("")  # blank line between datasets

    return "\n".join(lines).strip()


# ---- extracted from notebook cell 302 ----
def _is_missing(v) -> bool:
    return v is None or (isinstance(v, float) and pd.isna(v)) or v is pd.NA


def _smart_recover(value, dominant_label: Optional[str]):

    if _is_missing(value):
        return value

    s = str(value).strip()
    if s == "":
        return pd.NA

    if dominant_label == "digit":
        if "-" in s:
            return pd.NA
        m = re.search(r"\d+", s)
        return m.group(0) if m else pd.NA

    if dominant_label == "float":
        m = re.search(r"-?\d+[.,]?\d*", s)
        if not m:
            return pd.NA
        return m.group(0).replace(",", ".")

    if dominant_label == "alpha":
        m = re.search(r"[A-Za-z]+", s)
        return m.group(0) if m else pd.NA

    if dominant_label == "alphanumeric":
        m = re.search(r"[A-Za-z0-9]+", s)
        return m.group(0) if m else pd.NA

    return pd.NA


def _mask_for_map(series: pd.Series, params: dict) -> pd.Series:
    mapping = params.get("mapping", {}) or {}
    if not mapping:
        return pd.Series(False, index=series.index)
    keys = {str(k).strip().lower() for k in mapping.keys()}

    def _hit(v):
        if _is_missing(v):
            return False
        return str(v).strip().lower() in keys

    return series.map(_hit).astype(bool)


def _mask_for_extract(series: pd.Series, params: dict) -> pd.Series:
    pattern = params.get("regex", r"\d+")
    full = re.compile(f"^(?:{pattern})$")

    def _needs_extract(v):
        if _is_missing(v):
            return False
        return full.match(str(v).strip()) is None

    return series.map(_needs_extract).astype(bool)


def _mask_for_set_null(series: pd.Series, dominant_label: Optional[str]) -> pd.Series:
    if dominant_label is None:
        return series.notna()  

    def _non_conforming(v):
        if _is_missing(v):
            return False
        return _value_format_label(v) != dominant_label

    return series.map(_non_conforming).astype(bool)


def _action_none(series: pd.Series, params: dict) -> pd.Series:
    return series


def _action_extract(series: pd.Series, params: dict) -> pd.Series:
    pattern = params.get("regex", r"\d+")

    def _extract_one(v):
        if _is_missing(v):
            return v

        m = re.search(pattern, str(v).strip())
        if not m:
            return pd.NA

        if m.groups():
            return next((g for g in m.groups() if g is not None), pd.NA)

        return m.group(0)

    return series.map(_extract_one)


def _action_map(series: pd.Series, params: dict) -> pd.Series:
    mapping = params.get("mapping", {}) or {}
    if not mapping:
        return series
    norm = {str(k).strip().lower(): (pd.NA if v is None else str(v))
            for k, v in mapping.items()}

    def _map_one(v):
        if _is_missing(v):
            return v
        return norm.get(str(v).strip().lower(), v)

    return series.map(_map_one)


def _action_set_null(series: pd.Series, params: dict, dominant_label: Optional[str]) -> pd.Series:
    return series.map(lambda v: _smart_recover(v, dominant_label))


ACTION_DISPATCHER = {
    "none":     _action_none,
    "extract":  _action_extract,
    "map":      _action_map,
    "set_null": _action_set_null,
}


def apply_transformation_rule(
    series: pd.Series,
    transformation_rule: dict,
    dominant_label: Optional[str],
) -> pd.Series:
    action = (transformation_rule or {}).get("action", "none")
    params = (transformation_rule or {}).get("params", {}) or {}

    if action == "none" or action not in ACTION_DISPATCHER:
        return series

    if action == "map":
        target_mask = _mask_for_map(series, params)
    elif action == "extract":
        target_mask = _mask_for_extract(series, params)
    elif action == "set_null":
        target_mask = _mask_for_set_null(series, dominant_label)
    else:
        target_mask = pd.Series(False, index=series.index)

    if not target_mask.any():
        return series

    out = series.astype("object").copy()
    sub = out.loc[target_mask]

    if action == "set_null":
        out.loc[target_mask] = _action_set_null(sub, params, dominant_label)
    else:
        out.loc[target_mask] = ACTION_DISPATCHER[action](sub, params)

    return out


def enforce_expected_dtype(series: pd.Series, expected_dtype: str) -> pd.Series:
    if expected_dtype is None or str(series.dtype) == expected_dtype:
        return series

    try:
        if expected_dtype.startswith("datetime"):
            return pd.to_datetime(series, errors="coerce")
        if expected_dtype in {"Int64", "Int32"}:
            return pd.to_numeric(series, errors="coerce").astype(expected_dtype)
        if expected_dtype in {"Float64", "Float32", "float64", "float32"}:
            return pd.to_numeric(series, errors="coerce").astype(expected_dtype)
        return series.astype(expected_dtype)
    except Exception:
        return series


def clean_dataset(
    input_csv_path: str,
    output_csv_path: str,
    cleaning_plan_path: str,
    dataset_key: str,
    read_csv_kwargs: Optional[dict] = None,
) -> dict:
    read_csv_kwargs = read_csv_kwargs or {}

    df = pd.read_csv(input_csv_path, **read_csv_kwargs)
    shape_before = df.shape

    df = normalize_column_names(df)
    df = deduplicate_column_names(df)
    df = standardize_missing_values(df)
    df = normalize_text_values(df)

    plan = load_cleaning_plan(cleaning_plan_path, dataset_key)

    per_column_actions = {}
    dtype_changes = {}

    for col in df.columns:
        col_plan = plan.get(col)
        if not col_plan:
            per_column_actions[col] = {"action": "skipped (no plan)"}
            continue

        rule = col_plan.get("transformation_rule", {}) or {}
        dominant_label = col_plan.get("dominant_format")
        expected_dtype = col_plan.get("expected_dtype")

        original = df[col]
        df[col] = apply_transformation_rule(
            series=df[col],
            transformation_rule=rule,
            dominant_label=dominant_label,
        )

        dtype_before = str(df[col].dtype)
        df[col] = enforce_expected_dtype(df[col], expected_dtype)
        dtype_after = str(df[col].dtype)

        n_changed = int((original.astype("string") != df[col].astype("string")).sum())
        per_column_actions[col] = {
            "action": rule.get("action", "none"),
            "rows_changed": n_changed,
            "dtype_before": dtype_before,
            "dtype_after": dtype_after,
            "expected_dtype": expected_dtype,
            "dtype_match": (dtype_after == expected_dtype) if expected_dtype else None,
        }
        if dtype_before != dtype_after:
            dtype_changes[col] = {"before": dtype_before, "after": dtype_after}

    df = remove_duplicate_rows(df)

    print(f"DTYPE DIAGNOSTIC for {dataset_key}  (pre-to_csv)")
    print(f"{'column':<30} {'expected':<20} {'actual':<20} OK?")
    for col, info in per_column_actions.items():
        if info.get('action') == 'skipped (no plan)':
            continue
        exp = info.get('expected_dtype') or '(none)'
        act = info.get('dtype_after') or '?'
        ok = 'OK' if (info.get('expected_dtype') is None or info.get('dtype_match')) else 'NO'
        print(f"{col:<30} {exp:<20} {act:<20} {ok}")

    shape_after = df.shape
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)

    return {
        "dataset_key": dataset_key,
        "input_path": input_csv_path,
        "output_path": output_csv_path,
        "shape_before": list(shape_before),
        "shape_after": list(shape_after),
        "duplicate_rows_removed": int(shape_before[0] - shape_after[0]),
        "per_column_actions": per_column_actions,
        "dtype_changes": dtype_changes,
    }


# ---- extracted from notebook cell 304 ----
def llm_callable(prompt: str) -> str:
    response = _client.chat.completions.create(
        model=MISTRAL_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data profiling assistant. "
                    "When asked, you return ONLY a valid JSON object — "
                    "no preamble, no markdown fences, no explanations outside the JSON. "
                    "Do not invent facts not supported by the provided profile."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content.strip()

def run_pre_pipeline_column_profiling(
    datasets: list[tuple[str, str]],
) -> dict:
    profiles = {}

    for dataset_name, csv_path in datasets:
        if not os.path.exists(csv_path):
            print(f"  [profiling] File not found, skipped: {csv_path}")
            continue

        try:
            original_cols = list(pd.read_csv(csv_path, nrows=0).columns)
            print(f"  [profiling] Running column profiling for {dataset_name} "
                  f"({len(original_cols)} columns: {', '.join(original_cols[:5])}"
                  f"{'...' if len(original_cols) > 5 else ''})")
        except Exception:
            print(f"  [profiling] Running column profiling for {dataset_name}...")

        df = pd.read_csv(csv_path)
        df = normalize_column_names(df)
        df = deduplicate_column_names(df)
        df = standardize_missing_values(df)
        df = normalize_text_values(df)

        profiles[dataset_name] = build_dataset_column_profiles(
            df=df,
            dataset_name=dataset_name,
            rich_json_path=COLUMN_PROFILES_JSON,
            slim_json_path=CLEANING_PLAN_JSON,
            llm_callable=llm_callable,
            sample_size=DOMINANT_FORMAT_SAMPLE_SIZE,
        )
        print(f"  [profiling] Saved profile for {dataset_name}")

    return profiles


# ---- extracted from notebook cell 310 ----
def _findings_guidance(task_key: str, extra_notes: str = "") -> str:
    base = (
        f"Maintain a shared findings JSON at '{FINDINGS_JSON}'. "
        f"At the start, attempt to load it; if missing, empty, invalid, or corrupted, "
        f"initialize an empty dict instead of failing. "
        f"Store new information under the key '{task_key}' while preserving existing keys "
        f"for other tasks. "
        f"Use concise, machine-readable fields with only native Python JSON-serializable types "
        f"such as dict, list, str, int, float, bool, or null. "
        f"Convert pandas and numpy values to native Python types before saving. "
        f"Convert tuples to lists before saving. "
        f"After completing the task, update the entry for '{task_key}' and write the full JSON "
        f"back by overwriting the file. "
    )
    if extra_notes:
        base += extra_notes
    return base


# ---- extracted from notebook cell 313 ----
def build_group_key(
    df: pd.DataFrame,
    key_columns: list[str],
    separator: str = "|",
) -> pd.Series:

    if not key_columns:
        raise ValueError("key_columns must not be empty")

    missing = [c for c in key_columns if c not in df.columns]
    if missing:
        raise KeyError(f"group_key columns not in dataframe: {missing}")

    parts = []
    for col in key_columns:
        s = df[col]
        # Normalize integral floats: 1.0 -> "1", but 1.5 -> "1.5"
        if pd.api.types.is_float_dtype(s):
            integral_mask = s.notna() & (s == s.astype("Int64", errors="ignore").astype(float, errors="ignore"))
            # Simpler and safer: convert via Int64 if all non-null are integral
            try:
                if s.dropna().apply(float.is_integer).all():
                    s = s.astype("Int64")  # nullable integer
            except Exception:
                pass

        s = s.astype(str).fillna("").str.strip()
        # Replace the literal strings 'nan' / 'NaT' / '<NA>' coming from astype(str) on NaN
        s = s.replace({"nan": "", "NaT": "", "<NA>": "", "None": ""})
        parts.append(s)

    key = parts[0]
    for p in parts[1:]:
        key = key.str.cat(p, sep=separator)
    return key


def drop_empty_keys(
    df: pd.DataFrame,
    group_key: pd.Series,
    separator: str = "|",
) -> tuple[pd.DataFrame, pd.Series]:

    key_str = group_key.astype(str)
    has_empty = (
        key_str.eq("")
        | key_str.str.startswith(separator)
        | key_str.str.endswith(separator)
        | key_str.str.contains(rf"\{separator}\{separator}", regex=True)
    )
    keep = ~has_empty
    return df.loc[keep].copy(), group_key.loc[keep].copy()


def apply_scope_filters(
    df: pd.DataFrame,
    filters: dict[str, list],
) -> pd.Series:

    if not filters:
        return pd.Series(True, index=df.index)

    mask = pd.Series(True, index=df.index)
    for col, accepted_values in filters.items():
        if col not in df.columns:
            raise KeyError(f"filter column '{col}' not in dataframe")
        if not isinstance(accepted_values, list):
            raise TypeError(f"filter '{col}' must be a list, got {type(accepted_values).__name__}")

        col_series = df[col]
        if pd.api.types.is_numeric_dtype(col_series):
            # Cast filter values to numeric; ignore unparseable ones
            numeric_accepted = []
            for v in accepted_values:
                try:
                    numeric_accepted.append(float(v))
                except (TypeError, ValueError):
                    pass
            mask &= col_series.isin(numeric_accepted)
        else:
            normalized_col = col_series.astype(str).str.strip().str.lower()
            normalized_accepted = [str(v).strip().lower() for v in accepted_values]
            mask &= normalized_col.isin(normalized_accepted)

    return mask


def aggregate_baseline(
    df: pd.DataFrame,
    group_key: pd.Series,
    volume_column: Optional[str],
    dataset_name: str,
) -> pd.DataFrame:

    work = df.copy()
    work["__group_key__"] = group_key.values

    if volume_column is not None and volume_column in work.columns:
        v = pd.to_numeric(work[volume_column], errors="coerce")
    else:
        v = pd.Series(1.0, index=work.index)
    work["__volume__"] = v

    grouped = work.groupby("__group_key__", dropna=False)["__volume__"]
    agg = pd.DataFrame({
        "group_volume":  grouped.sum(min_count=1),
        "n_records":     grouped.size(),
        "baseline_mean": grouped.mean(),
        "baseline_std":  grouped.std(ddof=1),
    }).reset_index().rename(columns={"__group_key__": "group_key"})

    agg["rate"] = np.where(
        agg["n_records"] > 0,
        agg["group_volume"] / agg["n_records"],
        np.nan,
    )
    agg["dataset"] = dataset_name

    # Replace +/-inf with NaN
    for c in ["group_volume", "n_records", "rate", "baseline_mean", "baseline_std"]:
        agg[c] = pd.to_numeric(agg[c], errors="coerce")
        agg[c] = agg[c].replace([np.inf, -np.inf], np.nan)

    # Final column order, fixed by contract
    return agg[[
        "dataset", "group_key", "group_volume",
        "n_records", "rate", "baseline_mean", "baseline_std",
    ]]


# ---- extracted from notebook cell 316 ----
def compute_zscore_per_dataset(
    df: pd.DataFrame,
    value_column: str,
    dataset_column: str = "dataset",
) -> pd.Series:

    if value_column not in df.columns:
        raise KeyError(f"value_column '{value_column}' not in dataframe")
    if dataset_column not in df.columns:
        raise KeyError(f"dataset_column '{dataset_column}' not in dataframe")

    z = pd.Series(0.0, index=df.index)
    for ds_name, sub in df.groupby(dataset_column, dropna=False):
        v = pd.to_numeric(sub[value_column], errors="coerce")
        mean = v.mean()
        std  = v.std(ddof=0)
        if not np.isfinite(std) or std == 0:
            z.loc[sub.index] = 0.0
        else:
            z.loc[sub.index] = (v - mean) / std

    z = z.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return z


def compute_ratio_to_baseline(
    group_volume: pd.Series,
    baseline_mean: pd.Series,
) -> pd.Series:

    bm = pd.to_numeric(baseline_mean, errors="coerce")
    gv = pd.to_numeric(group_volume,  errors="coerce")

    # Avoid division warnings: replace 0 / non-finite baseline with NaN
    safe_bm = bm.where((bm != 0) & np.isfinite(bm), np.nan)
    ratio = gv / safe_bm
    return ratio.replace([np.inf, -np.inf], np.nan)


def flag_outliers_hybrid(
    df: pd.DataFrame,
    score_column: str,
    confidence_column: str,
    top_k_fraction: float = 0.05,
    min_confidence_abs: float = 1.5,
    per_dataset: bool = True,
    dataset_column: str = "dataset",
) -> pd.Series:

    if score_column not in df.columns:
        raise KeyError(f"score_column '{score_column}' not in dataframe")
    if confidence_column not in df.columns:
        raise KeyError(f"confidence_column '{confidence_column}' not in dataframe")

    is_outlier = pd.Series(False, index=df.index)

    confidence_ok = df[confidence_column].abs() >= min_confidence_abs

    if per_dataset:
        if dataset_column not in df.columns:
            raise KeyError(f"dataset_column '{dataset_column}' not in dataframe")
        groups = df.groupby(dataset_column, dropna=False)
    else:
        groups = [(None, df)]

    for _, sub in groups:
        n = len(sub)
        if n == 0:
            continue
        k = max(1, int(np.ceil(top_k_fraction * n)))
        top_idx = sub[score_column].sort_values(ascending=False).head(k).index
        is_outlier.loc[top_idx] = True

    return is_outlier & confidence_ok


def filter_by_scope_keys(
    df: pd.DataFrame,
    scope_keys: dict[str, list[str]],
    dataset_column: str = "dataset",
    key_column: str = "group_key",
) -> pd.DataFrame:

    if dataset_column not in df.columns:
        raise KeyError(f"dataset_column '{dataset_column}' not in dataframe")
    if key_column not in df.columns:
        raise KeyError(f"key_column '{key_column}' not in dataframe")

    parts = []
    for ds_name, keys in scope_keys.items():
        if not keys:
            continue
        keyset = set(str(k) for k in keys)
        sub = df[(df[dataset_column] == ds_name) & (df[key_column].astype(str).isin(keyset))]
        parts.append(sub)

    if not parts:
        return df.iloc[0:0].copy()
    return pd.concat(parts, ignore_index=False)


# ---- extracted from notebook cell 320 ----
CODE_EXECUTOR_SYSTEM_PROMPT = (
    "You are a code-generation agent. "
    "When given a task, you respond ONLY with executable Python code — "
    "no preamble, no explanations, no markdown fences. "
    "Use only standard libraries plus pandas, numpy, json, os, re, math. "
    "Do not import subprocess, requests, or any networking module. "
    "All inputs and outputs are file paths on the local filesystem. "
    "Always print short progress messages so the orchestrator can see what happened. "
    "Always end with a clear print line confirming success or raising an explicit error."
)


def _extract_code_from_response(raw: str) -> str:
    s = raw.strip()

    m = re.search(r"```(?:python)?\s*(.*?)```", s, re.DOTALL)
    if m:
        return m.group(1).strip()

    m = re.search(r"```(?:python)?\s*\n(.*)", s, re.DOTALL)
    if m:
        return m.group(1).strip()

    return s


AGENT_GLOBALS = {
    "__name__": "__agent__",

    "os":   os,
    "json": json,
    "np":   np,
    "pd":   pd,

    "build_group_key":      build_group_key,
    "drop_empty_keys":      drop_empty_keys,
    "apply_scope_filters":  apply_scope_filters,
    "aggregate_baseline":   aggregate_baseline,

    "compute_zscore_per_dataset":  compute_zscore_per_dataset,
    "compute_ratio_to_baseline":   compute_ratio_to_baseline,
    "flag_outliers_hybrid":        flag_outliers_hybrid,
    "filter_by_scope_keys":        filter_by_scope_keys,

    "OUTPUT_DIR":           OUTPUT_DIR,
    "SCOPE_MANIFEST_JSON":  SCOPE_MANIFEST_JSON,
    "COLUMN_PROFILES_JSON": COLUMN_PROFILES_JSON,
}


def code_executor_run(
    prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 4096,
) -> dict:

    response = _client.chat.completions.create(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": CODE_EXECUTOR_SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    raw = response.choices[0].message.content
    code = _extract_code_from_response(raw)

    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    success = True

    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = captured_stdout, captured_stderr

    try:

        exec(code, AGENT_GLOBALS.copy())
    except Exception:
        success = False
        captured_stderr.write(traceback.format_exc())
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

    return {
        "code":    code,
        "stdout":  captured_stdout.getvalue(),
        "stderr":  captured_stderr.getvalue(),
        "success": success,
    }


# ---- extracted from notebook cell 322 ----
# baseline validator
def validate_baseline_output(output_path: str) -> dict:
    """
    Validate the baseline CSV produced by the Baseline Agent, plus the
    sibling scope_keys.json.

    Checks (short-circuit on file-level failures):
      1. baseline CSV file exists and is loadable
      2. exact schema: dataset, group_key, group_volume, n_records, rate,
                       baseline_mean, baseline_std
      3. non-empty
      4. numeric columns are numeric and contain no +/-inf
      5. group_key column has no missing/empty values
      6. dataset column matches the dataset names declared in the manifest
      7. scope_keys.json exists, parses, and has one entry per manifest dataset
      8. every group_key listed in scope_keys actually exists in the baseline
         for that dataset
    """
    checks = []

    # 1. file exists + loadable
    file_exists = os.path.exists(output_path)
    checks.append({
        "name": "file_exists",
        "ok": file_exists,
        "detail": output_path,
    })
    if not file_exists:
        return {"passed": False, "checks": checks}

    try:
        df = pd.read_csv(output_path)
    except Exception as e:
        checks.append({"name": "loadable", "ok": False, "detail": str(e)})
        return {"passed": False, "checks": checks}
    checks.append({"name": "loadable", "ok": True, "detail": f"shape={df.shape}"})

    # 2. exact schema
    required_columns = [
        "dataset", "group_key", "group_volume",
        "n_records", "rate", "baseline_mean", "baseline_std",
    ]
    actual_columns = list(df.columns)
    schema_ok = actual_columns == required_columns
    checks.append({
        "name": "exact_schema",
        "ok": schema_ok,
        "detail": (
            "schema matches" if schema_ok
            else f"expected={required_columns}, got={actual_columns}"
        ),
    })
    if not schema_ok:
        return {"passed": False, "checks": checks}

    # 3. non-empty
    checks.append({
        "name": "non_empty",
        "ok": len(df) > 0,
        "detail": f"rows={len(df)}",
    })
    if len(df) == 0:
        return {"passed": False, "checks": checks}

    # 4. numeric dtypes + no inf
    numeric_cols = ["group_volume", "n_records", "rate", "baseline_mean", "baseline_std"]
    non_numeric = [
        c for c in numeric_cols
        if not pd.api.types.is_numeric_dtype(df[c])
    ]
    checks.append({
        "name": "numeric_dtypes",
        "ok": not non_numeric,
        "detail": f"non_numeric={non_numeric}" if non_numeric else "all numeric",
    })

    has_inf = False
    for c in numeric_cols:
        if pd.api.types.is_numeric_dtype(df[c]) and np.isinf(df[c]).any():
            has_inf = True
            break
    checks.append({
        "name": "no_infinity",
        "ok": not has_inf,
        "detail": "no inf" if not has_inf else "found +/-inf in numeric columns",
    })

    # 5. group_key populated
    gk_missing = df["group_key"].isna().sum() + (df["group_key"].astype(str).str.strip() == "").sum()
    checks.append({
        "name": "group_key_populated",
        "ok": gk_missing == 0,
        "detail": f"missing_or_empty={gk_missing}",
    })

    # 6 + 7 + 8. cross-check against manifest and scope_keys.json
    manifest_path = SCOPE_MANIFEST_JSON
    if not os.path.exists(manifest_path):
        checks.append({
            "name": "manifest_available",
            "ok": False,
            "detail": f"manifest not found at {manifest_path}",
        })
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        checks.append({"name": "manifest_loadable", "ok": False, "detail": str(e)})
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    manifest_dataset_names = [d.get("name") for d in manifest.get("datasets", [])]
    baseline_dataset_names = set(df["dataset"].dropna().unique().tolist())

    # 6. dataset column values
    unknown_datasets = baseline_dataset_names - set(manifest_dataset_names)
    checks.append({
        "name": "dataset_column_matches_manifest",
        "ok": not unknown_datasets,
        "detail": (
            f"baseline has unknown datasets: {sorted(unknown_datasets)}"
            if unknown_datasets
            else f"datasets present={sorted(baseline_dataset_names)}"
        ),
    })

    # 7. scope_keys.json
    scope_keys_path = os.path.join(OUTPUT_DIR, "scope_keys.json")
    scope_exists = os.path.exists(scope_keys_path)
    checks.append({
        "name": "scope_keys_file_exists",
        "ok": scope_exists,
        "detail": scope_keys_path,
    })
    if not scope_exists:
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    try:
        with open(scope_keys_path, "r", encoding="utf-8") as f:
            scope_keys = json.load(f)
    except Exception as e:
        checks.append({"name": "scope_keys_loadable", "ok": False, "detail": str(e)})
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    if not isinstance(scope_keys, dict):
        checks.append({
            "name": "scope_keys_structure",
            "ok": False,
            "detail": f"expected dict, got {type(scope_keys).__name__}",
        })
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    missing_in_scope_keys = [n for n in manifest_dataset_names if n not in scope_keys]
    checks.append({
        "name": "scope_keys_covers_manifest",
        "ok": not missing_in_scope_keys,
        "detail": (
            f"missing entries for: {missing_in_scope_keys}"
            if missing_in_scope_keys
            else f"all {len(manifest_dataset_names)} manifest datasets present"
        ),
    })

    # 8. every group_key in scope_keys exists in the baseline for that dataset
    orphan_keys = []
    for ds_name, keys in scope_keys.items():
        if not isinstance(keys, list):
            orphan_keys.append(f"{ds_name}: not a list")
            continue
        baseline_keys_for_ds = set(
            df.loc[df["dataset"] == ds_name, "group_key"].astype(str).tolist()
        )
        for k in keys:
            if str(k) not in baseline_keys_for_ds:
                orphan_keys.append(f"{ds_name}:{k}")
    checks.append({
        "name": "scope_keys_in_baseline",
        "ok": not orphan_keys,
        "detail": (
            f"{len(orphan_keys)} orphan keys (first 5: {orphan_keys[:5]})"
            if orphan_keys
            else "all scope keys exist in baseline"
        ),
    })

    return {
        "passed": all(c["ok"] for c in checks),
        "checks": checks,
    }

# Outlier Detection Validator

def validate_outlier_output(output_path: str) -> dict:
    """
    Validate the outliers CSV produced by the Outlier Agent.

    Checks (short-circuit on file-level failures):
      1. file exists and is loadable
      2. exact schema (column names + order)
      3. dataset and group_key columns are non-null on every row
      4. numeric columns are numeric and contain no +/-inf
      5. is_outlier column is boolean-coercible AND True for every row
         (because the file should contain only flagged rows after scope filter)
      6. dataset values are a subset of those declared in the manifest
      7. every (dataset, group_key) row in the file is also present in
         baseline_data.csv with the same dataset/group_key
      8. zero rows is ALLOWED (honest "no outlier" outcome) — but the file must
         still exist and have the correct schema
    """
    checks = []

    # 1. file + loadable
    file_exists = os.path.exists(output_path)
    checks.append({
        "name": "file_exists",
        "ok": file_exists,
        "detail": output_path,
    })
    if not file_exists:
        return {"passed": False, "checks": checks}

    try:
        df = pd.read_csv(output_path)
    except Exception as e:
        checks.append({"name": "loadable", "ok": False, "detail": str(e)})
        return {"passed": False, "checks": checks}
    checks.append({"name": "loadable", "ok": True, "detail": f"shape={df.shape}"})

    # 2. exact schema
    required_columns = [
        "dataset", "group_key", "group_volume", "n_records", "rate",
        "baseline_mean", "baseline_std",
        "z_score", "ratio_to_baseline", "anomaly_score", "is_outlier",
    ]
    actual_columns = list(df.columns)
    schema_ok = actual_columns == required_columns
    checks.append({
        "name": "exact_schema",
        "ok": schema_ok,
        "detail": (
            "schema matches" if schema_ok
            else f"expected={required_columns}, got={actual_columns}"
        ),
    })
    if not schema_ok:
        return {"passed": False, "checks": checks}

    # 8 (early). Empty file with correct schema is valid.
    if len(df) == 0:
        checks.append({
            "name": "empty_outlier_file_is_valid",
            "ok": True,
            "detail": "no in-scope outliers found (valid honest result)",
        })
        return {"passed": True, "checks": checks}

    # 3. dataset + group_key populated
    ds_missing = df["dataset"].isna().sum() + (df["dataset"].astype(str).str.strip() == "").sum()
    gk_missing = df["group_key"].isna().sum() + (df["group_key"].astype(str).str.strip() == "").sum()
    checks.append({
        "name": "identity_columns_populated",
        "ok": (ds_missing == 0 and gk_missing == 0),
        "detail": f"missing_dataset={ds_missing}, missing_group_key={gk_missing}",
    })

    # 4. numeric dtypes + no inf
    numeric_cols = [
        "group_volume", "n_records", "rate", "baseline_mean", "baseline_std",
        "z_score", "ratio_to_baseline", "anomaly_score",
    ]
    non_numeric = [
        c for c in numeric_cols
        if not pd.api.types.is_numeric_dtype(df[c])
    ]
    checks.append({
        "name": "numeric_dtypes",
        "ok": not non_numeric,
        "detail": f"non_numeric={non_numeric}" if non_numeric else "all numeric",
    })

    has_inf = False
    for c in numeric_cols:
        if pd.api.types.is_numeric_dtype(df[c]) and np.isinf(df[c]).any():
            has_inf = True
            break
    checks.append({
        "name": "no_infinity",
        "ok": not has_inf,
        "detail": "no inf" if not has_inf else "found +/-inf in numeric columns",
    })

    # 5. is_outlier should be True everywhere (file contains only flagged rows)
    try:
        is_out = df["is_outlier"].astype(bool)
        all_true = is_out.all()
    except Exception as e:
        checks.append({
            "name": "is_outlier_boolean",
            "ok": False,
            "detail": f"is_outlier not boolean-coercible: {e}",
        })
        return {"passed": False, "checks": checks}
    checks.append({
        "name": "is_outlier_all_true",
        "ok": bool(all_true),
        "detail": (
            "all rows flagged as outlier" if all_true
            else f"{(~is_out).sum()} rows have is_outlier=False (should be filtered out)"
        ),
    })

    # 6. dataset values consistent with manifest
    try:
        with open(SCOPE_MANIFEST_JSON, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        manifest_datasets = {d.get("name") for d in manifest.get("datasets", [])}
    except Exception as e:
        checks.append({
            "name": "manifest_loadable",
            "ok": False,
            "detail": str(e),
        })
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    unknown = set(df["dataset"].dropna().unique()) - manifest_datasets
    checks.append({
        "name": "dataset_values_in_manifest",
        "ok": not unknown,
        "detail": (
            f"unknown datasets in outliers: {sorted(unknown)}"
            if unknown else "all dataset values from manifest"
        ),
    })

    # 7. cross-check (dataset, group_key) against baseline_data.csv
    baseline_path = os.path.join(OUTPUT_DIR, "baseline_data.csv")
    if not os.path.exists(baseline_path):
        checks.append({
            "name": "baseline_available",
            "ok": False,
            "detail": f"baseline_data.csv not found at {baseline_path}",
        })
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    try:
        baseline_df = pd.read_csv(baseline_path)
        baseline_pairs = set(
            zip(baseline_df["dataset"].astype(str), baseline_df["group_key"].astype(str))
        )
    except Exception as e:
        checks.append({
            "name": "baseline_loadable",
            "ok": False,
            "detail": str(e),
        })
        return {"passed": all(c["ok"] for c in checks), "checks": checks}

    outlier_pairs = list(zip(df["dataset"].astype(str), df["group_key"].astype(str)))
    orphan_pairs = [p for p in outlier_pairs if p not in baseline_pairs]
    checks.append({
        "name": "outliers_exist_in_baseline",
        "ok": not orphan_pairs,
        "detail": (
            f"{len(orphan_pairs)} orphan rows (first 5: {orphan_pairs[:5]})"
            if orphan_pairs else "all outliers traceable to baseline"
        ),
    })

    return {
        "passed": all(c["ok"] for c in checks),
        "checks": checks,
    }

# Risk Profiling Validator

def validate_risk_output(output_path: str) -> dict:
    """
    Validate the risk report CSV produced by the Risk Profiling Agent.

    Checks:
      1. file exists and is loadable
      2. exact schema (11 outlier columns + 3 risk columns, in order)
      3. empty file with correct schema is valid (short-circuit OK)
      4. risk_level values are exactly {HIGH, MEDIUM, LOW}
      5. risk_score is numeric and in [0, 100]
      6. risk_reason is non-empty string for every row
      7. the original 11 outlier columns are unchanged (spot-check: dataset
         and group_key values exist in outliers.csv)
    """
    checks = []

    # 1. file + loadable
    file_exists = os.path.exists(output_path)
    checks.append({
        "name": "file_exists",
        "ok": file_exists,
        "detail": output_path,
    })
    if not file_exists:
        return {"passed": False, "checks": checks}

    try:
        df = pd.read_csv(output_path)
    except Exception as e:
        checks.append({"name": "loadable", "ok": False, "detail": str(e)})
        return {"passed": False, "checks": checks}
    checks.append({"name": "loadable", "ok": True, "detail": f"shape={df.shape}"})

    # 2. exact schema
    required_columns = [
        "dataset", "group_key", "group_volume", "n_records", "rate",
        "baseline_mean", "baseline_std",
        "z_score", "ratio_to_baseline", "anomaly_score", "is_outlier",
        "risk_score", "risk_level", "risk_reason",
    ]
    actual_columns = list(df.columns)
    schema_ok = actual_columns == required_columns
    checks.append({
        "name": "exact_schema",
        "ok": schema_ok,
        "detail": (
            "schema matches" if schema_ok
            else f"expected={required_columns}, got={actual_columns}"
        ),
    })
    if not schema_ok:
        return {"passed": False, "checks": checks}

    # 3. empty file is valid
    if len(df) == 0:
        checks.append({
            "name": "empty_risk_report_valid",
            "ok": True,
            "detail": "no outliers to profile (valid)",
        })
        return {"passed": True, "checks": checks}

    # 4. risk_level values
    valid_levels = {"HIGH", "MEDIUM", "LOW"}
    actual_levels = set(df["risk_level"].dropna().unique())
    levels_ok = actual_levels.issubset(valid_levels)
    checks.append({
        "name": "valid_risk_levels",
        "ok": levels_ok,
        "detail": (
            f"valid: {sorted(actual_levels)}" if levels_ok
            else f"invalid levels found: {sorted(actual_levels - valid_levels)}"
        ),
    })

    # 5. risk_score numeric and in [0, 100]
    if pd.api.types.is_numeric_dtype(df["risk_score"]):
        rs = df["risk_score"].dropna()
        in_range = (rs >= 0).all() and (rs <= 100).all()
        checks.append({
            "name": "risk_score_range",
            "ok": bool(in_range),
            "detail": (
                f"range=[{rs.min():.1f}, {rs.max():.1f}]" if in_range
                else f"out of range: min={rs.min():.1f}, max={rs.max():.1f}"
            ),
        })
    else:
        checks.append({
            "name": "risk_score_range",
            "ok": False,
            "detail": "risk_score is not numeric",
        })

    # 6. risk_reason non-empty
    reason_missing = (
        df["risk_reason"].isna().sum()
        + (df["risk_reason"].astype(str).str.strip() == "").sum()
    )
    checks.append({
        "name": "risk_reason_populated",
        "ok": reason_missing == 0,
        "detail": (
            "all rows have reasons" if reason_missing == 0
            else f"{reason_missing} rows missing risk_reason"
        ),
    })

    # 7. cross-check with outliers.csv
    outlier_path = os.path.join(OUTPUT_DIR, "outliers.csv")
    if os.path.exists(outlier_path):
        try:
            outlier_df = pd.read_csv(outlier_path)
            outlier_count = len(outlier_df)
            risk_count = len(df)
            count_match = outlier_count == risk_count
            checks.append({
                "name": "row_count_matches_outliers",
                "ok": count_match,
                "detail": (
                    f"both have {outlier_count} rows" if count_match
                    else f"outliers={outlier_count}, risk_report={risk_count}"
                ),
            })
        except Exception:
            pass  # not critical

    return {
        "passed": all(c["ok"] for c in checks),
        "checks": checks,
    }


# Report Validator

def validate_report_output(output_path: str) -> dict:
    """
    Validate the markdown report produced by the Report Agent.

    Checks:
      1. file exists
      2. file is non-trivially long (> 200 chars)
      3. required sections are present
      4. no raw group_key patterns (pipe-separated codes) leak into the report
    """
    checks = []

    # 1. file exists
    file_exists = os.path.exists(output_path)
    checks.append({
        "name": "file_exists",
        "ok": file_exists,
        "detail": output_path,
    })
    if not file_exists:
        return {"passed": False, "checks": checks}

    with open(output_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2. non-trivial length
    is_long = len(text.strip()) > 200
    checks.append({
        "name": "non_empty",
        "ok": is_long,
        "detail": f"chars={len(text)}",
    })

    # 3. required sections
    required_sections = [
        "Executive Summary",
        "Risk Distribution",
        "Detailed Findings",
        "Methodology",
        "Recommended Actions",
    ]
    missing = [s for s in required_sections if s not in text]
    checks.append({
        "name": "required_sections",
        "ok": len(missing) == 0,
        "detail": f"missing={missing}" if missing else "all present",
    })

    # 4. no raw group_keys leaked (pattern: word|word|word)
    import re
    raw_key_pattern = re.compile(r'\b[a-z]{2,5}\|[a-z]{2,5}\|\d{1,2}\b')
    raw_leaks = raw_key_pattern.findall(text)
    checks.append({
        "name": "no_raw_group_keys",
        "ok": len(raw_leaks) == 0,
        "detail": (
            "all group keys expanded" if not raw_leaks
            else f"raw keys found in report: {raw_leaks[:5]}"
        ),
    })

    return {
        "passed": all(c["ok"] for c in checks),
        "checks": checks,
    }


def print_validation_report(verdict: dict, label: str = ""):
    print(f"\n  ┌─ Validation report {label} ─")
    for c in verdict["checks"]:
        icon = "✓" if c["ok"] else "✗"
        print(f"  │ {icon}  {c['name']:<22} {c['detail']}")
    print(f"  └─ Overall: {'PASSED' if verdict['passed'] else 'FAILED'}\n")


# ---- extracted from notebook cell 324 ----
def run_agent_with_supervisor(
    task_name: str,
    prompt: str,
    validator_fn,             
    output_path: str,
    max_retries: int = 3,
    retry_temperatures: tuple = (0.0, 0.3, 0.6, 0.9),
) -> dict:

    print(f"  AGENT: {task_name}")

    last_exec = None
    last_verdict = None

    for attempt_idx in range(max_retries + 1):
        temp = retry_temperatures[min(attempt_idx, len(retry_temperatures) - 1)]
        print(f"\n  [attempt {attempt_idx + 1}/{max_retries + 1}] temperature={temp}")

        last_exec = code_executor_run(prompt, temperature=temp)

        if last_exec["stdout"]:
            print("  ── stdout ──")
            for line in last_exec["stdout"].rstrip().splitlines():
                print(f"  │ {line}")

        if not last_exec["success"]:
            print("  Execution Failed")
            tail = last_exec["stderr"].rstrip().splitlines()[-8:]
            for line in tail:
                print(f"  ! {line}")
            continue

        last_verdict = validator_fn(output_path)
        print_validation_report(last_verdict, label=f"attempt {attempt_idx + 1}")

        if last_verdict["passed"]:
            print(f"   {task_name} SUCCEEDED on attempt {attempt_idx + 1}")
            return {
                "task":       task_name,
                "succeeded":  True,
                "attempts":   attempt_idx + 1,
                "last_code":  last_exec["code"],
                "last_stdout": last_exec["stdout"],
                "last_stderr": last_exec["stderr"],
                "last_validation": last_verdict,
            }

    print(f"\n   {task_name} FAILED after {max_retries + 1} attempts")
    return {
        "task":       task_name,
        "succeeded":  False,
        "attempts":   max_retries + 1,
        "last_code":  last_exec["code"] if last_exec else "",
        "last_stdout": last_exec["stdout"] if last_exec else "",
        "last_stderr": last_exec["stderr"] if last_exec else "",
        "last_validation": last_verdict,
    }


# ---- extracted from notebook cell 327 ----
def _build_data_agent_prompt():
    # Datasets cleaned disponibili sul disco, mappati al loro nome nel column_profiles
    dataset_paths = {
        "allarmi_raw":   f"{OUTPUT_DIR}/allarmi_clean.csv",
        "tipologia_raw": f"{OUTPUT_DIR}/tipologia_clean.csv",
    }

    column_profiles_block = format_column_profiles_for_prompt(
        profiles_json_path=COLUMN_PROFILES_JSON,
        dataset_names=list(dataset_paths.keys()),
    )

    paths_block = "\n".join(
        f"- {ds_name} -> {ds_path}" for ds_name, ds_path in dataset_paths.items()
    )

    return (
        "You are the Data Agent of an anomaly detection pipeline for transit/event data. "
        "You do NOT filter or save any tabular data. Your single deliverable is a JSON file "
        "called the 'scope manifest', which describes how the rest of the pipeline should "
        "interpret the user's query. "

        f"User query: '{USER_QUERY}'. "
        f"Output file (JSON): '{SCOPE_MANIFEST_JSON}'. "

        "Generate Python code that reads no CSV, performs no filtering, and writes only the "
        "manifest JSON. The code MUST start with: "
        "import os, json "

        # ── DATASETS DESCRIPTION ──────────────────────────────────────────
        "AVAILABLE CLEANED DATASETS (paths on disk): "
        f"{paths_block} "

        "COLUMN PROFILES (role / description / sample values for every column of every dataset): "
        f"{column_profiles_block} "

        # ── WHAT YOU MUST DECIDE ──────────────────────────────────────────
        "Reason about the user query and decide: "
        "(1) which dataset(s) are relevant — this is multi-dataset capable, so include every "
        "dataset whose columns can contribute to answering the query. Use the column "
        "descriptions and sample_values to judge relevance, NOT the dataset name. "
        "(2) for each relevant dataset, the filters that translate the query into concrete "
        "column-level constraints. Express filters as a dict {column_name: [accepted_values]}. "
        "Use the actual value format stored in the dataset (e.g. IATA codes, ISO country codes, "
        "lowercase strings) — infer the right format from sample_values. "
        "(3) for each relevant dataset, a 'group_key_hint': the list of columns that the "
        "Baseline Agent should aggregate by, given the analytical granularity implied by the "
        "query. "

        "RULES FOR group_key_hint: "
        "  - Choose columns that produce groups with multiple records each. The baseline must "
        "    compute mean and standard deviation per group, so groups of size 1 are useless. "
        "  - NEVER include high-cardinality columns where almost every value is unique, such as "
        "    raw timestamps, exact datetimes, full ISO date-times, transaction IDs, or record IDs. "
        "    These produce one-row groups and break the baseline. "
        "  - TEMPORAL DIMENSION RULE (strict): "
        "    Do NOT include any time-related column (month, year, quarter, week, day, "
        "    day-of-week, date, etc.) in group_key_hint UNLESS the user query EXPLICITLY "
        "    asks for a time-based analysis. Explicit temporal signals are words like: "
        "    'monthly', 'per month', 'by month', 'over time', 'trend', 'seasonal', "
        "    'by year', 'yearly', 'weekly', 'evolution'. If none of these (or equivalents) "
        "    appears in the query, you MUST omit time columns from group_key_hint, even if "
        "    a coarse time column exists in the dataset. "
        "  - DEFAULT GRANULARITY (when query is generic about granularity): "
        "    If the user query mentions a location/origin/destination (a country, airport, "
        "    or city) without any other granularity hint, default to route-level grouping: "
        "    [departure_airport_column, arrival_airport_column]. This produces meaningful "
        "    groups (multiple flights per route) and leverages both endpoints of the journey. "
        "  - Allowed shapes, ordered by preference: "
        "    1. [departure_airport, arrival_airport]  -> route-level (DEFAULT for location queries) "
        "    2. [departure_airport]                   -> origin-airport-level "
        "    3. [country]                             -> country-level (only if many countries in scope) "
        "    4. [airport, month] / [route, month]     -> ONLY when query is explicitly temporal "

        "(4) for each relevant dataset, a 'volume_column_hint': the single numeric column "
        "representing THE METRIC WE WANT TO MONITOR FOR ANOMALIES — the quantity that, when "
        "unusually high or low for a group, signals an anomaly. "
        "RULES FOR volume_column_hint: "
        "  - This is the NUMERATOR of the anomaly story, not the denominator. If the dataset "
        "    contains both a count of events of interest (e.g. number of alarms, number of "
        "    flagged travelers) and a total population (e.g. total flights, total travelers), "
        "    pick the count of events of interest, NOT the total population. "
        "  - Use column descriptions and roles to identify the metric: prefer columns described "
        "    as 'alarms', 'alerts', 'flagged', 'incidents', 'anomalies', 'events of interest' "
        "    over columns described as 'total', 'volume', 'population', 'all flights', 'all "
        "    travelers'. "
        "  - If multiple candidates exist, pick the one most semantically aligned with the user "
        "    query. "
        "  - If the dataset truly has no metric column (only categorical info and totals), set "
        "    this to null and the baseline will fall back to record counts. "
        "(5) a short 'user_intent_summary' (one sentence) and, for each dataset, a short "
        "'rationale' explaining why it is included AND why you picked that group_key_hint and "
        "volume_column_hint. "

        "Produce a JSON object with EXACTLY this structure: "
        "{ "
        "  'user_query': <the original user query as a string>, "
        "  'user_intent_summary': <one-sentence summary>, "
        "  'datasets': [ "
        "    { "
        "      'name': <dataset name as it appears in the column profiles, e.g. allarmi_raw>, "
        "      'path': <full path to the cleaned CSV from the AVAILABLE CLEANED DATASETS block>, "
        "      'filters': { <column_name>: [<value>, ...], ... }, "
        "      'group_key_hint': [<column_name>, ...], "
        "      'volume_column_hint': <column_name or null>, "
        "      'rationale': <short string> "
        "    }, "
        "    ... "
        "  ] "
        "} "
        "Use double quotes in the JSON output. Do NOT include any other top-level keys. "

        "Hard constraints: "
        "- Every column referenced in 'filters', 'group_key_hint', or 'volume_column_hint' "
        "  MUST exist in the column profiles of the corresponding dataset. "
        "- The 'datasets' array must contain at least one dataset. If no dataset is relevant, "
        "  raise a ValueError with a clear message instead of writing the file. "
        "- All filter values must be lists, even single-value filters. "
        "- All filter values must use the lowercase / coded form found in sample_values. "
        "- Do NOT load, read, or save any CSV. Do NOT filter any data."
    )


# ---- extracted from notebook cell 328 ----
def validate_data_agent_output(output_path: str) -> dict:

    checks = []

    # 1. file exists
    file_exists = os.path.exists(output_path)
    checks.append({
        "name": "file_exists",
        "ok": file_exists,
        "detail": output_path,
    })
    if not file_exists:
        return {"passed": False, "checks": checks}

    # 2. parseable JSON
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        checks.append({"name": "parseable_json", "ok": False, "detail": str(e)})
        return {"passed": False, "checks": checks}
    checks.append({"name": "parseable_json", "ok": True, "detail": "ok"})

    # 3. top-level keys
    required_top = ["user_query", "user_intent_summary", "datasets"]
    missing_top = [k for k in required_top if k not in manifest]
    checks.append({
        "name": "top_level_keys",
        "ok": not missing_top,
        "detail": f"missing={missing_top}" if missing_top else "all present",
    })
    if missing_top:
        return {"passed": False, "checks": checks}

    # 4. datasets is non-empty list
    datasets = manifest.get("datasets")
    is_list = isinstance(datasets, list)
    is_non_empty = is_list and len(datasets) > 0
    checks.append({
        "name": "datasets_non_empty_list",
        "ok": is_non_empty,
        "detail": f"type={type(datasets).__name__}, len={len(datasets) if is_list else 'n/a'}",
    })
    if not is_non_empty:
        return {"passed": False, "checks": checks}

    # 5. per-dataset structural checks
    required_ds_fields = {
        "name": str,
        "path": str,
        "filters": dict,
        "group_key_hint": list,
        "rationale": str,
    }
    structural_errors = []
    for i, ds in enumerate(datasets):
        if not isinstance(ds, dict):
            structural_errors.append(f"datasets[{i}] is not a dict")
            continue
        for field, expected_type in required_ds_fields.items():
            if field not in ds:
                structural_errors.append(f"datasets[{i}] missing '{field}'")
            elif not isinstance(ds[field], expected_type):
                structural_errors.append(
                    f"datasets[{i}].{field} has type {type(ds[field]).__name__}, "
                    f"expected {expected_type.__name__}"
                )
        # volume_column_hint may be str or None
        if "volume_column_hint" not in ds:
            structural_errors.append(f"datasets[{i}] missing 'volume_column_hint'")
        elif ds["volume_column_hint"] is not None and not isinstance(ds["volume_column_hint"], str):
            structural_errors.append(
                f"datasets[{i}].volume_column_hint must be str or null"
            )
    checks.append({
        "name": "datasets_structure",
        "ok": not structural_errors,
        "detail": "; ".join(structural_errors) if structural_errors else "all valid",
    })
    if structural_errors:
        return {"passed": False, "checks": checks}

    # 6 + 7. cross-check column references against column_profiles.json
    try:
        with open(COLUMN_PROFILES_JSON, "r", encoding="utf-8") as f:
            raw_profiles = json.load(f)
        profiles_root = raw_profiles.get("column_profiles", raw_profiles)
    except Exception as e:
        checks.append({
            "name": "column_profiles_loadable",
            "ok": False,
            "detail": str(e),
        })
        return {"passed": False, "checks": checks}

    column_errors = []
    for i, ds in enumerate(datasets):
        ds_name = ds["name"]
        ds_block = profiles_root.get(ds_name)
        if not isinstance(ds_block, dict) or "columns" not in ds_block:
            column_errors.append(f"datasets[{i}].name='{ds_name}' not found in column_profiles")
            continue
        known_cols = set(ds_block["columns"].keys())

        # filters
        for col, values in ds["filters"].items():
            if col not in known_cols:
                column_errors.append(
                    f"datasets[{i}] filter column '{col}' not in profiles for '{ds_name}'"
                )
            if not isinstance(values, list):
                column_errors.append(
                    f"datasets[{i}].filters['{col}'] must be a list, got {type(values).__name__}"
                )

        # group_key_hint
        for col in ds["group_key_hint"]:
            if col not in known_cols:
                column_errors.append(
                    f"datasets[{i}] group_key_hint column '{col}' not in profiles for '{ds_name}'"
                )

        # volume_column_hint (if not null)
        vol = ds.get("volume_column_hint")
        if vol is not None and vol not in known_cols:
            column_errors.append(
                f"datasets[{i}] volume_column_hint '{vol}' not in profiles for '{ds_name}'"
            )

    checks.append({
        "name": "column_references_valid",
        "ok": not column_errors,
        "detail": "; ".join(column_errors) if column_errors else "all references valid",
    })

    return {
        "passed": all(c["ok"] for c in checks),
        "checks": checks,
    }


# ---- extracted from notebook cell 332 ----
def _build_baseline_prompt():
    return (
        "You are the Baseline Agent of an anomaly detection pipeline. "
        "Your job is to build a population-level statistical baseline by aggregating each "
        "cleaned dataset listed in the scope manifest, then mark which groups fall inside the "
        "user's scope. You do NOT detect anomalies — that is the next agent's job. "

        f"Input manifest (JSON): '{SCOPE_MANIFEST_JSON}'. "
        f"Output baseline CSV: '{OUTPUT_DIR}/baseline_data.csv'. "
        f"Output scope keys JSON: '{OUTPUT_DIR}/scope_keys.json'. "

        "Generate Python code. The code MUST start with these imports and NOTHING ELSE: "
        "  import os, json "
        "  import pandas as pd "
        "  import numpy as np "

        # ── HELPERS: PRE-LOADED, DO NOT IMPORT ────────────────────────────
        "CRITICAL — HELPER FUNCTIONS ARE PRE-LOADED IN THE GLOBAL NAMESPACE. "
        "Do NOT write any of these statements: "
        "  - 'import build_group_key' "
        "  - 'from helpers import ...' "
        "  - 'from build_group_key import ...' "
        "  - any other import that references the helper names below. "
        "These functions are already callable as plain names. They are NOT modules. "
        "They are NOT in any package. Just call them directly, like you call len() or print(). "

        "Available helpers and their signatures: "
        "  build_group_key(df, key_columns, separator='|') -> pd.Series "
        "      Robust string concatenation of the columns into a group_key Series. "
        "      Already handles float-as-int normalization and NaN. Do not pre-cast columns. "

        "  drop_empty_keys(df, group_key, separator='|') -> (pd.DataFrame, pd.Series) "
        "      Returns a tuple. Always unpack into TWO variables. The function never returns "
        "      None. Use the returned df and key for everything downstream. "

        "  apply_scope_filters(df, filters) -> pd.Series[bool] "
        "      Boolean mask, AND across columns, OR within a column, case-insensitive on "
        "      strings. Pass the cleaned df (after drop_empty_keys), not the raw one. "

        "  aggregate_baseline(df, group_key, volume_column, dataset_name) -> pd.DataFrame "
        "      Returns a dataframe with the canonical baseline schema, ALREADY in the right "
        "      column order: dataset, group_key, group_volume, n_records, rate, baseline_mean, "
        "      baseline_std. Do NOT post-process the columns of this dataframe. "

        "INPUT CONTRACT — the manifest JSON has this structure: "
        "{ "
        "  'user_query': str, 'user_intent_summary': str, "
        "  'datasets': [ "
        "    { 'name': str, 'path': str, 'filters': {col: [values]}, "
        "      'group_key_hint': [col, ...], 'volume_column_hint': col or null, "
        "      'rationale': str } "
        "  ] "
        "} "
        "Each path points to a cleaned CSV with the FULL population. The baseline must be "
        "computed on the full population so that the downstream Outlier Agent has "
        "statistically meaningful means and standard deviations. "

        "REFERENCE SKELETON — adapt this canonical structure. The skeleton is correct as "
        "written; only modify variable values, not the call shape. "

        "  with open(MANIFEST_PATH, 'r', encoding='utf-8') as f: "
        "      manifest = json.load(f) "
        ""
        "  baseline_frames = [] "
        "  scope_keys = {} "
        ""
        "  for ds in manifest['datasets']: "
        "      ds_name   = ds['name'] "
        "      ds_path   = ds['path'] "
        "      gk_cols   = ds['group_key_hint'] "
        "      vol_col   = ds['volume_column_hint'] "
        "      filters   = ds['filters'] "
        ""
        "      df = pd.read_csv(ds_path) "
        "      print(f'{ds_name}: shape={df.shape}') "
        ""
        "      raw_key = build_group_key(df, gk_cols) "
        "      df_clean, key_clean = drop_empty_keys(df, raw_key) "
        ""
        "      if len(df_clean) == 0: "
        "          scope_keys[ds_name] = [] "
        "          print(f'{ds_name}: empty after drop_empty_keys, skipping') "
        "          continue "
        ""
        "      agg = aggregate_baseline(df_clean, key_clean, vol_col, ds_name) "
        "      baseline_frames.append(agg) "
        ""
        "      mask = apply_scope_filters(df_clean, filters) "
        "      in_scope_keys = key_clean[mask].unique().tolist() "
        "      scope_keys[ds_name] = in_scope_keys "
        ""
        "  baseline_df = pd.concat(baseline_frames, ignore_index=True) "
        "  baseline_df.to_csv(BASELINE_CSV, index=False) "
        ""
        "  with open(SCOPE_KEYS_JSON, 'w', encoding='utf-8') as f: "
        "      json.dump(scope_keys, f, indent=2, ensure_ascii=False) "

        "Replace MANIFEST_PATH, BASELINE_CSV, SCOPE_KEYS_JSON with the literal paths from "
        "this prompt. "

        "Hard constraints: "
        "- Do NOT import the helpers. Call them as bare names. "
        "- Do NOT reimplement group_key concatenation, scope filtering, or baseline aggregation. "
        "- Do NOT post-process the schema returned by aggregate_baseline. "
        "- Always unpack drop_empty_keys into TWO variables: 'df_clean, key_clean = drop_empty_keys(...)'. "
        "- Use df_clean and key_clean (not the raw df or raw_key) for aggregation and scope filtering. "
        "- The code must run top-to-bottom without user input. "

        "At the end, print: number of datasets processed, total baseline rows, in-scope group "
        "counts per dataset (one line per dataset), and baseline_df.head(10). "
    )


# ---- extracted from notebook cell 336 ----
def _build_outlier_prompt():
    return (
        "You are the Outlier Detection Agent of an anomaly detection pipeline. "
        "Your job is to score every group in the population baseline, flag anomalies using a "
        "robust hybrid rule, and finally narrow the output to the groups inside the user's "
        "scope. The scoring is GLOBAL (full population), the output is LOCAL (scope only). "
        "You do NOT classify risk levels — that is the next agent's job. "

        f"Input baseline CSV: '{OUTPUT_DIR}/baseline_data.csv'. "
        f"Input scope keys JSON: '{OUTPUT_DIR}/scope_keys.json'. "
        f"Output outliers CSV: '{OUTPUT_DIR}/outliers.csv'. "

        "Generate Python code. The code MUST start with these imports and NOTHING ELSE: "
        "  import os, json "
        "  import pandas as pd "
        "  import numpy as np "

        "CRITICAL — HELPER FUNCTIONS ARE PRE-LOADED IN THE GLOBAL NAMESPACE. "
        "Do NOT write any of these statements: "
        "  - 'import compute_zscore_per_dataset' "
        "  - 'from helpers import ...' "
        "  - any other import that references the helper names below. "
        "These functions are already callable as plain names. They are NOT modules. "
        "They are NOT in any package. Just call them directly, like you call len() or print(). "

        "Available helpers and their signatures: "
        "  compute_zscore_per_dataset(df, value_column, dataset_column='dataset') -> pd.Series "
        "      Returns z-score of value_column computed PER DATASET separately. Already "
        "      handles std=0, NaN, inf. Output is aligned with df.index. "

        "  compute_ratio_to_baseline(group_volume, baseline_mean) -> pd.Series "
        "      Element-wise ratio. Returns NaN where baseline_mean is 0 or non-finite. "
        "      Pass two pd.Series, not column names. "

        "  flag_outliers_hybrid(df, score_column, confidence_column, "
        "                       top_k_fraction=0.05, min_confidence_abs=1.5, "
        "                       per_dataset=True, dataset_column='dataset') -> pd.Series[bool] "
        "      Returns boolean mask: True iff row is in top-K (per dataset) AND "
        "      |confidence_column| >= min_confidence_abs. Never raises if no row qualifies; "
        "      simply returns all False. "

        "  filter_by_scope_keys(df, scope_keys, dataset_column='dataset', "
        "                        key_column='group_key') -> pd.DataFrame "
        "      Keeps only rows whose (dataset, group_key) is listed in scope_keys. "
        "      Datasets not present in the dict, or with empty lists, are excluded entirely. "

        "INPUT CONTRACT — baseline_data.csv has exactly these columns, in this order: "
        "  dataset, group_key, group_volume, n_records, rate, baseline_mean, baseline_std "
        "Multiple datasets may coexist in the same file (the 'dataset' column distinguishes "
        "them). Numeric columns may contain NaN; do not assume completeness. "

        "scope_keys.json has structure { dataset_name: [group_key, ...], ... }. "
        "It defines which groups are in the user's scope. Datasets with empty lists are valid "
        "and mean 'no group in scope from this dataset'. "

        "SCORING DESIGN — compute the following per-row signals on the FULL baseline (do not "
        "filter by scope before scoring): "
        "  - z_score:           compute_zscore_per_dataset on group_volume "
        "  - ratio_to_baseline: compute_ratio_to_baseline on group_volume and baseline_mean "
        "  - anomaly_score:     a single non-negative aggregate combining the magnitude of "
        "    z_score and the magnitude of (ratio_to_baseline - 1). Compute it as: "
        "        anomaly_score = z_score.abs() + (ratio_to_baseline - 1).abs().fillna(0) "
        "    This treats both 'much more than expected' and 'much less than expected' as "
        "    anomalous, and is invariant to the absolute scale of group_volume because both "
        "    components are normalized. "

        "FLAGGING — use flag_outliers_hybrid with score_column='anomaly_score', "
        "confidence_column='z_score', top_k_fraction=0.05, min_confidence_abs=1.5, "
        "per_dataset=True. This selects per-dataset top 5% AND requires |z|>=1.5. "
        "If no row qualifies, the result is an empty mask — that is valid and expected on "
        "well-behaved datasets. Do NOT artificially force at least one outlier. "

        "SCOPE FILTERING — after flagging, narrow the output with filter_by_scope_keys. "
        "Apply the scope filter ONLY at the end, never before scoring. "

        "REFERENCE SKELETON — adapt this canonical structure. The skeleton is correct as "
        "written; only modify literal values, not the call shape. "

        "  baseline_df = pd.read_csv(BASELINE_CSV) "
        ""
        "  with open(SCOPE_KEYS_JSON, 'r', encoding='utf-8') as f: "
        "      scope_keys = json.load(f) "
        ""
        "  # Scoring on the FULL population "
        "  baseline_df['z_score'] = compute_zscore_per_dataset(baseline_df, 'group_volume') "
        "  baseline_df['ratio_to_baseline'] = compute_ratio_to_baseline( "
        "      baseline_df['group_volume'], baseline_df['baseline_mean'] "
        "  ) "
        "  baseline_df['anomaly_score'] = ( "
        "      baseline_df['z_score'].abs() "
        "      + (baseline_df['ratio_to_baseline'] - 1).abs().fillna(0) "
        "  ) "
        ""
        "  # Hybrid flagging on the FULL population "
        "  baseline_df['is_outlier'] = flag_outliers_hybrid( "
        "      baseline_df, "
        "      score_column='anomaly_score', "
        "      confidence_column='z_score', "
        "      top_k_fraction=0.05, "
        "      min_confidence_abs=1.5, "
        "      per_dataset=True, "
        "  ) "
        ""
        "  # Scope filter ONLY at the end "
        "  flagged = baseline_df[baseline_df['is_outlier']].copy() "
        "  in_scope_outliers = filter_by_scope_keys(flagged, scope_keys) "
        ""
        "  # Sort by anomaly_score descending so the most anomalous rows come first "
        "  in_scope_outliers = in_scope_outliers.sort_values( "
        "      'anomaly_score', ascending=False "
        "  ).reset_index(drop=True) "
        ""
        "  in_scope_outliers.to_csv(OUTLIERS_CSV, index=False) "

        "Replace BASELINE_CSV, SCOPE_KEYS_JSON, OUTLIERS_CSV with the literal paths from this "
        "prompt. "

        "OUTPUT SCHEMA — outliers.csv must have EXACTLY these columns, in this order: "
        "  dataset, group_key, group_volume, n_records, rate, baseline_mean, baseline_std, "
        "  z_score, ratio_to_baseline, anomaly_score, is_outlier "
        "All numeric columns must be numeric. Replace +/-inf with NaN. The file may be empty "
        "(zero rows) if no in-scope group qualifies as outlier; that is a valid result. "

        "Hard constraints: "
        "- Do NOT import the helpers. Call them as bare names. "
        "- Do NOT reimplement z-score, ratio-to-baseline, hybrid flagging, or scope filtering. "
        "- Do NOT filter by scope before scoring. The scoring needs the full population. "
        "- Do NOT force at least one outlier. An empty result is valid and honest. "
        "- Do NOT change the column order in the output. "
        "- The code must run top-to-bottom without user input. "

        "At the end, print: total baseline rows, number of rows flagged on full population, "
        "number of rows in scope (regardless of flag), final number of in-scope outliers, "
        "and in_scope_outliers.head(10). "
    )


# ---- extracted from notebook cell 340 ----
def _build_risk_prompt():
    return (
        "You are the Risk Profiling Agent of an anomaly detection pipeline. "
        "Your job is to translate raw anomaly scores into actionable risk levels with "
        "human-readable explanations. You work ONLY on the outlier rows produced by the "
        "previous agent — you do NOT re-detect anomalies. "

        f"Input outliers CSV: '{OUTPUT_DIR}/outliers.csv'. "
        f"Output risk report CSV: '{OUTPUT_DIR}/risk_report.csv'. "

        "Generate Python code. The code MUST start with these imports and NOTHING ELSE: "
        "  import os "
        "  import pandas as pd "
        "  import numpy as np "

        # ── INPUT CONTRACT ────────────────────────────────────────────────
        "INPUT CONTRACT — outliers.csv has exactly these columns, in this order: "
        "  dataset, group_key, group_volume, n_records, rate, baseline_mean, baseline_std, "
        "  z_score, ratio_to_baseline, anomaly_score, is_outlier "
        "The file may have ZERO rows (no in-scope outliers). This is a valid input. "
        "If the file is empty (0 rows), write a risk_report.csv with correct columns but "
        "zero rows, print a message saying no outliers to profile, and exit normally. "

        # ── WHAT YOU MUST DO ──────────────────────────────────────────────
        "If the file has rows, do the following: "

        "1. RISK SCORE — normalize anomaly_score to a 0-100 scale: "
        "     min_s = df['anomaly_score'].min() "
        "     max_s = df['anomaly_score'].max() "
        "     df['risk_score'] = 100 * (df['anomaly_score'] - min_s) / (max_s - min_s + 1e-9) "
        "   If only one row exists, set risk_score to 100 for that row. "

        "2. RISK LEVEL — assign a categorical risk level based on risk_score: "
        "     risk_score >= 70   → 'HIGH' "
        "     risk_score >= 30   → 'MEDIUM' "
        "     otherwise          → 'LOW' "
        "   Do NOT use ratio_to_baseline or z_score directly for the level assignment — they "
        "   can be inflated on sparse data. The normalized risk_score is the only driver of "
        "   the level. "

        "3. RISK REASON — generate a short, human-readable explanation for each row by "
        "   examining the available signals. Use the actual column values to build the "
        "   sentence. Example patterns (adapt based on the row data): "
        "   - HIGH + large z_score: 'This group shows a z-score of {z:.1f}, indicating "
        "     volume {x} times above the population average for dataset {dataset}.' "
        "   - HIGH + large ratio: 'This group has {ratio:.1f}x the expected baseline "
        "     volume, with {n_records} records observed.' "
        "   - MEDIUM: 'Moderate deviation detected: z-score={z:.1f}, ratio={r:.1f}x baseline.' "
        "   - LOW: 'Minor deviation from baseline; monitor for trend changes.' "
        "   These are examples, not templates. Write reasons that are informative and specific "
        "   to each row's actual numbers. Do NOT hardcode domain-specific words like 'alarm', "
        "   'flight', 'route' — use the generic terms 'group', 'volume', 'baseline'. "
        "   CRITICAL: NEVER include the raw group_key value (e.g. 'tia|bgy|1', 'ist|fco|2') "
        "   inside risk_reason. The group_key is shown separately in its own column. "
        "   The risk_reason must be self-contained narrative text that does NOT reference "
        "   the group by its coded key — use 'this group' or 'the group' instead. "

        "4. Sort by risk_score descending. "

        # ── OUTPUT SCHEMA (STRICT) ────────────────────────────────────────
        "OUTPUT SCHEMA — risk_report.csv must have EXACTLY these columns, in this order: "
        "  dataset, group_key, group_volume, n_records, rate, baseline_mean, baseline_std, "
        "  z_score, ratio_to_baseline, anomaly_score, is_outlier, "
        "  risk_score, risk_level, risk_reason "
        "That is: ALL 11 columns from outliers.csv (unchanged) + 3 new columns appended. "
        "Do NOT drop, rename, or reorder the original 11 columns. "

        # ── HARD CONSTRAINTS ──────────────────────────────────────────────
        "Hard constraints: "
        "- Do NOT re-detect or re-flag outliers. Every input row remains in the output. "
        "- Do NOT drop rows (even if risk_level is LOW). "
        "- Do NOT use domain-specific terms (alarm, flight, route, transit) in risk_reason; "
        "  keep it generic so it works across any dataset. "
        "- risk_level must be one of exactly three values: 'HIGH', 'MEDIUM', 'LOW'. "
        "- Empty input → empty output (with correct schema). This is valid. "
        "- The code must run top-to-bottom without user input. "

        # ── REPORTING ─────────────────────────────────────────────────────
        "At the end, print: total rows, count per risk_level (HIGH, MEDIUM, LOW), "
        "and df.head(10). "
    )


# ---- extracted from notebook cell 344 ----
def _build_report_prompt():
    # Leggiamo il manifest per dare contesto al report agent su come
    # interpretare i group_key (quali colonne li compongono)
    try:
        with open(SCOPE_MANIFEST_JSON, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        manifest_block = json.dumps(manifest, indent=2, ensure_ascii=False)
    except Exception:
        manifest_block = "[scope_manifest.json not available]"

    # Column profiles per arricchimento semantico
    column_profiles_block = format_column_profiles_for_prompt(
        profiles_json_path=COLUMN_PROFILES_JSON,
    )

    return (
        "You are a senior intelligence analyst writing an Anomaly Report for a transit/event "
        "monitoring system. Your task is to produce a detailed, descriptive, narrative report "
        "from risk_report.csv, enriched with human-readable interpretations of every data point. "

        f"Input risk report: '{OUTPUT_DIR}/risk_report.csv'. "
        f"Output report: '{OUTPUT_DIR}/anomaly_report.md'. "

        "Generate Python code. The code MUST start with these imports and NOTHING ELSE: "
        "  import os, json "
        "  import pandas as pd "
        "  import numpy as np "

        # ── INPUT CONTRACT ────────────────────────────────────────────────
        "INPUT CONTRACT — risk_report.csv has exactly these columns: "
        "  dataset, group_key, group_volume, n_records, rate, baseline_mean, baseline_std, "
        "  z_score, ratio_to_baseline, anomaly_score, is_outlier, "
        "  risk_score, risk_level, risk_reason "
        "The file may have zero rows. In that case, produce a short report stating that no "
        "anomalies were detected in the user's scope, and exit normally. "

        # ── SCOPE MANIFEST (for context) ──────────────────────────────────
        "SCOPE MANIFEST — this describes the user's original query, the datasets involved, "
        "the filters applied, and critically the GROUP KEY STRUCTURE. Use it to understand "
        "what each component of the group_key represents: "
        f"{manifest_block} "

        "GROUP KEY INTERPRETATION — the group_key column contains values like 'ist|fco|1'. "
        "Each segment separated by '|' maps to a column from the group_key_hint in the manifest. "
        "For example, if group_key_hint is ['areoporto_partenza', 'areoporto_arrivo', 'mese_partenza'], "
        "then 'ist|fco|1' means: departure airport = IST, arrival airport = FCO, month = 1. "
        "When writing the report, you MUST decode each group_key into a rich, human-readable "
        "description. Use your world knowledge to expand coded values: "
        "  - IATA airport codes → full airport name + city (e.g. IST → Istanbul Airport, "
        "    FCO → Roma Fiumicino Leonardo da Vinci) "
        "  - Month numbers → month name (e.g. 1 → January, 2 → February) "
        "  - Country codes → full country name (e.g. TR → Turkey, IT → Italy) "
        "  - Any other coded value → expand if known, keep as-is if not "
        "Format expanded groups as: 'Istanbul Airport (IST) → Roma Fiumicino (FCO), January'. "
        "This makes the report immediately understandable without reference to raw data. "

        "COLUMN PROFILES (for additional context on what columns mean): "
        f"{column_profiles_block} "

        # ── REPORT STRUCTURE ──────────────────────────────────────────────
        "The report MUST include exactly these sections, in this order: "

        "# Anomaly Report "
        "## Executive Summary "
        "A concise overview: what did the user ask for (from the manifest's user_intent_summary), "
        "how many groups were analyzed, how many were flagged as anomalous, and the overall "
        "risk distribution. Mention the datasets involved by name and the scope filters applied. "
        "Set the tone: this is an analytical assessment, not an alarm. "

        "## Risk Distribution "
        "Report the exact HIGH, MEDIUM, LOW counts from risk_level. Do not invent counts. "
        "Present as narrative prose, not a raw table. Example: 'Of the N flagged groups, "
        "X present high risk, Y moderate risk, and Z lower-priority deviations.' "

        "## Detailed Findings "
        "For each row in the risk report (start with HIGH, then MEDIUM, then LOW): "
        "  - Use the EXPANDED group_key as the subsection title (not the raw coded key). "
        "  - Report all quantitative signals: group_volume, baseline_mean, z_score, "
        "    ratio_to_baseline, anomaly_score, risk_score. "
        "  - Include the risk_reason from the Risk Agent. "
        "  - Add your own analytical commentary: what does this deviation plausibly mean? "
        "    Is it a volume spike, a rate anomaly, a seasonal effect? Use the available numbers "
        "    to reason. Be specific but avoid speculation beyond what the data shows. "
        "  - Compare against the baseline: 'This group recorded X events against a population "
        "    average of Y, representing a Z-fold deviation.' "
        "If there are more than 15 rows, focus in detail on the top 10 by risk_score and "
        "summarize the rest in a compact table. "

        "## Methodology "
        "Briefly explain how anomalies were detected: population-level baseline by group, "
        "z-score per dataset, hybrid flagging (top-K + confidence floor), scope filtering. "
        "This section helps the reader understand the confidence level of the findings. "
        "Keep it to 3-5 sentences. "

        "## Recommended Actions "
        "Write operational recommendations proportional to the actual risk distribution: "
        "  - If HIGH risks exist → recommend immediate review with specific group references. "
        "  - If only MEDIUM → recommend enhanced monitoring and trend analysis. "
        "  - If only LOW → recommend routine monitoring, no escalation needed. "
        "  - If no outliers → state that the scope shows no significant deviations. "
        "Recommendations must reference specific groups by their expanded names. "

        # ── STYLE REQUIREMENTS ────────────────────────────────────────────
        "STYLE REQUIREMENTS: "
        "- Write in narrative, professional English. "
        "- Be descriptive and detailed — this report should stand on its own without access "
        "  to the underlying data. A reader who has never seen the CSV should understand "
        "  exactly what was found. "
        "- Use the expanded group_key descriptions everywhere; NEVER show raw coded keys "
        "  like 'ist|fco|1' in the final report. "
        "- Present numbers with appropriate precision (integers for counts, 1-2 decimals for "
        "  scores and ratios). "
        "- Avoid excessive tables; prefer prose with inline numbers. A summary table is "
        "  acceptable for the Risk Distribution section. "
        "- Do NOT use domain-specific terms that assume the dataset is about flights. Use "
        "  'groups', 'entities', 'records', 'events' as generic terms. The expanded group_key "
        "  already tells the reader what the entities are. "
        "- Do not invent data or fabricate numbers. Every number in the report must come from "
        "  risk_report.csv. "

        # ── HARD CONSTRAINTS ──────────────────────────────────────────────
        "Hard constraints: "
        "- Do NOT load any CSV other than risk_report.csv. All context comes from the manifest "
        "  and column profiles embedded in this prompt, plus your world knowledge for decoding "
        "  coded values. "
        "- Do NOT crash if risk_report.csv is empty. Write a short 'no anomalies' report. "
        "- The code must run top-to-bottom without user input. "

        # ── OUTPUT ────────────────────────────────────────────────────────
        f"Write the final markdown to '{OUTPUT_DIR}/anomaly_report.md' using utf-8 encoding. "
        "Print the full report to stdout as well, so it appears in the supervisor logs. "
    )


# ---- Gradio application wrapper ----
import shutil
import time
import uuid
from pathlib import Path


def configure_paths(project_root: str) -> None:
    """Reconfigure notebook globals so each Gradio run is isolated."""
    global PROJECT_ROOT, DATA_DIR, RAW_DIR, ALLARMI_CSV, TIPOLOGIA_CSV
    global OUTPUT_DIR, FINDINGS_JSON, COLUMN_PROFILES_JSON, CLEANING_PLAN_JSON, SCOPE_MANIFEST_JSON

    PROJECT_ROOT = os.path.abspath(project_root)
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")
    RAW_DIR = os.path.join(DATA_DIR, "raw")
    ALLARMI_CSV = os.path.join(RAW_DIR, "ALLARMI.csv")
    TIPOLOGIA_CSV = os.path.join(RAW_DIR, "TIPOLOGIA_VIAGGIATORE.csv")
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
    FINDINGS_JSON = os.path.join(OUTPUT_DIR, "findings.json")
    COLUMN_PROFILES_JSON = os.path.join(OUTPUT_DIR, "column_profiles.json")
    CLEANING_PLAN_JSON = os.path.join(OUTPUT_DIR, "cleaning_plan.json")
    SCOPE_MANIFEST_JSON = os.path.join(OUTPUT_DIR, "scope_manifest.json")

    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    refresh_agent_globals()


def refresh_agent_globals() -> None:
    """Keep the LLM-executed agents aligned with current helper functions and paths."""
    global AGENT_GLOBALS
    AGENT_GLOBALS = {
        "__name__": "__agent__",
        "os": os,
        "json": json,
        "np": np,
        "pd": pd,
        "build_group_key": build_group_key,
        "drop_empty_keys": drop_empty_keys,
        "apply_scope_filters": apply_scope_filters,
        "aggregate_baseline": aggregate_baseline,
        "compute_zscore_per_dataset": compute_zscore_per_dataset,
        "compute_ratio_to_baseline": compute_ratio_to_baseline,
        "flag_outliers_hybrid": flag_outliers_hybrid,
        "filter_by_scope_keys": filter_by_scope_keys,
        "OUTPUT_DIR": OUTPUT_DIR,
        "SCOPE_MANIFEST_JSON": SCOPE_MANIFEST_JSON,
        "COLUMN_PROFILES_JSON": COLUMN_PROFILES_JSON,
    }


def _as_upload_path(uploaded) -> str | None:
    if uploaded is None:
        return None
    if isinstance(uploaded, str):
        return uploaded
    return getattr(uploaded, "name", None)


def _copy_input_files(allarmi_file, tipologia_file) -> None:
    allarmi_src = _as_upload_path(allarmi_file)
    tipologia_src = _as_upload_path(tipologia_file)

    if allarmi_src:
        shutil.copyfile(allarmi_src, ALLARMI_CSV)
    elif not os.path.exists(ALLARMI_CSV):
        raise FileNotFoundError("Carica ALLARMI.csv oppure mettilo in data/raw/ALLARMI.csv")

    if tipologia_src:
        shutil.copyfile(tipologia_src, TIPOLOGIA_CSV)
    elif not os.path.exists(TIPOLOGIA_CSV):
        raise FileNotFoundError("Carica TIPOLOGIA_VIAGGIATORE.csv oppure mettilo in data/raw/TIPOLOGIA_VIAGGIATORE.csv")


def _build_or_load_profiles(force_rebuild: bool = False) -> dict:
    if (
        not force_rebuild
        and os.path.exists(COLUMN_PROFILES_JSON)
        and os.path.exists(CLEANING_PLAN_JSON)
        and os.path.getsize(COLUMN_PROFILES_JSON) > 0
        and os.path.getsize(CLEANING_PLAN_JSON) > 0
    ):
        return {"status": "cache", "profiles": COLUMN_PROFILES_JSON, "plan": CLEANING_PLAN_JSON}

    profiles = run_pre_pipeline_column_profiling(
        datasets=[
            ("allarmi_raw", ALLARMI_CSV),
            ("tipologia_raw", TIPOLOGIA_CSV),
        ]
    )
    return {"status": "rebuilt", "profiles": COLUMN_PROFILES_JSON, "plan": CLEANING_PLAN_JSON}


def _run_cleaning() -> list[dict]:
    reports = []
    datasets_to_clean = [
        ("allarmi_raw", ALLARMI_CSV, os.path.join(OUTPUT_DIR, "allarmi_clean.csv")),
        ("tipologia_raw", TIPOLOGIA_CSV, os.path.join(OUTPUT_DIR, "tipologia_clean.csv")),
    ]
    for dataset_key, input_path, output_path in datasets_to_clean:
        report = clean_dataset(
            input_csv_path=input_path,
            output_csv_path=output_path,
            cleaning_plan_path=CLEANING_PLAN_JSON,
            dataset_key=dataset_key,
        )
        reports.append(report)
    return reports


def _run_supervised_agents(max_retries: int) -> dict:
    results = {}

    results["data_agent"] = run_agent_with_supervisor(
        task_name="data_agent",
        prompt=_build_data_agent_prompt(),
        validator_fn=validate_data_agent_output,
        output_path=SCOPE_MANIFEST_JSON,
        max_retries=max_retries,
    )
    if not results["data_agent"]["succeeded"]:
        return results

    baseline_output_csv = os.path.join(OUTPUT_DIR, "baseline_data.csv")
    results["baseline"] = run_agent_with_supervisor(
        task_name="baseline",
        prompt=_build_baseline_prompt(),
        validator_fn=validate_baseline_output,
        output_path=baseline_output_csv,
        max_retries=max_retries,
    )
    if not results["baseline"]["succeeded"]:
        return results

    outlier_output_csv = os.path.join(OUTPUT_DIR, "outliers.csv")
    results["outlier_detection"] = run_agent_with_supervisor(
        task_name="outlier_detection",
        prompt=_build_outlier_prompt(),
        validator_fn=validate_outlier_output,
        output_path=outlier_output_csv,
        max_retries=max_retries,
    )
    if not results["outlier_detection"]["succeeded"]:
        return results

    risk_output_csv = os.path.join(OUTPUT_DIR, "risk_report.csv")
    results["risk_profiling"] = run_agent_with_supervisor(
        task_name="risk_profiling",
        prompt=_build_risk_prompt(),
        validator_fn=validate_risk_output,
        output_path=risk_output_csv,
        max_retries=max_retries,
    )
    if not results["risk_profiling"]["succeeded"]:
        return results

    report_output_md = os.path.join(OUTPUT_DIR, "anomaly_report.md")
    results["report"] = run_agent_with_supervisor(
        task_name="report",
        prompt=_build_report_prompt(),
        validator_fn=validate_report_output,
        output_path=report_output_md,
        max_retries=max_retries,
    )
    return results


def _summarize_agent_results(results: dict) -> str:
    lines = []
    for name, result in results.items():
        status = "OK" if result.get("succeeded") else "FAILED"
        attempts = result.get("attempts", "?")
        lines.append(f"{name}: {status} ({attempts} attempt)")
        validation = result.get("last_validation") or {}
        for check in validation.get("checks", [])[:8]:
            mark = "✓" if check.get("ok") else "✗"
            lines.append(f"  {mark} {check.get('name')}: {check.get('detail')}")
        stderr = (result.get("last_stderr") or "").strip()
        if stderr and not result.get("succeeded"):
            lines.append("  stderr tail:")
            lines.extend("    " + x for x in stderr.splitlines()[-8:])
    return "\n".join(lines)


def run_pipeline_gradio(
    user_query: str,
    allarmi_file,
    tipologia_file,
    mistral_api_key: str,
    force_rebuild_profiles: bool,
    max_retries: int,
    progress=gr.Progress(track_tqdm=False),
):
    """Entry point used by the Gradio interface."""
    global USER_QUERY, MISTRAL_API_KEY, _client

    user_query = (user_query or "").strip()
    if not user_query:
        raise gr.Error("Inserisci una query, per esempio: 'show me anomalous routes from IST to FCO'.")

    key = (mistral_api_key or os.getenv("MISTRAL_API_KEY", "")).strip()
    if not key:
        raise gr.Error("Manca MISTRAL_API_KEY. Inseriscila nel campo API key o impostala nel file .env.")

    MISTRAL_API_KEY = key
    _client = OpenAI(base_url=MISTRAL_BASE_URL, api_key=MISTRAL_API_KEY)

    run_id = time.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    run_root = os.path.join(os.getcwd(), "gradio_runs", run_id)
    configure_paths(run_root)
    USER_QUERY = user_query

    progress(0.05, desc="Preparazione file")
    _copy_input_files(allarmi_file, tipologia_file)

    progress(0.15, desc="Profiling colonne e piano di cleaning")
    profile_status = _build_or_load_profiles(force_rebuild=force_rebuild_profiles)

    progress(0.30, desc="Cleaning dataset")
    cleaning_reports = _run_cleaning()

    progress(0.45, desc="Esecuzione agenti")
    results = _run_supervised_agents(max_retries=int(max_retries))

    progress(0.90, desc="Preparazione output")
    report_path = os.path.join(OUTPUT_DIR, "anomaly_report.md")
    risk_path = os.path.join(OUTPUT_DIR, "risk_report.csv")
    manifest_path = SCOPE_MANIFEST_JSON
    baseline_path = os.path.join(OUTPUT_DIR, "baseline_data.csv")
    outliers_path = os.path.join(OUTPUT_DIR, "outliers.csv")

    report_text = ""
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()
    else:
        report_text = "Il report finale non è stato generato. Controlla il log agenti."

    risk_df = pd.DataFrame()
    if os.path.exists(risk_path):
        risk_df = pd.read_csv(risk_path)

    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    log = {
        "run_root": run_root,
        "profile_status": profile_status,
        "cleaning_reports": cleaning_reports,
        "agents": _summarize_agent_results(results),
    }

    files = [p for p in [report_path, risk_path, manifest_path, baseline_path, outliers_path] if os.path.exists(p)]
    progress(1.0, desc="Completato")
    return report_text, risk_df, manifest, json.dumps(log, indent=2, ensure_ascii=False), files


def build_demo() -> gr.Blocks:
    with gr.Blocks(title="Multi-Agent Anomaly Detection Pipeline") as demo:
        gr.Markdown(
            "# Multi-Agent Anomaly Detection Pipeline\n"
            "Interfaccia Gradio per eseguire la pipeline del notebook: profiling, cleaning, "
            "scope manifest, baseline, outlier detection, risk profiling e report finale."
        )

        with gr.Row():
            with gr.Column(scale=1):
                user_query = gr.Textbox(
                    label="Query utente",
                    value="show me anomaly routes",
                    lines=3,
                    placeholder="Esempio: show me anomalous routes from IST to FCO",
                )
                allarmi_file = gr.File(label="ALLARMI.csv", file_types=[".csv"])
                tipologia_file = gr.File(label="TIPOLOGIA_VIAGGIATORE.csv", file_types=[".csv"])
                mistral_api_key = gr.Textbox(
                    label="MISTRAL_API_KEY",
                    type="password",
                    placeholder="Lascia vuoto se già presente in .env",
                )
                with gr.Row():
                    force_rebuild = gr.Checkbox(label="Rigenera profiling/cleaning plan", value=True)
                    max_retries = gr.Slider(label="Retry per agente", minimum=0, maximum=5, step=1, value=3)
                run_btn = gr.Button("Esegui pipeline", variant="primary")

            with gr.Column(scale=2):
                report = gr.Markdown(label="Report finale")
                risk_table = gr.Dataframe(label="Risk report", interactive=False)
                manifest = gr.JSON(label="Scope manifest")
                log = gr.Code(label="Log", language="json")
                output_files = gr.Files(label="File generati")

        run_btn.click(
            fn=run_pipeline_gradio,
            inputs=[user_query, allarmi_file, tipologia_file, mistral_api_key, force_rebuild, max_retries],
            outputs=[report, risk_table, manifest, log, output_files],
        )
    return demo


if __name__ == "__main__":
    demo = build_demo()
    demo.launch()
