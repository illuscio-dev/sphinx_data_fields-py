from sphinx.application import Sphinx
from ._process_docstring import process_docstring


def setup(app: Sphinx) -> dict:
    app.add_config_value("set_dataclass_fields", False, "html")
    app.connect("autodoc-process-docstring", process_docstring)
    return dict(parallel_read_safe=True)
