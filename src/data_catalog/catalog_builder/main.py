import logging

from data_catalog.catalog_builder.config import inputs_dir, rst_dir
from data_catalog.catalog_builder.utils import load_json
from data_catalog.catalog_builder.write_rst import (
    write_db_index,
    write_index,
    write_inputs,
    write_table,
    write_table_list,
)


def build():
    """
    execute process for building the whole rst files from the json input
    """

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("Building RST files")

    input_paths = list(inputs_dir.rglob("*"))

    write_inputs(input_paths, rst_dir)
    write_index(rst_dir)

    logging.info(f"Input directory: {inputs_dir}")

    # iterate through inputs, each db
    for input_path in input_paths:

        logging.info(f"Building {input_path}")
        json_input = load_json(input_path)

        if json_input is None:
            break

        db = input_path.stem
        db_dir = rst_dir / db

        write_table(json_input, db_dir / "tables")
        write_table_list(db, json_input, db_dir)
        write_db_index(db, db_dir)


if __name__ == "__main__":
    build()
