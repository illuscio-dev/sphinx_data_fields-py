import pytest
import copy
from dataclasses import fields


from sphinx_data_fields._process_docstring import (
    process_docstring,
    DATA_CLASSES,
)
from sphinx_data_fields._example_object import ExampleDataclass


FIELDS_DICT = {f.name: f for f in fields(ExampleDataclass)}


@pytest.mark.parametrize(
    "field_name, default_value, default_factory, init, init_only",
    [
        ("key1", None, None, True, False),
        ("key2", "default", None, True, False),
        ("key3", 10, None, True, False),
        ("key4", None, list, True, False),
        ("key5", None, None, False, False),
        ("key6", None, None, True, True),
        ("key7", 10, None, True, True),
    ],
)
def test_docstring_process(field_name, default_value, default_factory, init, init_only):

    process_docstring(None, "class", "module.X", ExampleDataclass, {}, [])
    print(DATA_CLASSES)
    print()

    lines = ["Key Description", ""]
    name = f"module.X.{field_name}"

    process_docstring(None, "attribute", name, None, {}, lines)
    print("\n".join(lines))

    print("KEY:", field_name)
    print("TYPE STRING RECEIVED:", lines[0])

    assert lines[0] == f"Key Description"
    if default_value is not None and not init_only:
        assert f"* **default:** ``{default_value}``" in lines
    if default_factory is not None and not init_only:
        line = (
            f"* **default factory:** "
            f"``{default_factory.__module__}"
            f".{default_factory.__name__}``"
        )
        assert line in lines
    if init is False:
        assert f"* **field-only**" in lines


@pytest.mark.parametrize(
    "sphinx_name, sphinx_type",
    [
        ("not_a_field1", "attribute"),
        ("not_a_field2", "attribute"),
        ("method", "method"),
        ("not_a_anything", "attribute"),
        ("Y.not_a_anything", "attribute"),
    ],
)
def test_non_fields(sphinx_name, sphinx_type):

    lines = ["what a description!", ""]
    lines_original = copy.copy(lines)

    process_docstring(None, "class", "module.X", ExampleDataclass, {}, [])
    print(DATA_CLASSES)
    print()

    sphinx_name = f"module.X.{sphinx_name}"
    process_docstring(None, sphinx_type, sphinx_name, None, {}, lines)
    print("\n".join(lines))

    assert lines == lines_original
