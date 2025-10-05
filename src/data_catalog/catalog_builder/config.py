import os
from pathlib import Path

inputs_dir = Path(os.getenv("input_dir", "inputs")).resolve()
rst_dir = Path(os.getenv("rst_dir", "rst_source")).resolve()
template_dir = Path(__file__).parents[1] / "templates"

table_list_file = template_dir / "table_list.rst"
db_index_file = template_dir / "db_index.rst"
db_list_file = template_dir / "db_list.rst"
index_file = template_dir / "index.rst"
