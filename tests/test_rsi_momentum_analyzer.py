from datetime import UTC, datetime, timedelta
from decimal import Decimal

from atlas.analyzers import RSIMomentumAnalyzer
from atlas.domain.shared import Instrument, OHLCV, Signal
from atlas.indicators import IndicatorResult


class FakeIndicatorEngine:
    def __init__(self, results: list[IndicatorResult]) -> None:
        self.results = results
        self.calls: list[tuple[str, list[OHLCV]]] = []

    def run(self, name: str, bars: list[OHLCV]) -> IndicatorResult:
        self.calls.append((name, bars))
        return self.results.pop(0)


def make_bars(count: int) -> list[OHLCV]:
    instrument = Instrument(symbol="AAPL")
    start = datetime(2026, 1, 1, tzinfo=UTC)

    return [
        OHLCV(
            instrument=instrument,
            timestamp=start + timedelta(days=index),
            open=Decimal("100"),
            high=Decimal("100"),
            low=Decimal("100"),
            close=Decimal("100"),
            volume=Decimal("1000"),
        )
        for index in range(count)
    ]


def test_analyzer_returns_oversold_signal() -> None:
    engine = FakeIndicatorEngine([IndicatorResult(name="rsi", value=Decimal("25"))])
    analyzer = RSIMomentumAnalyzer(engine=engine)
    instrument = Instrument(symbol="AAPL")

    signal = analyzer.analyze(instrument, make_bars(10))

    assert isinstance(signal, Signal)
    assert signal.instrument == instrument
    assert signal.name == "rsi_momentum"
    assert signal.confidence == 0.8
    assert signal.metadata["category"] == "momentum"
    assert len(signal.evidence) == 1
    assert signal.evidence[0].category == "momentum"
    assert signal.evidence[0].title == "RSI below 30"
    assert not hasattr(signal, "action")


def test_analyzer_returns_overbought_signal() -> None:
    engine = FakeIndicatorEngine([IndicatorResult(name="rsi", value=Decimal("75"))])
    analyzer = RSIMomentumAnalyzer(engine=engine)

    signal = analyzer.analyze(Instrument(symbol="AAPL"), make_bars(10))

    assert signal.confidence == 0.8
    assert signal.evidence[0].title == "RSI above 70"


def test_analyzer_returns_neutral_signal() -> None:
    engine = FakeIndicatorEngine([IndicatorResult(name="rsi", value=Decimal("52"))])
    analyzer = RSIMomentumAnalyzer(engine=engine)

    signal = analyzer.analyze(Instrument(symbol="AAPL"), make_bars(10))

    assert signal.confidence == 0.2
    assert signal.evidence[0].title == "RSI neutral"


def test_analyzer_handles_insufficient_data() -> None:
    engine = FakeIndicatorEngine(
        [
            IndicatorResult(
                name="rsi",
                value=None,
                metadata={"reason": "insufficient_bars"},
            )
        ]
    )
    analyzer = RSIMomentumAnalyzer(engine=engine)

    signal = analyzer.analyze(Instrument(symbol="AAPL"), make_bars(3))

    assert signal.confidence == 0.0
    assert signal.evidence[0].title == "RSI unavailable"
    assert signal.evidence[0].metadata["reason"] == "insufficient_bars"
    assert len(signal.evidence) == 1


def test_analyzer_uses_indicator_engine() -> None:
    bars = make_bars(10)
    engine = FakeIndicatorEngine([IndicatorResult(name="rsi", value=Decimal("52"))])
    analyzer = RSIMomentumAnalyzer(engine=engine)

    analyzer.analyze(Instrument(symbol="AAPL"), bars)

    assert engine.calls == [("rsi", bars)]
