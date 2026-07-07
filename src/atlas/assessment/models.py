from dataclasses import dataclass

from atlas.domain.shared import Evidence, Signal


@dataclass(frozen=True, slots=True)
class Assessment:
    summary: str
    confidence: float
    signals: tuple[Signal, ...]
    evidence: tuple[Evidence, ...]
