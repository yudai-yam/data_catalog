import os
from pathlib import Path

from ride_interfaces_services.configuration.app_configuration import AppConfiguration
from ride_interfaces_services.interface.adapters.sqlalchemy_connector.connector import (
    create_engine_for_bdwh,
)
from sqlalchemy.orm import sessionmaker

inputs_folder = Path(__file__).parents[2] / "inputs"

target_columns = {
    "all_col_comments": ["table_name", "column_name", "comments"],
    "all_tab_columns": ["table_name", "column_name", "data_type"],
    "all_tab_comments": ["table_name", "comments"],
}

allowed_table_prefixes = ("RISK", "ERS")


def read_config() -> AppConfiguration:
    """
    read configurations from env and assign it to a variable

    Returns:
        AppConfiguration
    """

    config = AppConfiguration()

    config["engine"] = create_engine_for_bdwh(
        username=os.getenv("BDWH_USER"),
        password=os.getenv("BDWH_PASSWORD"),
        host=os.getenv("BDWH_HOST"),
        port=os.getenv("BDWH_PORT"),
        service_name=os.getenv("BDWH_SERVICE_NAME"),
    )

    config["connection"] = config["engine"].connect()

    config["session"] = sessionmaker(config["connection"])()

    config.add_parameter_from_env("bdwh_owner", "BDWH_OWNER", sanitize_schema)

    config["db_name"] = os.getenv("DB_NAME")

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
