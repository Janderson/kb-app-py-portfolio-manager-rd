import pandas as pd
import unittest
from core.cdataframe import CDataFrame, COHLCDataFrame, CDataFramesJoined


class TestCoreCDataFrame(unittest.TestCase):
    def setUp(self):
        self.dataframe1 = pd.DataFrame([
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-18"), "ticker": "TICKERA", "timeframe": "M15"},
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-19"), "ticker": "TICKERA", "timeframe": "M15"},
            {"open": 14, "high":14, "low": 14, "close":14, "volume": 14,
                "time": pd.to_datetime("2020-05-14"), "ticker": "TICKERA", "timeframe": "M15"},
        ])

    def test_cdatafame_should_return_a(self):
        df = pd.DataFrame()
        dataframe = COHLCDataFrame(df)
        self.assertEqual(type(dataframe.get()), pd.DataFrame)
        self.assertFalse(dataframe.is_valid())

    def test_cdatafame_should_be_valid(self):
        df = pd.DataFrame([{"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-18"), "ticker": "TICKERA"}
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
        self.assertEqual(cdataframe.info["ticker"], "TICKERA")
        self.assertEqual(cdataframe.info["timeframe"], "M15")


class TestCDataFramesJoined(unittest.TestCase):
    def setUp(self):
        dfA =  pd.DataFrame([
            {"open": 14, "high":14, "low": 14, "close":1, "volume": 1000,
                "time": pd.to_datetime("2020-05-14"), "ticker": "TICKERA", "timeframe": "M15"},
            {"open": 1, "high":5, "low": 2, "close":2, "volume": 15000,
                "time": pd.to_datetime("2020-05-15"), "ticker": "TICKERA", "timeframe": "M15"},
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-16"), "ticker": "TICKERA", "timeframe": "M15"},
        ])

        dfB = pd.DataFrame([
            {"open": 1, "high":5, "low": 2, "close":3, "volume": 15000,
                "time": pd.to_datetime("2020-05-14"), "ticker": "TICKERB", "timeframe": "M15"},
            {"open": 1, "high":5, "low": 2, "close":4, "volume": 15000,
                "time": pd.to_datetime("2020-05-15"), "ticker": "TICKERB", "timeframe": "M15"},
            {"open": 14, "high":14, "low": 14, "close":5, "volume": 14,
                "time": pd.to_datetime("2020-05-16"), "ticker": "TICKERB", "timeframe": "M15"},
        ])
        self.dataframeA = COHLCDataFrame(dfA, info={})
        self.dataframeB = COHLCDataFrame(dfB, info={})

    def test_unit_join(self):
        list_cdataframes = [self.dataframeA, self.dataframeB]
        cdfs_joined = CDataFramesJoined(list_cdataframes)


        self.assertEqual(cdfs_joined.tickers,
                         ["TICKERA", "TICKERB"])

        expected_df_shape = cdfs_joined.join().shape
        observed_df_shape = (3, 2)
        self.assertEqual(expected_df_shape,
                         observed_df_shape)


