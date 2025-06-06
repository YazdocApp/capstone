import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import unittest
from data_utils import load_data
from model import SimpleModel
import os

class TestModel(unittest.TestCase):
    def test_fit_predict(self):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'samples.csv')
        data = load_data(data_path)
        model = SimpleModel()
        model.fit(data)
        # Expect a mean value for F1
        pred = model.predict('F1', [0.5, 0.6])
        self.assertAlmostEqual(pred, 1.0, places=3)

if __name__ == '__main__':
    unittest.main()
