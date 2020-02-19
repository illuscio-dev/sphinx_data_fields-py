from sphinx.application import Sphinx  # type: ignore
from typing import Any, Dict, List, Tuple, Type, Union
from dataclasses import is_dataclass, fields, Field, MISSING, InitVar


DATA_CLASSES = dict()


class NotFieldError(BaseException):
    pass


def split_name(sphinx_name: str) -> Tuple[str, str]:

    name_split = sphinx_name.split(".")
    class_name = ".".join(name_split[:-1])
    sphinx_name = name_split[-1]

    return class_name, sphinx_name


def resolve_field(
    what: str, name: str, obj: Any
) -> Union[Field, Tuple[Type[InitVar], Any]]:
    if is_dataclass(obj):
        DATA_CLASSES[name] = obj
        raise NotFieldError

    if not what == "attribute":
        raise NotFieldError

    class_name, field_name = split_name(name)

    try:
        data_class = DATA_CLASSES[class_name]
    except KeyError:
        raise NotFieldError

    this_field: Field
    try:
        return next(f for f in fields(data_class) if f.name == field_name)
    except StopIteration:
        raise NotFieldError


def format_dataclass_field(this_field: Field, lines: List[str]) -> None:

    if this_field.init is False:
        lines.append(f"* **field-only**")
        lines.append(f"")

    if this_field.default is not MISSING:
        lines.append(f"* **default:** ``{this_field.default}``")
        lines.append(f"")

    if this_field.default_factory is not MISSING:  # type: ignore
        lines.append(
            f"* **default factory:** "  # type: ignore
            f"``{this_field.default_factory.__module__}"
            f".{this_field.default_factory.__name__}``"
        )
        lines.append(f"")


def process_docstring(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: Dict[str, Any],
    lines: List[str],
) -> None:
    """Processes a field docstring."""

    try:
        result = resolve_field(what, name, obj)
    except NotFieldError:
        return

    if isinstance(result, Field):
        format_dataclass_field(result, lines)
