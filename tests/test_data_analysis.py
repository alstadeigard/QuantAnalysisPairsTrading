import unittest
import pandas as pd
from src.utils.data_analysis import check_cointegration


class TestCheckCointegration(unittest.TestCase):

    def setUp(self):
        # Mock data for testing
        self.stock1 = pd.Series([1, 2, 3, 4, 5, 6])
        self.stock2 = pd.Series([1.1, 2.1, 3.1, 4.1, 5.1, 6.1])
        self.stock3 = pd.Series([6, 5.5, 4.7, 3.5, 2.5, 1.5])


    def test_cointegrated(self):
        are_cointegrated, pvalue = check_cointegration(self.stock1, self.stock2)
        self.assertTrue(are_cointegrated)
        self.assertLess(pvalue, 0.05)

    def test_not_cointegrated(self):
        are_cointegrated, pvalue = check_cointegration(self.stock1, self.stock3)
        self.assertFalse(are_cointegrated)
        self.assertGreaterEqual(pvalue, 0.05)


if __name__ == "__main__":
    unittest.main()
