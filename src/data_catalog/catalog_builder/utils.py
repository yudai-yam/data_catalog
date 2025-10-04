import json
import logging
from pathlib import Path


def load_json(input_file: Path) -> dict:
    """
    load json file
    Args:
        input_file: path to json file

    Returns:
        content of json file
    """
    try:
        with input_file.open("r") as f:
            data = json.load(f)
            return data

    except FileNotFoundError as e:
        logging.error(f"File {input} not found.")
        raise e
    except json.decoder.JSONDecodeError as e:
        logging.error(f"File {input} could not be decoded.")
        raise e
