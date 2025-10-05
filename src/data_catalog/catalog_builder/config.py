import os
from pathlib import Path

# inputs_dir = Path(__file__).parents[3].resolve() / "inputs"

inputs_dir = Path(os.getenv("input_dir", "inputs")).resolve()
rst_dir = Path(__file__).parents[3] / "rst_source"
template_dir = Path(__file__).parents[1] / "templates"

table_list_file = template_dir / "table_list.rst"
db_index_file = template_dir / "db_index.rst"
db_list_file = template_dir / "db_list.rst"
index_file = template_dir / "index.rst"
