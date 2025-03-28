import logging

import pandas as pd


def sanitize_table_name(table_name: str) -> str:
    """
    make the table name lower case

    Args:
        table_name: name of the table to sanitize

    Returns:
        name of the table with lower case characters
    """
    return table_name.lower()


def read_table(table_name: str, schema: str, connection) -> pd.DataFrame:
    """
    read a table from BDWH database

    Args:
        table_name: name of the table to read
        schema: schema in the database
        connection: connection to BDWH database

    Returns:
        dataframe containing the table read from the database
    """

    # saniztize the table name
    table_name = sanitize_table_name(table_name)

    try:
        df = pd.read_sql_table(table_name, connection, schema=schema)
        return df
    except Exception as e:
        logging.error(e)
