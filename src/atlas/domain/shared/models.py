from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from types import MappingProxyType
from typing import Literal, Mapping, TypeAlias

Metadata: TypeAlias = Mapping[str, object]
RecommendationAction: TypeAlias = Literal["BUY", "SELL", "HOLD"]


def _freeze_metadata(metadata: Metadata) -> Metadata:
    return MappingProxyType(dict(metadata))


@dataclass(frozen=True, slots=True)
class Instrument:
    symbol: str
    name: str | None = None
    exchange: str | None = None
    asset_class: str | None = None
    currency: str | None = None
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class OHLCV:
    instrument: Instrument
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Evidence:
    category: str
    title: str
    confidence: float
    weight: float
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Signal:
    instrument: Instrument
    name: str
    confidence: float
    evidence: tuple[Evidence, ...] = ()
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Recommendation:
    instrument: Instrument
    action: RecommendationAction
    confidence: float
    evidence: tuple[Evidence, ...]
    metadata: Metadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
