import logging

import pandas as pd

from db_extract.config import allowed_table_prefixes, target_columns
from db_extract.utils import df_utils


def extract_and_query_table(
    table_name: str, schema: str, connection: str, owner: str
) -> pd.DataFrame:
    """
    Generic function to extract a table and query it.

    Args:
        table_name (str): Table name to read.
        schema (str): Schema name.
        connection (dict): DB connection details.
        owner (str): Database owner.

    Returns:
        Processed DataFrame.
    """
    logging.info(f"Extracting data from {table_name} table")

    # sanitize the table name
    table_name = sanitize_table_name(table_name)

    prefix_query = " OR ".join(
        [f"(table_name LIKE '{prefix}%')" for prefix in allowed_table_prefixes]
    )

    query = f"SELECT {', '.join(target_columns[table_name])} FROM {schema}.{table_name} WHERE (owner = '{owner}') AND ({prefix_query})"
    try:
        df = pd.read_sql_query(query, connection)
        logging.info(f"Extracted {len(df)} rows from {table_name}")
        return df_utils.clean(df)
    except Exception as e:
        logging.error(e)
        raise e


def sanitize_table_name(table_name: str) -> str:
    """
    make the table name lower case

    Args:
        table_name: name of the table to sanitize

    Returns:
        name of the table with lower case characters
    """
    return table_name.lower()
