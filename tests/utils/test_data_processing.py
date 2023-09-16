import unittest
import pandas as pd
from src.utils.data_processing import preprocess_data


class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'Adj Close': [100, 101, 101, 102, 102.5]
        })

    def test_preprocess_data(self):
        result = preprocess_data(self.data.copy())
        self.assertEqual(len(result), 4)

        expected_daily_returns = [0.01, 0.0, 0.0099, 0.0049]
        for computed, expected in zip(result['Adj Close'].tolist(), expected_daily_returns):
            self.assertAlmostEqual(computed, expected, places=4)


if __name__ == '__main__':
    unittest.main()
