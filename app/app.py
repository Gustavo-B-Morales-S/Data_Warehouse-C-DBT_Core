# Default Libraries
import sys
import os

# Thirdy-Party Libraries
import pandas as pd
from pandas import DataFrame
import streamlit as st


# Add the parent directory (/src) to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database_connection import engine, connection


def get_data() -> DataFrame:
    sql_query = f"""
    SELECT Date,
           Symbol,
           Closing_price,
           Action,
           Quantity,
           Value,
           Gain
           
    FROM Public.DM_Commodities;
    """

    data: DataFrame = pd.read_sql(sql=sql_query, con=engine)

    return data

# Setting Streamlit Configurations
st.set_page_config(page_title='Commodities Dashboard', layout='wide')

# Setting page title
st.title(body='Commodities Dashboard')

# Description
st.write('This dashboard shows data about commodities and their transactions')

# Inserting Data
st.dataframe(data=get_data())
