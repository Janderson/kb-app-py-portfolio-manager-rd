from abc import ABC, abstractmethod
import pandas as pd
from typing import List

DATAFRAME_COLUMNS = ["time", "open", "high", "low", "close", "volume"]


class CDataFrame(ABC):
    def __init__(self, dataframe, info={}):
        self.__dataframe = dataframe
        self._info = info
        self.source = None
        if self.is_valid():
            self.parse()

    @property
    def index(self):
        return self.__dataframe.index

    @property
    def dataframe(self):
        return self.__dataframe

    @property
    def info(self):
        return self._info

    def get(self):
        return self.__dataframe.copy()

    def set(self, dataframe):
        self.__dataframe = dataframe
    
    @property
    def ticker(self):
        return self._info.get("ticker")

    @abstractmethod
    def parse(self):
        pass

    def is_valid(self):
        return all(
            [len(set(DATAFRAME_COLUMNS) - set(list(self.dataframe.columns))) == 0]
        )

    @property
    def columns(self):
        return list(self.dataframe.columns)

    @staticmethod
    def is_type_obj(obj):
        return any([isinstance(obj, CDataFrame), issubclass(obj.__class__, CDataFrame)])


class COHLCDataFrame(CDataFrame):
    def parse(self):
        if "ticker" in self.dataframe.columns:
            self._info["ticker"] = self.dataframe.ticker.iloc[0]
        if "timeframe" in self.dataframe.columns:
            self._info["timeframe"] = self.dataframe.timeframe.iloc[0]
        self.set(
            self.dataframe[DATAFRAME_COLUMNS].sort_values(["time"], ascending=True)
        )

    def save_price(self, filename):
        price_column = "close"
        df_to_export = self.dataframe.reset_index()[["time", price_column]]
        df_to_export.columns = ["time", self.ticker]
        df_to_export.to_csv(filename, index=None)


class CCalcDataFrame(CDataFrame):
    def __init__(self, dataframe, info={}):
        super().__init__(dataframe, info=info)

    def parse(self):
        pass


class CDataFramesJoined:
    def __init__(self, cdataframes: List[CDataFrame]):
        self.cdataframes = cdataframes

    @property
    def tickers(self):
        return sorted([cdf.ticker for cdf in self.cdataframes], reverse=False)

    def convert_cdf_to_df(self, cdf: COHLCDataFrame):
        df = cdf.get()[['time', 'close']]
        df.columns = ['time', cdf.ticker]
        df.set_index(["time"], inplace=True)
        return df
    
    def join(self):
        dfs = [self.convert_cdf_to_df(cdf)
                              for cdf in self.cdataframes]
        final_df = pd.concat(dfs, join="inner", axis=1).reset_index()
        return final_df.rename({"time": "Date"}, axis=1).set_index(["Date"])
        
