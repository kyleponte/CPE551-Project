"""
Timing functions for traffic signal analysis.

Provides delay calculations, timing plan generation, and comparison helpers
using advanced Python features (list comprehensions, zip, lambda) plus
exception handling for divide-by-zero scenarios.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

try:
    from timing_plan import TimingPlan
except ImportError:  # Fallback until Kyle's TimingPlan is available

    class TimingPlan:  # type: ignore
        """Minimal timing plan stub to allow local development."""

        def __init__(self, green_times: Dict[str, float], cycle_length: float):
            self.green_times = green_times
            self.cycle_length = cycle_length

        def __add__(self, other: "TimingPlan") -> "TimingPlan":
            combined_keys = set(self.green_times) | set(other.green_times)
            combined = {
                key: (self.green_times.get(key, 0) + other.green_times.get(key, 0)) / 2
                for key in combined_keys
            }
            combined_cycle = (self.cycle_length + other.cycle_length) / 2
            return TimingPlan(combined, combined_cycle)

        def __str__(self) -> str:  # pragma: no cover - convenience only
            return f"TimingPlan(cycle={self.cycle_length:.1f}s, approaches={len(self.green_times)})"


def compute_average_delay(volume: float, green_s: float, cycle_s: float = 90.0) -> float:
    """
    Compute average delay (approximate) for a single approach.

    Uses a simplified delay estimate based on volume-to-capacity ratio.
    Handles divide-by-zero by returning 0.0 and logging the condition.
    """
    try:
        if green_s <= 0:
            raise ZeroDivisionError("Green time must be positive.")

        # Capacity approximation: proportional to green time within cycle
        saturation_flow = 1800  # vehicles per hour per lane
        capacity = (green_s / cycle_s) * saturation_flow

        if capacity <= 0:
            return 0.0

        vc_ratio = volume / capacity if capacity > 0 else 0.0

        # Simple piecewise delay: undersaturated vs. oversaturated
        if vc_ratio < 1.0:
            delay = 0.5 * (1 - vc_ratio) * (green_s / 2)
        else:
            delay = 0.5 * green_s + (vc_ratio - 1) * green_s

        return max(delay, 0.0)
    except ZeroDivisionError:
        print("Warning: Division by zero in delay calculation")
        return 0.0


def generate_timing_plan(df, alternative: bool = False) -> TimingPlan:
    """
    Generate a baseline or alternative timing plan from hourly volumes.

    - List comprehension: build hourly volume averages.
    - Lambda + map: convert volume to green time.
    - zip: pair observed volumes with computed greens (for diagnostics).
    """
    import pandas as pd

    if df is None or len(df) == 0:
        raise ValueError("Input dataframe is empty.")

    if "hour" not in df.columns or "count" not in df.columns:
        raise ValueError("Dataframe must contain 'hour' and 'count' columns.")

    hourly_volumes = [
        df[df["hour"] == hour]["count"].mean()
        for hour in range(24)
    ]

    transform_volume = lambda vol: max(20.0, min(60.0, (vol or 0) * 0.1))  # noqa: E731
    green_times_by_hour = list(map(transform_volume, hourly_volumes))

    volume_green_pairs = list(zip(hourly_volumes, green_times_by_hour))

    approaches = df["approach"].unique() if "approach" in df.columns else ["North"]
    green_time_dict: Dict[str, float] = {}

    for idx, approach in enumerate(approaches):
        base_green = green_times_by_hour[idx % len(green_times_by_hour)]
        green_time_dict[approach] = base_green * (1.2 if alternative else 1.0)

    cycle_length = sum(green_time_dict.values()) + 10.0  # include clearance time

    plan = TimingPlan(green_time_dict, cycle_length)
    # Attach diagnostic pairing for downstream inspection if needed
    plan.volume_green_pairs = volume_green_pairs  # type: ignore[attr-defined]
    return plan


def compare_timing_plans(
    baseline_plan: TimingPlan,
    alt_plan: TimingPlan,
    volumes: List[float],
    default_approach: str | None = "North",
) -> Dict[str, float | List[Tuple[float, float]]]:
    """
    Compare baseline vs. alternative plans using computed delays.

    Uses zip to pair baseline/alternative delays for each volume entry.
    """
    if not volumes:
        return {
            "baseline_avg_delay": 0.0,
            "alternative_avg_delay": 0.0,
            "improvement_percent": 0.0,
            "delay_pairs": [],
        }

    def _green_for(plan: TimingPlan) -> float:
        if default_approach and hasattr(plan, "green_times"):
            return plan.green_times.get(default_approach, next(iter(plan.green_times.values()), 30.0))
        return 30.0

    base_green = _green_for(baseline_plan)
    alt_green = _green_for(alt_plan)

    baseline_delays = [compute_average_delay(vol, base_green) for vol in volumes]
    alt_delays = [compute_average_delay(vol, alt_green) for vol in volumes]

    delay_pairs = list(zip(baseline_delays, alt_delays))

    avg_baseline = sum(baseline_delays) / len(baseline_delays)
    avg_alt = sum(alt_delays) / len(alt_delays)

    improvement = ((avg_baseline - avg_alt) / avg_baseline * 100) if avg_baseline > 0 else 0.0

    return {
        "baseline_avg_delay": avg_baseline,
        "alternative_avg_delay": avg_alt,
        "improvement_percent": improvement,
        "delay_pairs": delay_pairs,
    }

