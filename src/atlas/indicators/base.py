from typing import Protocol

from atlas.domain.shared import OHLCV
from atlas.indicators.result import IndicatorResult


class Indicator(Protocol):
    name: str

    def calculate(self, bars: list[OHLCV]) -> IndicatorResult:
        ...
