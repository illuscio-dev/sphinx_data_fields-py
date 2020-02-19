from dataclasses import dataclass, InitVar, field
from typing import List


@dataclass
class ExampleDataclass:
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
        """Method description."""
        pass
