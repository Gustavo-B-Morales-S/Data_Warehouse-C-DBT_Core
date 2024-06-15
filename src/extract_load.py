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
    """Retrieves historical closing prices for a specified commodity symbol.
    Parameters:
        symbol (str): The symbol of the commodity to retrieve data for.
        period (str, optional): The time period to retrieve data for. Default is '5D' (5 days).
        interval (str, optional): The time interval between data points. Default is '1D' (daily).
        
    Returns:
        A DataFrame containing the historical closing prices of the specified commodity.
    """
    ticker: Ticker = yf.Ticker(ticker=symbol)
    data: DataFrame = ticker.history(period=period, interval=interval)[['Close']]
    data.insert(loc=0, column='symbol', value=symbol)

    return data


def get_all_commodities_data(commodities: tuple) -> DataFrame:
    """Retrieves historical closing prices for multiple commodity symbols.

    Parameters:
        commodities (tuple): 
            A tuple containing symbols of commodities for which 
            historical data needs to be retrieved.
    Returns:
        A DataFrame containing the concatenated historical closing prices 
        of all specified commodities.
    """
    all_data: Generator[DataFrame] = (get_commoditie_data(symbol)
                                      for symbol in commodities)

    return pd.concat(objs=all_data)


def load_in_database(df: DataFrame, schema: str) -> None:
    """
    Loads a DataFrame into a PostgreSQL database table named 'commodities' 
    within the specified schema using SQLAlchemy engine connection.

    Parameters:
        df (DataFrame):
            The DataFrame containing the data to be loaded into the database.
        schema (str):
            The schema name where the 'commodities' table exists or should be created.
    """
    df.to_sql(name='commodities', con=engine,
              if_exists='replace', index=True,
              index_label='date', schema=schema)
    
    print(f'The data was saved in schema -> {schema} <- in the PostgreSQL DB')


if __name__ == '__main__':
    df: DataFrame = get_all_commodities_data(commodities=commodities)
    load_in_database(df=df, schema='public')
