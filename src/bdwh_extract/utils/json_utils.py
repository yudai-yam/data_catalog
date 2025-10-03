import json
import logging
from collections import OrderedDict
from pathlib import Path


def combine(key: str, overviews: list, columns: list) -> OrderedDict:
    """
    Combine overviews and columns into a single json
    Args:
        key: key, normally table name
        overviews: list of overviews json
        columns: list of columns json

    Returns:
        combined json
    """

    tables = OrderedDict()

    # table comments
    for overview in overviews:
        table = overview[key]
        if table not in tables:
            del overview[key]
            # fix the order
            tables[table] = OrderedDict(
                [
                    ("author", overview.get("author")),
                    ("description", overview.get("description")),
                    ("comments", overview.get("comments")),
                    ("regression_test_config", overview.get("regression_test_config")),
                    ("columns", []),
                ]
            )
        else:
            logging.error(f"Duplicate table comment for '{table}' — ignoring")

    # column comments
    for column in columns:
        table = column[key]
        if table not in tables:
            # fix the order
            tables[table] = OrderedDict(
                [
                    ("author", None),
                    ("description", None),
                    ("comments", None),
                    ("regression test config", None),
                    ("columns", []),
                ]
            )
        del column[key]
        tables[table]["columns"].append(column)

    return tables


def write_to_file(file_path: Path, content: OrderedDict):
    """
    write content to file
    Args:
        file_path: path to file
        content: content to write in the file
    """
    try:
        with open(file_path, "w") as file:
            json.dump(content, file, indent=2)
    except (OSError, IOError) as e:
        print(f"Failed to write to {file_path}: {e}")
    except TypeError as e:
        print(f"Invalid content type. Expected a dictionary: {e}")


def rename_keys(key_map: dict, original_dict: dict) -> dict:
    """
    rename the keys in the original dict
    Args:
        key_map: key map
        original_dict: original dict to rename its keys
    Returns:
        renamed dict
    """

    renamed_dict = {}
    for key, value in original_dict.items():
        key = key.lower()
        key = key_map.get(key, key)
        renamed_dict[key] = value

    return renamed_dict


def sanitize_overviews(overviews_json_list: list, target_fields: list) -> list:
    """
    Sanitize overviews, ensuring field order and normalizing keys.
    Fields in target_fields are assigned their own keys, others go into "other_fields".
    Args:
        overviews_json_list: list of overviews json
        target_fields: list of fields that obtain their own key

    Returns:
        sanitized overviews json list with guaranteed field order
    """
    sanitized_overviews = []
    key_map = {
        "purpose": "description",
        "usage": "comments",
        "key": "comparison_key",
        "columns-no-compare": "columns_to_ignore",
        "where": "where_query",
    }

    for overview_json in overviews_json_list:
        if overview_json["comments"] is None:
            sanitized_overviews.append(OrderedDict(overview_json))
            continue

        comments = json.loads(overview_json["comments"], strict=False)
        reshaped = rename_keys(key_map, comments)

        # change the keys of regression testing config
        if "regression_test_config" in reshaped.keys():
            reshaped["regression_test_config"] = rename_keys(
                key_map, reshaped["regression_test_config"]
            )

        # Construct final ordered overview
        sanitized_overview = OrderedDict()
        sanitized_overview["table_name"] = overview_json["table_name"]

        for _, value in key_map.items():
            if value in reshaped:
                sanitized_overview[value] = reshaped.pop(value)

        # Other target fields in order
        for field in target_fields:
            if field in reshaped:
                sanitized_overview[field] = reshaped.pop(field)

        sanitized_overviews.append(sanitized_overview)

    return sanitized_overviews
