import unittest
from datetime import date
from core.data_service import DataService, DataServiceParams
import pandas as pd


class TestDataService(unittest.TestCase):
    def setUp(self):
        self.fixture_file = "tests/core/fixture_data_service_pandas_reader.csv"

        def fake_pandas_reader_func(tickers, start_date):
            return self.load_multiindex_pandas(self.fixture_file)

        self.fake_pandas_reader_func = fake_pandas_reader_func

    def load_multiindex_pandas(self, filename):
        # referencia:
        # https://stackoverflow.com/questions/19103624/load-csv-to-pandas-multiindex-dataframe
        return pd.read_csv(filename, header=[0, 1], index_col=[0])

    def test_load_data_service(self):
        params = DataServiceParams(tickers=[], start_date=date.today())
        data_service = DataService(params=params)
        self.assertEqual(data_service.tickers, [])

    def test_convert_tickers(self):
        # GIVEN
        data_service = DataService()
        tickers = ["BOVA11", "SMAL11"]
        expected_tickers = ["BOVA11.SA", "SMAL11.SA"]

        # WHEN
        observed_tickers = data_service.convert_tickers(tickers)

        # THEN
        self.assertEqual(observed_tickers, expected_tickers)

    def test_convert_tickers_2(self):
        # GIVEN
        data_service = DataService()
        tickers = ["BOVA11.SA", "SMAL11.SA"]
        expected_tickers = ["BOVA11.SA", "SMAL11.SA"]

        # WHEN
        observed_tickers = data_service.convert_tickers(tickers)

        # THEN
        self.assertEqual(observed_tickers, expected_tickers)

    def test_load_call_method_1(self):
        expected_tickers = ["BOVA11", "SMAL11"]

        service_params = DataServiceParams(
            tickers=expected_tickers, start_date=date.today()
        )
        data_service = DataService(params=service_params)
        self.observed_tickers = []

        data_service.data_reader_func = self.fake_pandas_reader_func
        data_service.load()

        self.assertEqual(len(expected_tickers), len(data_service.cdataframes))

        index_on_source = [
            index for index in self.fake_pandas_reader_func([], None).index
        ]
        index_on_first_df = [index
                             for index in data_service.cdataframes[0].index]

        self.assertTrue(all([index in index_on_first_df
                             for index in index_on_source]))

    def test_load_call_should_call_converted_tickers(self):
        expected_tickers = ["BOVA11", "SMAL11"]

        service_params = DataServiceParams(
            tickers=expected_tickers, start_date=date.today()
        )
        data_service = DataService(params=service_params)
        self.observed_tickers = []

        def fake_pandas_read(tickers, start_date):
            self.observed_tickers = tickers
            return self.fake_pandas_reader_func(tickers, start_date)

        data_service.data_reader_func = fake_pandas_read

        data_service.load()

        # THEN
        self.assertEqual(
            data_service.convert_tickers(expected_tickers),
            self.observed_tickers
        )
