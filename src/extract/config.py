import os
from pathlib import Path


inputs_folder = Path(__file__).parents[2] / "inputs"

target_columns = {
    "all_col_comments": ["table_name", "column_name", "comments"],
    "all_tab_columns": ["table_name", "column_name", "data_type"],
    "all_tab_comments": ["table_name", "comments"],
}


def read_config() -> AppConfiguration:
    """
    read configurations from env and assign it to a variable

    Returns:
        AppConfiguration
    """

    config = AppConfiguration()

    config["engine"] = create_engine_for_bdwh(
        username=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        service_name=os.getenv("SERVICE_NAME"),
    )

    config["connection"] = config["engine"].connect()

    config["session"] = sessionmaker(config["connection"])()

    config.add_parameter_from_env("owner", "OWNER", sanitize_schema)

    config["db_name"] = os.getenv("DB_NAME")
    config["target_fields"] = os.getenv("TARGET_FIELDS")
    config["target_tables"] = os.getenv("TARGET_TABLES")

    return config


def sanitize_schema(value: str) -> str:
    """
    Return uppercase value

    Args:
        value: the value to turn into upper case

    Returns:
        the upper case value
    """
    # lowercase schema leads to no results in the queries in regression_config.py
    return value.upper()
