from typing import List, Tuple
import random
import math


class SimpleModel:
    """A trivial model that memorizes average scores per function."""

    def __init__(self):
        self.func_stats = {}

    def fit(self, data: List[Tuple[str, List[float], float]]):
        sums = {}
        counts = {}
        for func, vec, score in data:
            sums[func] = sums.get(func, 0.0) + score
            counts[func] = counts.get(func, 0) + 1
        self.func_stats = {func: sums[func] / counts[func] for func in sums}

    def predict(self, func: str, vec: List[float]) -> float:
        return self.func_stats.get(func, 0.0)


class RandomSearchOptimizer:
    """Suggests new vectors by random search around the best known vector."""

    def __init__(self, dim: int, best_vec: List[float]):
        self.dim = dim
        self.best_vec = best_vec

    def suggest(self, n: int = 5) -> List[List[float]]:
        suggestions = []
        for _ in range(n):
            candidate = [
                min(1.0, max(0.0, x + random.uniform(-0.05, 0.05)))
                for x in self.best_vec
            ]
            suggestions.append(candidate)
        return suggestions

    def update_best(self, vec: List[float]):
        self.best_vec = vec
