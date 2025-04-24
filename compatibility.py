#!/usr/bin/env python3
"""
compatibility.py
================
Predicts applicant-to-team compatibility for the Datahouse take-home.

Run:
    python compatibility.py sample_input.json > output.json
"""

import json            # Built-in: parse / emit JSON
import math            # sqrt for Euclidean distance
import sys             # Command-line args & stdout typing
from typing import Dict, List



# Helper functions


def mean_vector(team: List[Dict]) -> Dict[str, float]:
    """Return the average value for each attribute across the whole team.

    Args:
        team: List of team-member objects, each containing an "attributes" dict.

    Returns:
        Dict whose keys are attribute names and values are the mean attribute
        value (float) over all team members.
    """
    totals: Dict[str, float] = {}           # Accumulator for attribute sums
    for member in team:                     # ── iterate through each teammate
        for key, value in member["attributes"].items():
            # Add current value to running total for this key
            totals[key] = totals.get(key, 0.0) + value
    # Divide each accumulated total by team size to get the mean
    return {k: totals[k] / len(team) for k in totals}


def euclidean(a: Dict[str, float], b: Dict[str, float]) -> float:
    """Compute straight-line (L2) distance between two attribute vectors.

    Args:
        a: Dict of attribute values.
        b: Dict of attribute values with the same keys as `a`.

    Returns:
        Non-negative float representing Euclidean distance.
    """
    # Σ (a_i − b_i)²  → sqrt
    return math.sqrt(sum((a[k] - b[k]) ** 2 for k in a))


def normalise(distance: float,
              num_attributes: int,
              scale: int = 10) -> float:
    """Map a raw distance into the closed interval [0, 1].

    Args:
        distance: Raw Euclidean distance for a single applicant.
        num_attributes: How many dimensions are in the vector.
        scale: Maximum possible attribute value (10 per the PDF).

    Returns:
        Float in [0, 1] where 1 ≡ perfect match, 0 ≡ worst case.
    """
    # Worst-case distance: (scale) units apart on every dimension
    max_distance = math.sqrt(num_attributes * (scale ** 2))
    return 1 - distance / max_distance       # Invert so larger = better



# Core scoring routine


def score_applicants(team: List[Dict],
                     applicants: List[Dict]) -> List[Dict]:
    """Compute compatibility scores for each applicant.

    Args:
        team: List of current team members (with attributes).
        applicants: List of applicant objects (with attributes).

    Returns:
        New list of dicts, each containing "name" and rounded "score".
    """
    team_mean = mean_vector(team)                # Pre-compute centroid
    num_attrs = len(team_mean)                   # Dimensionality for scaling
    scored: List[Dict] = []                      # Output container

    for person in applicants:
        # 1 · Euclidean distance to the mean
        dist = euclidean(person["attributes"], team_mean)
        # 2 · Convert to 0–1 scale & round to one decimal
        score = round(normalise(dist, num_attrs), 1) # Can change 1 to 3 for better procision
        # 3 · Append result object
        scored.append({"name": person["name"], "score": score})

    return scored



# Command-line interface


def main() -> None:
    """Entry-point for CLI usage."""
    if len(sys.argv) != 2:
        sys.exit("Usage: python compatibility.py <input.json>")

    # Read input JSON 
    with open(sys.argv[1], encoding="utf-8") as fp:
        data = json.load(fp)                    # Obj with "team" & "applicants"

    # Compute scores
    output = {
        "scoredApplicants": score_applicants(
            data["team"],
            data["applicants"]
        )
    }

    # --- Emit output JSON ---------------------------------------------------
    json.dump(output, sys.stdout, indent=2)     # Pretty-print to stdout


# Execute only when run as script, not when imported
if __name__ == "__main__":
    main()
