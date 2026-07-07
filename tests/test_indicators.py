from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from atlas.domain.shared import Instrument, OHLCV
from atlas.indicators import Indicator, IndicatorEngine, IndicatorRegistry, IndicatorResult


class FakeIndicator:
    name = "fake"

    def __init__(self) -> None:
        self.calls: list[list[OHLCV]] = []

    def calculate(self, bars: list[OHLCV]) -> IndicatorResult:
        self.calls.append(bars)
        return IndicatorResult(name=self.name, value="ok", metadata={"bars": len(bars)})


def make_bars() -> list[OHLCV]:
    instrument = Instrument(symbol="AAPL")
    return [
        OHLCV(
            instrument=instrument,
            timestamp=datetime(2026, 1, 2, tzinfo=UTC),
            open=Decimal("100"),
            high=Decimal("101"),
            low=Decimal("99"),
            close=Decimal("100.50"),
            volume=Decimal("1000"),
        )
    ]


def test_register_indicator() -> None:
    registry = IndicatorRegistry()
    indicator = FakeIndicator()

    registry.register(indicator)

    assert registry.resolve("fake") is indicator


def test_resolve_indicator() -> None:
    registry = IndicatorRegistry()
    indicator: Indicator = FakeIndicator()

    registry.register(indicator)

    assert registry.resolve("fake") is indicator


def test_execute_indicator_through_engine() -> None:
    registry = IndicatorRegistry()
    indicator = FakeIndicator()
    bars = make_bars()
    registry.register(indicator)
    engine = IndicatorEngine(registry)

    result = engine.run("fake", bars)

    assert result == IndicatorResult(name="fake", value="ok", metadata={"bars": 1})
    assert indicator.calls == [bars]


def test_indicator_result_is_immutable() -> None:
    result = IndicatorResult(name="fake", value="ok", metadata={"source": "test"})

    with pytest.raises(FrozenInstanceError):
        result.name = "changed"  # type: ignore[misc]

    with pytest.raises(TypeError):
        result.metadata["source"] = "changed"  # type: ignore[index]
