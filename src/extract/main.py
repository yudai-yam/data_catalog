import json
import logging

import pandas as pd
from dotenv import load_dotenv

from extract.config import inputs_folder, read_config, target_columns
from extract.utils import db_utils, df_utils, json_utils


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

    df = db_utils.read_table(table_name, schema, connection)
    result_df = df_utils.query(df, owner, target_columns.get(table_name, []))

    logging.info(f"Extracted {len(result_df)} rows from {table_name}")
    return df_utils.clean(result_df)


def load_configuration():
    """
    load the configuration from environment variables.
    """
    load_dotenv()
    return read_config()


def extract():
    """
    extract data from BDWH tables
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # load DB parameters from .env file
    config = load_configuration()
    schema = "SYS"

    try:
        result_column_comments = extract_and_query_table(
            "all_col_comments",
            schema,
            config["connection"],
            config["bdwh_owner"],
        )

        result_column_types = extract_and_query_table(
            "all_tab_columns",
            schema,
            config["connection"],
            config["bdwh_owner"],
        )

        columns_df = pd.merge(
            result_column_comments,
            result_column_types,
            on=["table_name", "column_name"],
            how="outer",
        )
        columns_json_list = df_utils.to_json_list(columns_df)

        overviews_df = extract_and_query_table(
            "all_tab_comments",
            schema,
            config["connection"],
            config["bdwh_owner"],
        )
        overviews_json_list = json_utils.sanitize_overviews(
            df_utils.to_json_list(overviews_df), json.loads(config["target_fields"])
        )

        input_json = json_utils.combine(
            "table_name", overviews_json_list, columns_json_list
        )

        file_path = inputs_folder / (str(config["db_name"]) + ".json")

        logging.info(f"Writing input json to {file_path}")
        json_utils.write_to_file(file_path, input_json)

    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    extract()
