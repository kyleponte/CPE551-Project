"""
Data processing utilities for traffic signal volume data.

Combines CSV I/O helpers, cleaning functions, grouping utilities, and
generators for streaming data in chunks. Merges functionality needed by
both teammates' commits (file-based streaming + record-level streaming).
"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, List, Tuple

import pandas as pd

REQUIRED_COLUMNS = {"intersection_id", "timestamp", "count"}


def load_traffic_data(filepath: str | Path) -> pd.DataFrame:
    """
    Load traffic signal data from CSV and perform basic cleaning.

    Uses pandas for critical CSV I/O (Part 1 requirement), validates required
    columns, and ensures timestamps/counts are parsed.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Traffic data file not found: {path}")

    try:
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError(f"Data file is empty: {path}")

        _validate_required_columns(df.columns)

        df = df.dropna(subset=["intersection_id", "count"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        df["count"] = pd.to_numeric(df["count"], errors="coerce")
        df = df.dropna(subset=["count"])

        return df
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise Exception(f"Error loading traffic data: {exc}") from exc


def volume_stream(
    source: str | Path | pd.DataFrame,
    chunk_size: int = 1000,
    approach: str | None = None,
) -> Generator[Any, None, None]:
    """
    Generator for streaming traffic data.

    Supports two modes:
    - File path: yields cleaned DataFrame chunks (chunked CSV read).
    - DataFrame: yields record dictionaries (optionally filtered by approach).
    """
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        for chunk in pd.read_csv(path, chunksize=chunk_size):
            _validate_required_columns(chunk.columns)
            chunk = chunk.dropna(subset=["intersection_id", "count"])
            chunk["timestamp"] = pd.to_datetime(chunk["timestamp"], errors="coerce")
            chunk = chunk.dropna(subset=["timestamp"])
            chunk["count"] = pd.to_numeric(chunk["count"], errors="coerce")
            chunk = chunk.dropna(subset=["count"])
            yield chunk
        return

    df = source
    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        return

    if approach:
        if "approach" not in df.columns:
            raise ValueError("'approach' column not found in data")
        df = df[df["approach"] == approach]

    for _, row in df.iterrows():
        yield row.to_dict()


def group_by_intersection_and_day(df: pd.DataFrame) -> Dict[Tuple[str, object], List[object]]:
    """
    Group traffic records by (intersection_id, day) using itertools.groupby.
    """
    _validate_required_columns(df.columns)
    if "timestamp" not in df.columns:
        raise ValueError("timestamp column is required for grouping.")

    df_sorted = df.sort_values(["intersection_id", "timestamp"])

    grouped: Dict[Tuple[str, object], List[object]] = {}
    for key, group in itertools.groupby(
        df_sorted.itertuples(index=False),
        key=lambda row: (row.intersection_id, row.timestamp.date()),
    ):
        grouped[key] = list(group)

    return grouped


def aggregate_by_hour(data: pd.DataFrame, volume_col: str = "count") -> Dict[int, float]:
    """
    Aggregate volumes by hour with empty-bin handling.
    """
    if data is None or (isinstance(data, pd.DataFrame) and data.empty):
        raise ValueError("Data is empty, cannot aggregate")

    required_columns = {"hour", volume_col}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    hourly_data: Dict[int, float] = {}
    for hour in range(24):
        try:
            hour_data = data[data["hour"] == hour]
            hourly_data[hour] = hour_data[volume_col].sum() if not hour_data.empty else 0
        except Exception:
            hourly_data[hour] = 0

    return hourly_data


def save_results(results: pd.DataFrame | Dict[str, Any], output_path: str | Path) -> None:
    """
    Save analysis results to CSV (data I/O requirement).

    Accepts either a DataFrame or a dictionary payload.
    """
    try:
        if results is None:
            raise ValueError("Results cannot be None")

        if isinstance(results, dict):
            if not results:
                raise ValueError("Results dictionary is empty")
            results = pd.DataFrame([results])

        if isinstance(results, pd.DataFrame) and results.empty:
            raise ValueError("Results DataFrame is empty")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
    except Exception as exc:
        print(f"Error saving results to {output_path}: {exc}")
        raise


def clean_traffic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and augment traffic data with time-based features.
    """
    _validate_required_columns(df.columns)

    cleaned = df.copy()
    cleaned = cleaned[cleaned["count"] >= 0]
    cleaned = cleaned.dropna(subset=["intersection_id", "count"])

    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], errors="coerce")
    cleaned = cleaned.dropna(subset=["timestamp"])
    cleaned["count"] = pd.to_numeric(cleaned["count"], errors="coerce")
    cleaned = cleaned.dropna(subset=["count"])

    cleaned["hour"] = cleaned["timestamp"].dt.hour
    cleaned["day_of_week"] = cleaned["timestamp"].dt.dayofweek

    return cleaned


def validate_traffic_data(data: pd.DataFrame, count_column: str = "count") -> bool:
    """
    Validate traffic data for required fields and basic data quality checks.
    """
    try:
        if data is None:
            raise ValueError("Data cannot be None")
        if isinstance(data, pd.DataFrame) and data.empty:
            raise ValueError("Data is empty")

        if isinstance(data, pd.DataFrame):
            if count_column not in data.columns:
                print(f"Warning: Missing column '{count_column}'")
                return False

            zero_counts = (data[count_column] == 0).sum()
            missing_counts = data[count_column].isna().sum()
            if zero_counts > 0:
                print(f"Warning: Found {zero_counts} zero counts in data")
            if missing_counts > 0:
                print(f"Warning: Found {missing_counts} missing counts in data")

            numeric_columns = data.select_dtypes(include=["number"]).columns
            for col in numeric_columns:
                if (data[col] < 0).any():
                    print(f"Warning: Negative values detected in '{col}'")

        return True
    except ValueError as exc:
        print(f"Error validating data: {exc}")
        return False
    except Exception as exc:
        print(f"Unexpected error validating data: {exc}")
        return False


def _validate_required_columns(columns: Iterable[str]) -> None:
    """Ensure required columns exist; raise ValueError if any are missing."""
    missing = REQUIRED_COLUMNS.difference(set(columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")


