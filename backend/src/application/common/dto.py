from dataclasses import dataclass, Field
from typing import get_type_hints, Optional, Type
import typing

from src.domain.models import GameSession

_FIELDS = "__dataclass_fields__"


def _construct_init(annotations: dict[str, Field]) -> typing.Callable:
    body = []
    for field in annotations.values():
        body.append(f"  setattr(self, '{field.name}', None)")
    txt = "\n".join(body)
    param_annotations = ",".join(
        (
            f"{annotation.name}: {annotation.type} = {annotation.default}"
            for annotation in annotations.values()
        )
    )
    txt = f"def __create_fn__():\n def __init__(self, {param_annotations}) -> None:\n{txt}\n return __init__"
    ns = {}
    exec(txt, globals(), ns)
    return ns["__create_fn__"]()


def optional(cls: Type):
    # make all fields optional
    assert hasattr(cls, _FIELDS), "Only dataclass can be decorated with @optional()"
    fields: dict[str, Field] = getattr(cls, _FIELDS)
    type_hints = get_type_hints(cls)
    for field, annotation in fields.items():
        annotation.type = Optional[annotation.type]
        annotation.default = None
        type_hints[field] = annotation.type

    new_init = _construct_init(fields)
    new_init.__annotations__ = type_hints
    cls.__init__ = new_init
    cls.__annotations__ = type_hints
    return cls


@optional
@dataclass
class UpdateGameSession(GameSession):
    pass
