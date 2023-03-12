from core.markowitz import run_markowitz, calculate, adjust_leverage
import unittest
from datetime import date
import pandas as pd

class TestE2EMarkowitz(unittest.TestCase):
    @unittest.skip("not call, alltime yfinance")
    def test_e2e_refactor_run_markowitz(self):
        stocks = ["BOVA11.SA", "SMAL11.SA"]
        start_date = date(2023, 1, 1)
        expected_min_vol = 0.2056
        expected_max_sharpe = -0.5350
        observed_min_vol, observed_max_sharpe = run_markowitz(stocks=stocks, start_date=start_date.isoformat())

        self.assertEqual(round(expected_min_vol, 4), round(observed_min_vol, 4))
        self.assertEqual(round(expected_max_sharpe, 4), round(observed_max_sharpe, 4))


class TestMarkowitz(unittest.TestCase):
    def setUp(self) -> None:
        fixture_path = "tests/core/fixture_test_e2e_refactor_run_markowitz_with_file.csv"
        self.fake_yfinance_results = pd.read_csv(fixture_path, index_col="Date")
        self.fake_stocks = ["BOVA11.SA", "SMAL11.SA"]
        return super().setUp()

    def test_e2e_refactor_run_markowitz_with_file(self):
        expected_min_vol = 0.2056
        expected_max_sharpe = -0.5350
        observed_min_vol, observed_max_sharpe = calculate(self.fake_yfinance_results, stocks=self.fake_stocks)

        self.assertEqual(round(expected_min_vol, 4), round(observed_min_vol, 4))
        self.assertEqual(round(expected_max_sharpe, 4), round(observed_max_sharpe, 4))


