from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from atlas.domain.shared import Instrument, OHLCV
from atlas.indicators import Indicator, IndicatorResult, RSIIndicator


def make_bars(closes: list[str]) -> list[OHLCV]:
    instrument = Instrument(symbol="AAPL")
    start = datetime(2026, 1, 1, tzinfo=UTC)

    return [
        OHLCV(
            instrument=instrument,
            timestamp=start + timedelta(days=index),
            open=Decimal(close),
            high=Decimal(close),
            low=Decimal(close),
            close=Decimal(close),
            volume=Decimal("1000"),
        )
        for index, close in enumerate(closes)
    ]


def test_rsi_indicator_uses_indicator_protocol() -> None:
    indicator: Indicator = RSIIndicator(period=3)

    assert indicator.name == "rsi"


def test_rsi_for_rising_market() -> None:
    result = RSIIndicator(period=3).calculate(make_bars(["1", "2", "3", "4", "5"]))

    assert result == IndicatorResult(name="rsi", value=Decimal("100"), metadata={"period": 3})


def test_rsi_for_falling_market() -> None:
    result = RSIIndicator(period=3).calculate(make_bars(["5", "4", "3", "2", "1"]))

    assert result == IndicatorResult(name="rsi", value=Decimal("0"), metadata={"period": 3})


def test_rsi_for_flat_market() -> None:
    result = RSIIndicator(period=3).calculate(make_bars(["5", "5", "5", "5", "5"]))

    assert result == IndicatorResult(name="rsi", value=Decimal("50"), metadata={"period": 3})


def test_rsi_handles_insufficient_bars_gracefully() -> None:
    result = RSIIndicator(period=3).calculate(make_bars(["1", "2", "3"]))

    assert result == IndicatorResult(
        name="rsi",
        value=None,
        metadata={"period": 3, "reason": "insufficient_bars"},
    )


def test_rsi_rejects_invalid_period() -> None:
    with pytest.raises(ValueError, match="period must be greater than 0"):
        RSIIndicator(period=0)
