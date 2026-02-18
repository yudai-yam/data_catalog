import logging
import os
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import sessionmaker

inputs_folder = Path(__file__).parents[2] / "inputs"

target_columns = {
    "all_col_comments": ["table_name", "column_name", "comments"],
    "all_tab_columns": ["table_name", "column_name", "data_type"],
    "all_tab_comments": ["table_name", "comments"],
}

allowed_table_prefixes = ("RISK", "ERS")


class AppConfiguration(dict):
    """
    A simple dummy dictionary-based configuration class.
    """

    def __init___(self):
        super().__init__()


def read_config() -> AppConfiguration:
    """
    read configurations from env and assign it to a variable

    Returns:
        AppConfiguration
    """

    logging.warning(
        "This read_config function is work in progress."
        "Try using dev command instead of this extract command."
    )

    config = AppConfiguration()

    config["engine"] = create_dummy_engine(
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        service_name=os.getenv("DB_SERVICE_NAME"),
    )

    config["connection"] = config["engine"].connect()

    config["session"] = sessionmaker(config["connection"])()

    # config.add_parameter_from_env("DB_owner", "DB_OWNER", sanitize_schema)

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


def create_dummy_engine(
    username: Optional[str] = "username",
    password: Optional[str] = "password",
    host: Optional[str] = "host",
    port: Optional[str] = "port",
    service_name: Optional[str] = "service_name",
):
    """
    Create a dummy engine for testing purpose

    Args:
        username: username for the db
        password: password for the db
        host: host of the db
        port: port of the db
        service_name: service name of the db
    """
    return "oracle+oracledb://{username}:{password}@{host}:{port}/?service_name={service_name}"
