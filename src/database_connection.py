# Default Libraries
from os import getenv

# Third-Party Libraries
from sqlalchemy import Engine, Connection, create_engine
from typing import Tuple
from dotenv import load_dotenv

# Loading enviroment variables
load_dotenv()
DB_HOST = getenv(key='DB_HOST_PROD')
DB_PORT = getenv(key='DB_PORT_PROD')
DB_NAME = getenv(key='DB_NAME_PROD')
DB_USER = getenv(key='DB_USER_PROD')
DB_PASS = getenv(key='DB_PASS_PROD')
DB_SCHEMA = getenv(key='DB_SCHEMA_PROD')
DB_DIALECT = 'postgresql'


def connect_with_database(**connection_parameters) -> Tuple[Engine, Connection]:
    """
    Connects to a database using the provided connection parameters and returns 
    both the SQLAlchemy engine and connection objects.

    Parameters:
        connection_parameters (Kwargs/Dict): 
        A dictionary containing connection parameters 
        including user, password, 
        host, port, and dbname.
    """

    connection_url = '{dbdialect}://{user}:{password}@{host}:{port}/{dbname}'
    engine: Engine = create_engine(connection_url.format(**connection_parameters))
    connection: Connection = engine.connect()

    return (engine, connection)


engine, connection = connect_with_database(user=DB_USER, password=DB_PASS,
                                           host=DB_HOST, port=DB_PORT,
                                           dbname=DB_NAME, dbdialect=DB_DIALECT)

print(f'\nConnected at Database: {DB_DIALECT} / Database Name: {DB_NAME}\n')
