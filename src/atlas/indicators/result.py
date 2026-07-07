from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Hashable, Mapping, TypeAlias

IndicatorMetadata: TypeAlias = Mapping[str, object]


def _freeze_metadata(metadata: IndicatorMetadata) -> IndicatorMetadata:
    return MappingProxyType(dict(metadata))


@dataclass(frozen=True, slots=True)
class IndicatorResult:
    name: str
    value: Hashable
    metadata: IndicatorMetadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
