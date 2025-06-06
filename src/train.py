from data_utils import load_data
from model import SimpleModel, RandomSearchOptimizer
import os


def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples.csv')
    data = load_data(data_path)

    model = SimpleModel()
    model.fit(data)

    print("Average scores per function:")
    for func, mean in model.func_stats.items():
        print(func, '->', round(mean, 3))

    # Choose best vector for F4 from dataset as starting point
    f4_data = [vec for func, vec, _ in data if func == 'F4']
    if f4_data:
        best_vec = f4_data[0]
        optimizer = RandomSearchOptimizer(dim=len(best_vec), best_vec=best_vec)
        suggestions = optimizer.suggest(n=3)
        print("New suggestions for F4:")
        for s in suggestions:
            print(s)

if __name__ == '__main__':
    main()
