from atlas.domain.shared import OHLCV
from atlas.indicators.registry import IndicatorRegistry
from atlas.indicators.result import IndicatorResult


class IndicatorEngine:
    def __init__(self, registry: IndicatorRegistry) -> None:
        self._registry = registry

    def run(self, name: str, bars: list[OHLCV]) -> IndicatorResult:
        indicator = self._registry.resolve(name)
        return indicator.calculate(bars)
