from typing import List
from dataclasses import dataclass


@dataclass
class Ticker:
    ticker: str


class DataService:
    def __init__(self, tickers: List[Ticker] = []):
        self.tickers = tickers

    def load(self):
        pass

    def convert_tickers(self, tickers):
        return [f"{ticker}.SA" for ticker in tickers]
