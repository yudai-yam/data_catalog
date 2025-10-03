import logging
import subprocess

from data_catalog.catalog_builder.main import build


def dev():
    """
    execute the whole pipeline
    """

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("Starting the job")

    build()

    # Define the command
    command = ["sphinx-build", "-E", "-d", ".doctree", "-c", ".", "rst_source", "docs"]

    # Run the command
    subprocess.run(command, check=True)

    logging.info("Finishing the job")


if __name__ == "__main__":
    dev()
