from data_utils import load_data
from model import RandomSearchOptimizer
import os


def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples.csv')
    data = load_data(data_path)

    # gather best known vector per function (first occurrence)
    best_vectors = {}
    for func, vec, _ in data:
        best_vectors.setdefault(func, vec)

    for func, vec in sorted(best_vectors.items()):
        opt = RandomSearchOptimizer(dim=len(vec), best_vec=vec)
        suggestions = opt.suggest(n=3)
        print(f"Suggestions for {func}:")
        for s in suggestions:
            print(' ', s)

if __name__ == '__main__':
    main()
