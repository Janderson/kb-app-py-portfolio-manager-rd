import pandas as pd
import unittest
from core.cdataframe import CDataFrame, COHLCDataFrame


class TestCoreCDataFrame(unittest.TestCase):
    def setUp(self):
        self.dataframe1 = pd.DataFrame([
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-18"), "ticker": "PETR4", "timeframe": "M15"},
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-19"), "ticker": "PETR4", "timeframe": "M15"},
            {"open": 14, "high":14, "low": 14, "close":14, "volume": 14,
                "time": pd.to_datetime("2020-05-14"), "ticker": "PETR4", "timeframe": "M15"},
        ])

    def test_cdatafame_should_return_a(self):
        df = pd.DataFrame()
        dataframe = COHLCDataFrame(df)
        self.assertEqual(type(dataframe.get()), pd.DataFrame)
        self.assertFalse(dataframe.is_valid())

    def test_cdatafame_should_be_valid(self):
        df = pd.DataFrame([{"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-18"), "ticker": "PETR4"}
        ])
        cdataframe = COHLCDataFrame(df)
        self.assertTrue(cdataframe.is_valid())
        self.assertTrue(list(cdataframe.dataframe.columns) == ["time", "open", "high", "low", "close", "volume"])

    def test_cdatafame_with_data_inside_should_be_valid(self):
        cdataframe = COHLCDataFrame(self.dataframe1)
        self.assertTrue(cdataframe.is_valid())
        self.assertTrue(list(cdataframe.dataframe.columns) == ["time", "open", "high", "low", "close", "volume"])
        self.assertEqual(cdataframe.dataframe.iloc[0].time, pd.to_datetime("2020-05-14"))

    def test_cdatafame_with_ticker_columns_should_get_this_info(self):
        cdataframe = COHLCDataFrame(self.dataframe1)
        self.assertTrue(cdataframe.is_valid())
        self.assertEqual(cdataframe.info["ticker"], "PETR4")
        self.assertEqual(cdataframe.info["timeframe"], "M15")
