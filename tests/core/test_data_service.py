import unittest
from core.data_service import DataService


class TestData(unittest.TestCase):
    def test_setup(self):
        pass

    def test_load_data_service(self):
        data_service = DataService()
        self.assertEqual(data_service.tickers, [])

    def test_convert_tickers(self):
        data_service = DataService()

        tickers = ["BOVA11", "SMALL11"]
        expected_tickers = ["BOVA11.SA", "SMALL11.SA"]
        observed_tickers = data_service.convert_tickers(tickers)
        self.assertEqual(observed_tickers, expected_tickers)
