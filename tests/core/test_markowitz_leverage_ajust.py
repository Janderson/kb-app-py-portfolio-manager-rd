from core.markowitz import run_markowitz, calculate, apply_leveraged, AdjustLeverageParams, return_series_leverage, LeveragedApplier
import unittest
from datetime import date
import pandas as pd

class TestMarkowitzAdjustLeverage(unittest.TestCase):
    def setUp(self) -> None:
        fixture_path1 = "tests/fixture_returns.csv"
        fixture_path2 = "tests/fixture_closes2.csv"
        self.fake_stocks1 = ["BOVA11.SA","SMAL11.SA"]
        self.fake_stocks2 = ["ITSA4","PETR4","BBSE3","VALE3","ELET3"]
        self.fake_returns1 = pd.read_csv(fixture_path1)
        self.fake_prices2 = pd.read_csv(fixture_path2).set_index(["Date"])
        return super().setUp()

    def test_return_series_leverage_stock1(self):
        stock_a = "ITSA4"
        series_a = self.fake_prices2.pct_change()[stock_a]
        target_return = 1
        observed_leveraged = return_series_leverage(stock_a, series_a, target_return).leverage
        expected_leveraged = (5.38, 5.39)
        self.assertTrue(observed_leveraged >= expected_leveraged[0] and observed_leveraged <= expected_leveraged[1])

    def test_return_series_leverage_stock2(self):
        stock_a = "PETR4"
        series_a = self.fake_prices2.pct_change()[stock_a]
        target_return = 1
        observed_leveraged = return_series_leverage(stock_a, series_a, target_return).leverage
        expected_leveraged = (0.63, 0.64)
        self.assertTrue(observed_leveraged >= expected_leveraged[0] and observed_leveraged <= expected_leveraged[1])

    def test_adjust_leverage_1(self):
        expected_min_vol = 0.2056
        expected_max_sharpe = -0.5350
        expected_stock_a = "ITSA4"
        expected_stock_b = "PETR4"

        expected_return = 0.1
        params = AdjustLeverageParams(expected_return=expected_return)
        leverage_applier = LeveragedApplier(self.fake_prices2, params=params)
        leverage_applier.run()

        self.assertIn(
            expected_stock_a, leverage_applier.prices_leveraged_df.columns
        )
        self.assertIn(
            expected_stock_b, leverage_applier.prices_leveraged_df.columns
        )
        return_a_expeted_rules = [
            leverage_applier.prices_leveraged_df[expected_stock_a] > 0.99,
            leverage_applier.prices_leveraged_df[expected_stock_a] < 1.10
        ]
        self.assertTrue(all(return_a_expeted_rules))

        return_b_expeted_rules = [
            leverage_applier.prices_leveraged_df[expected_stock_a] > 0.99,
            leverage_applier.prices_leveraged_df[expected_stock_a] < 1.10
        ]
        self.assertTrue(all(return_b_expeted_rules))

