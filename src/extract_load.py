# Thirdy-Party Libraries
import yfinance as yf
import pandas as pd

from yfinance import Ticker
from pandas import DataFrame
from typing import Generator

# Local Modules
from database_connection import engine

# Setting the requested commodities
commodities = ('CL=F', 'GC=F', 'SI=F')  # Petroleum & Gold & Silver

def get_commoditie_data(symbol: str, period: str = '5D', interval: str = '1D') -> DataFrame:
    ticker: Ticker = yf.Ticker(ticker=symbol)
    data: DataFrame = ticker.history(period=period, interval=interval)[['Close']]
    data.insert(loc=0, column='Symbol', value=symbol)

    return data


def get_all_commodities_data(commodities: tuple) -> DataFrame:
    all_data: Generator[DataFrame] = (get_commoditie_data(symbol)
                                      for symbol in commodities)

    return pd.concat(objs=all_data)


def load_in_database(df: DataFrame, schema: str) -> None:
    df.to_sql(name='commodities', con=engine,
              if_exists='replace', index=True,
              index_label='Date', schema=schema)
    
    print(f'The data was saved in schema -> {schema} <- in the PostgreSQL database')


if __name__ == '__main__':
    df: DataFrame = get_all_commodities_data(commodities=commodities)
    load_in_database(df=df, schema='public')
