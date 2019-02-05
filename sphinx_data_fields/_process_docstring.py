from sphinx.application import Sphinx  # type: ignore
from sphinx_autodoc_typehints import format_annotation
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

    try:
        return resolve_init_var(field_name, data_class)
    except NotFieldError:
        pass

    this_field: Field
    try:
        return next(f for f in fields(data_class) if f.name == field_name)
    except StopIteration:
        raise NotFieldError


def resolve_init_var(
    field_name: str, data_class: Type[Any]
) -> Tuple[Type[InitVar], Any]:

    try:
        annotation = data_class.__annotations__[field_name]
    except KeyError:
        raise NotFieldError

    if not isinstance(annotation, type) or not issubclass(annotation, InitVar):
        raise NotFieldError

    default = getattr(data_class, field_name, MISSING)

    return annotation, default


def format_dataclass_field(this_field: Field, lines: List[str]) -> None:

    lines[0] = f"{format_annotation(this_field.type)}: {lines[0]}"

    if this_field.init is False:
        lines.append(f"* **field-only**")
        lines.append(f"")

    if this_field.default is not MISSING:
        lines.append(f"* **default:** ``{this_field.default}``")
        lines.append(f"")

    if this_field.default_factory is not MISSING:  # type: ignore
        lines.append(
            f"* **default factory:** "
            f"``{this_field.default_factory.__module__}"
            f".{this_field.default_factory.__name__}``"
        )
        lines.append(f"")


def format_init_var(annotation: Type[InitVar], default: Any, lines: List[str]) -> None:

    lines.append(f"* **init-only**")
    lines.append(f"")

    if default is not MISSING:
        lines.append(f"* **default:** ``{default}``")
        lines.append(f"")
        field_type = type(default)
    else:
        field_type = annotation

    lines[0] = f"{format_annotation(field_type)}: {lines[0]}"


def process_docstring(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: Dict[str, Any],
    lines: List[str],
) -> None:

    try:
        result = resolve_field(what, name, obj)
    except NotFieldError:
        return

    if isinstance(result, Field):
        format_dataclass_field(result, lines)
    else:
        format_init_var(result[0], result[1], lines)
