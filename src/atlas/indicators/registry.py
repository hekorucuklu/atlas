from atlas.indicators.base import Indicator


class IndicatorRegistry:
    def __init__(self) -> None:
        self._indicators: dict[str, Indicator] = {}

    def register(self, indicator: Indicator) -> None:
        self._indicators[indicator.name] = indicator

    def resolve(self, name: str) -> Indicator:
        return self._indicators[name]
