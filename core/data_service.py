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
    def __init__(self,
                 params: DataServiceParams = DataServiceParams.default()):
        self.tickers = params.tickers
        self.data_reader_func = None
        self.cdataframes = []
        self.start_date = params.start_date
        self.build_callbacks()

    def get_data_from_yf(self, tickers, start_date):
        return pdreader_data.get_data_yahoo(tickers, start=start_date)

    def build_callbacks(self):
        self.data_reader_func = self.get_data_from_yf
        self.before_start = self.before_start_yfinance

    def load(self):
        self.before_start()
        tickers_data = self.data_reader_func(
            self.convert_tickers(self.tickers), self.start_date
        )
        for ticker, ticker_yf in zip(self.tickers,
                                     self.convert_tickers(self.tickers)):
            df_dict = {
                "close": tickers_data["Adj Close"][ticker_yf],
                "open": tickers_data["Open"][ticker_yf],
                "high": tickers_data["High"][ticker_yf],
                "low": tickers_data["Low"][ticker_yf],
                "volume": tickers_data["Volume"][ticker_yf],
                "time": tickers_data.index,
            }
            df = pd.DataFrame(df_dict)
            cdataframe = COHLCDataFrame(df)
            cdataframe._info["ticker"] = ticker
            cdataframe._info["source"] = "yfinance"
            self.cdataframes.append(cdataframe)

    def before_start_yfinance(self):
        import yfinance as yf

        yf.pdr_override()

    def save_prices(self):
        import os

        path = "pricesdata"
        os.makedirs(path, exist_ok=True)
        for cdf in self.cdataframes:
            file = f"prices_{cdf.ticker}.csv"
            filename = os.path.join(path, file)
            print(f"prices file: {filename}")
            cdf.save_price(filename)

    def convert_single_ticker(self, ticker):
        if ".SA" in ticker:
            return ticker
        return f"{ticker}.SA"

    def convert_tickers(self, tickers):
        return [self.convert_single_ticker(ticker) for ticker in tickers]
