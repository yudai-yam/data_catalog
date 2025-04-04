import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from data_catalog.catalog_builder.config import template_dir


def render_template(template_name: str, context: dict, output_path: Path):
    """
    render the template and write a rst file
    Args:
        template_name: name of the template used for jinja2
        context: variables used in the template
        output_path: location to write the rst file

    """
    environment = Environment(loader=FileSystemLoader(template_dir))

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        template = environment.get_template(template_name)
        with open(output_path, mode="w", encoding="utf-8") as file:
            file.write(template.render(context))
        logging.info(f"Wrote to {output_path}")
    except IOError as e:
        logging.error(f"Could not write to {output_path}: {e}")


def write_table(json_input: dict, output_folder: Path):
    """
    write table rst pages
    Args:
        json_input: json input for a DB
        output_folder: location to write the rst file

    """
    for table_name, table_content in json_input.items():
        # create rst for each table
        filename = f"{table_name}.rst"
        context = {
            "table_name": table_name,
            "description": table_content.get("description"),
            "comments": table_content.get("comments"),
            "author": table_content.get("author"),
            "regression_test_config": table_content.get("regression_test_config"),
            "columns": table_content.get("columns"),
        }
        render_template("table.rst", context, output_folder / filename)


def write_table_list(db: str, json_input: dict, output_folder: Path):
    """
    write a rst page that contains a list of tables
    Args:
        db: name of the input json file which corresponds to the name of DB
        json_input: json input for a DB
        output_folder: location to write the rst file

    """
    file_name = "table_list.rst"

    # create rst for each table
    context = {
        "db_name": db,
        "table_names": json_input.keys(),
        "json_input": json_input,
    }

    render_template(file_name, context, output_folder / file_name)


def write_db_index(db: str, output_folder: Path):
    """
    write an index page for each DB
    Args:
        db : name of the input json file which corresponds to the name of DB
        output_folder: the location to write the rst file

    """
    file_name = "db_index.rst"

    context = {
        "db_name": db,
        "index_description": "this repo is currently under development",
    }

    render_template(file_name, context, output_folder / file_name)


def write_inputs(input_paths: list, output_folder: Path):
    """
    write a rst page that includes the list of available DBs
    Args:
        input_paths: list of paths of inputs
        output_folder: the location to write the rst file

    """
    db_list = [path.stem for path in input_paths]
    file_name = "db_list.rst"

    context = {
        "inputs": db_list,
    }

    render_template(file_name, context, output_folder / file_name)


def write_index(output_folder: Path):
    """
    write an index page
    Args:
        output_folder: the location to write the rst file

    """
    file_name = "index.rst"

    index_description = """
        This page hosts a data catalog of databases.
        This page can be updated through a successful PR to the master branch of data_catalog repository: https://github.com/yudai-yam/data_catalog.
        Refer the ``README.rst`` in the repository for more information.
        Note that this repository is currently under development.
    """

    context = {
        "index_description": index_description,
    }

    render_template(file_name, context, output_folder / file_name)
