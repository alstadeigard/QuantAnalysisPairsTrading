import unittest
import pandas as pd

from src.utils.risk_assessment_utils import calculate_max_drawdown, \
    calculate_sharpe_ratio


class TestRiskAssessment(unittest.TestCase):

    def setUp(self):
        self.cum_returns = pd.Series([1, 1.05, 1.02, 1.1, 1.03, 1.2, 1.18])
        self.daily_returns = pd.Series([0, 0.05, -0.03, 0.08, -0.07, 0.17, -0.02])

    def test_calculate_max_drawdown(self):
        expected_max_drawdown = -0.0636
        computed_max_drawdown = calculate_max_drawdown(self.cum_returns)
        self.assertAlmostEqual(computed_max_drawdown, expected_max_drawdown, places=2)

    def test_calculate_sharpe_ratio(self):
        expected_sharpe_ratio = self.daily_returns.mean() / self.daily_returns.std() * (252 ** 0.5)
        computed_sharpe_ratio = calculate_sharpe_ratio(self.daily_returns)
        self.assertAlmostEqual(computed_sharpe_ratio, expected_sharpe_ratio, places=2)


if __name__ == '__main__':
    unittest.main()
