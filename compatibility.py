#!/usr/bin/env python3
"""
compatibility.py  –  Datahouse take-home
Run:  python compatibility.py input.json > output.json
"""

import json               # built-in: turns JSON ↔ Python objects
import math
import sys
from typing import Dict, List

# ---------- 1. Helper functions -------------------------------------------

def mean_vector(team: List[Dict]) -> Dict[str, float]:
    """
    Return the average value for every attribute across the whole team.

    Example:
    team = [
      {"attributes": {"intelligence": 1, "strength": 5}},
      {"attributes": {"intelligence": 9, "strength": 4}},
    ]
    --> {"intelligence": 5.0, "strength": 4.5}
    """
    totals: Dict[str, float] = {}
    for member in team:
        for key, value in member["attributes"].items():
            totals[key] = totals.get(key, 0.0) + value
    return {k: totals[k] / len(team) for k in totals}


def euclidean(a: Dict[str, float], b: Dict[str, float]) -> float:
    """Straight-line distance between two attribute vectors."""
    return math.sqrt(sum((a[k] - b[k]) ** 2 for k in a))


def normalise(distance: float, num_attributes: int, scale: int = 10) -> float:
    """
    Map a raw distance to the 0–1 range.
    `scale` is the largest value any attribute can take (10 in the PDF sample).
    """
    max_distance = math.sqrt(num_attributes * (scale ** 2))
    return 1 - distance / max_distance


# ---------- 2. Core scoring routine ---------------------------------------

def score_applicants(team: List[Dict], applicants: List[Dict]) -> List[Dict]:
    team_mean = mean_vector(team)
    num_attrs = len(team_mean)

    scored = []
    for person in applicants:
        dist   = euclidean(person["attributes"], team_mean)
        score  = round(normalise(dist, num_attrs), 3)  # keep 3 decimals
        scored.append({"name": person["name"], "score": score})
    return scored


# ---------- 3. Command-line interface -------------------------------------

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python compatibility.py input.json")

    with open(sys.argv[1]) as fp:
        data = json.load(fp)

    output = {
        "scoredApplicants": score_applicants(data["team"], data["applicants"])
    }

    json.dump(output, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
