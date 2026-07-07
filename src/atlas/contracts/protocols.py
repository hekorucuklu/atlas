from collections.abc import Hashable
from typing import Protocol

from atlas.domain.shared import Instrument, OHLCV, Recommendation, Signal


class Analyzer(Protocol):
    def analyze(self, instrument: Instrument, bars: list[OHLCV]) -> Signal:
        ...


class Indicator(Protocol):
    def calculate(self, bars: list[OHLCV]) -> Hashable:
        ...


class MarketDataProvider(Protocol):
    def get_ohlcv(self, instrument: Instrument) -> list[OHLCV]:
        ...


class DecisionEngine(Protocol):
    def recommend(self, signals: list[Signal]) -> Recommendation:
        ...
