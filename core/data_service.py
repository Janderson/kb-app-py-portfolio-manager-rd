from typing import List
from dataclasses import dataclass
import pandas_datareader.data as pdreader_data
from core.cdataframe import COHLCDataFrame
import pandas as pd
from datetime import date


@dataclass
class DataServiceParams:
    tickers: List[str]
    start_date: date

    @classmethod
    def default(cls):
        return DataServiceParams(tickers=[], start_date=date.today())


class DataService:
    def __init__(self, params: DataServiceParams = DataServiceParams.default()):
        self.tickers = params.tickers
        self.data_reader_func = None
        self.cdataframes = []
        self.start_date = params.start_date
        self.build_callbacks()

    def get_data_from_yf(self, tickers, start_date):
        return pdreader_data.get_data_yahoo(tickers, start=start_date)

    def build_callbacks(self):
        self.data_reader_func = self.get_data_from_yf # , start=start_date

    def load(self):
        tickers_data = self.data_reader_func(self.convert_tickers(self.tickers), self.start_date)
        for ticker, ticker_yf in zip(self.tickers, self.convert_tickers(self.tickers)):
            df_dict = {
                "close": tickers_data["Adj Close"][ticker_yf],
                "open": tickers_data["Open"][ticker_yf],
                "high": tickers_data["High"][ticker_yf],
                "low": tickers_data["Low"][ticker_yf],
                "volume": tickers_data["Volume"][ticker_yf],
                "time": tickers_data.index
            }
            df = pd.DataFrame(df_dict)
            cdataframe = COHLCDataFrame(df)
            cdataframe.ticker = ticker
            cdataframe.source = "yfinance"
            self.cdataframes.append(cdataframe)

    def save_prices(self):
        import os
        path = "pricesdata"
        os.makedirs(path, exist_ok=True)
        for cdf in self.cdataframes:
            file = f"prices_{cdf.ticker}.csv"
            filename = os.path.join(path, file)
            print(f"prices file: {filename}")
            cdf.save_price(filename)

    def convert_tickers(self, tickers):
        return [f"{ticker}.SA" for ticker in tickers]
