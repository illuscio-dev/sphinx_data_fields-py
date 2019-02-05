import pytest
import copy
from dataclasses import dataclass, field, fields
from typing import List

from sphinx_data_fields._process_docstring import (
    process_docstring,
    DATA_CLASSES,
    InitVar,
)


@dataclass
class X:
    key1: str
    "Key Description"

    key6: InitVar[str]
    "Key Description"

    key2: str = "default"
    "Key Description"

    key3: int = field(default=10)
    "Key Description"

    key4: List[int] = field(default_factory=list)
    "Key Description"

    key5: str = field(init=False)
    "Key Description"

    key7: InitVar[str] = 10
    "Key Description"

    def __post_init__(self, key6: str, key7: str) -> None:
        self.not_a_field = key6
        """field description"""

        self.not_a_field2 = key7
        """field_description"""

    def method(self) -> None:
        pass


FIELDS_DICT = {f.name: f for f in fields(X)}


@pytest.mark.parametrize(
    "field_name, type_string, default_value, default_factory, init, init_only",
    [
        ("key1", ":py:class:`str`", None, None, True, False),
        ("key2", ":py:class:`str`", "default", None, True, False),
        ("key3", ":py:class:`int`", 10, None, True, False),
        ("key4", ":py:class:`~typing.List`\[:py:class:`int`]", None, list, True, False),
        ("key5", ":py:class:`str`", None, None, False, False),
        ("key6", ":py:class:`~dataclasses.InitVar`", None, None, True, True),
        ("key7", ":py:class:`int`", 10, None, True, True),
    ],
)
def test_docstring_process(
    field_name, type_string, default_value, default_factory, init, init_only
):

    process_docstring(None, "class", "module.X", X, {}, [])
    print(DATA_CLASSES)
    print()

    lines = ["Key Description", ""]
    name = f"module.X.{field_name}"

    process_docstring(None, "attribute", name, None, {}, lines)
    print("\n".join(lines))

    assert lines[0] == f"{type_string}: Key Description"
    if default_value is not None:
        assert f"* **default:** ``{default_value}``" in lines
    if default_factory is not None:
        line = (
            f"* **default factory:** "
            f"``{default_factory.__module__}"
            f".{default_factory.__name__}``"
        )
        assert line in lines
    if init is False:
        assert f"* **field-only**" in lines
    if init_only is True:
        assert f"* **init-only**" in lines


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

    process_docstring(None, "class", "module.X", X, {}, [])
    print(DATA_CLASSES)
    print()

    sphinx_name = f"module.X.{sphinx_name}"
    process_docstring(None, sphinx_type, sphinx_name, None, {}, lines)
    print("\n".join(lines))

    assert lines == lines_original
