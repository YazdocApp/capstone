import csv
from typing import List, Tuple


def load_data(path: str) -> List[Tuple[str, List[float], float]]:
    """Load sample data from a CSV file.

    Returns a list of (function_name, vector, score) tuples.
    Missing values are ignored."""
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            func = row["function"].strip()
            vec = []
            for i in range(1, 9):
                v = row.get(f"x{i}")
                if v is not None and v != "":
                    vec.append(float(v))
            score_str = row.get("score")
            score = float(score_str) if score_str not in (None, "") else 0.0
            rows.append((func, vec, score))
    return rows
