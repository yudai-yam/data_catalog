import logging

import pandas as pd
from dotenv import load_dotenv

from db_extract.config import allowed_table_prefixes, inputs_folder, read_config
from db_extract.utils import db_utils, df_utils, json_utils


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
    target_fields = [
        "table_name",
        "author",
        "purpose",
        "description",
        "regression_test_config",
        "usage",
    ]

    try:
        result_column_comments = db_utils.extract_and_query_table(
            "all_col_comments",
            schema,
            config["connection"],
            config["bdwh_owner"],
        )

        result_column_types = db_utils.extract_and_query_table(
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
        # separate dfs based on the prefix of the table name (ex. ERS & DAL)
        columns_df_dict = df_utils.separate(columns_df)

        overviews_df = db_utils.extract_and_query_table(
            "all_tab_comments",
            schema,
            config["connection"],
            config["bdwh_owner"],
        )
        # separate dfs based on the prefix of the table name (ex. ERS & DAL)
        overviews_df_dict = df_utils.separate(overviews_df)

        for prefix in allowed_table_prefixes:

            columns_json_list = df_utils.to_json_list(columns_df_dict[prefix])
            overviews_json_list = json_utils.sanitize_overviews(
                df_utils.to_json_list(overviews_df_dict[prefix]),
                target_fields,
            )

            input_json = json_utils.combine(
                "table_name", overviews_json_list, columns_json_list
            )

            file_path = inputs_folder / (
                str(config["db_name"]) + "_" + prefix + ".json"
            )

            logging.info(f"Writing input json to {file_path}")
            json_utils.write_to_file(file_path, input_json)

    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    extract()
