import json

import pandas as pd

from bdwh_extract.config import allowed_table_prefixes


def separate(df: pd.DataFrame) -> dict:
    """
    separate a df based on the prefix of the table
    ex. BDWH_RISK and BDWH_ERS

    Args:
        df: original dataframe for a whole db

    Returns:
        a dictionary with prefix as a key and
        df that has a corresponding table name as a value
    """

    return {
        prefix: df[df.table_name.str.startswith(prefix)]
        for prefix in allowed_table_prefixes
    }


def to_json_list(df: pd.DataFrame) -> list:
    """
    make dataframe into a list of json

    Args:
        df: dataframe to be converted

    Returns:
        list of json strings
    """
    return json.loads(df.to_json(orient="records"))


def clean(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace(r"\n", " ", regex=True)
