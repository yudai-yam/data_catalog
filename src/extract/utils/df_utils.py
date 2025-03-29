import json

import pandas as pd


def query(df: pd.DataFrame, target_owner: str, target_columns: list) -> pd.DataFrame:
    """
    extract the target data from the dataframe
    Args:
        df: dataframe containing the table data extracted from the BDWH database
        target_owner: owner of the target table
        target_columns: list of columns to extract from the target table

    Returns:
        target table data
    """
    return df.loc[
        df.owner == target_owner,
        target_columns,
    ]


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
    """
    replace the \n into a space

    Returns:
    cleaned dataframe
    """
    return df.replace(r"\n", " ", regex=True)
