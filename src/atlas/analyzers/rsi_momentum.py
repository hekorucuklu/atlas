from decimal import Decimal, InvalidOperation
from typing import Hashable

from atlas.domain.shared import Evidence, Instrument, OHLCV, Signal
from atlas.indicators import IndicatorEngine, IndicatorRegistry, IndicatorResult, RSIIndicator

MOMENTUM_CATEGORY = "momentum"
RSI_NAME = "rsi"
OVERSOLD_THRESHOLD = Decimal("30")
MIDPOINT = Decimal("50")
OVERBOUGHT_THRESHOLD = Decimal("70")


class RSIMomentumAnalyzer:
    def __init__(self, engine: IndicatorEngine | None = None, period: int = 14) -> None:
        self._period = period
        self._engine = engine or self._default_engine(period)

    def analyze(self, instrument: Instrument, bars: list[OHLCV]) -> Signal:
        current = self._engine.run(RSI_NAME, bars)
        previous = self._previous_result(bars)
        evidence = self._evidence(current, previous)

        return Signal(
            instrument=instrument,
            name="rsi_momentum",
            confidence=evidence.confidence,
            evidence=(evidence,),
            metadata={"category": MOMENTUM_CATEGORY, "indicator": RSI_NAME},
        )

    def _previous_result(self, bars: list[OHLCV]) -> IndicatorResult | None:
        if len(bars) <= self._period + 1:
            return None

        return self._engine.run(RSI_NAME, bars[:-1])

    def _evidence(self, current: IndicatorResult, previous: IndicatorResult | None) -> Evidence:
        current_value = self._decimal_value(current.value)
        previous_value = self._decimal_value(previous.value) if previous is not None else None

        if current_value is None:
            return Evidence(
                category=MOMENTUM_CATEGORY,
                title="RSI unavailable",
                confidence=0.0,
                weight=1.0,
                metadata={"indicator": RSI_NAME, "reason": current.metadata.get("reason")},
            )

        title = self._title(current_value, previous_value)
        confidence = self._confidence(title)

        return Evidence(
            category=MOMENTUM_CATEGORY,
            title=title,
            confidence=confidence,
            weight=1.0,
            metadata={"indicator": RSI_NAME, "value": current_value},
        )

    def _title(self, current: Decimal, previous: Decimal | None) -> str:
        if current > OVERBOUGHT_THRESHOLD:
            return "RSI above 70"
        if current < OVERSOLD_THRESHOLD:
            return "RSI below 30"
        if previous is not None and previous <= MIDPOINT < current:
            return "RSI crossed above 50"
        if previous is not None and previous >= MIDPOINT > current:
            return "RSI crossed below 50"
        return "RSI neutral"

    def _confidence(self, title: str) -> float:
        if title in {"RSI above 70", "RSI below 30"}:
            return 0.8
        if title in {"RSI crossed above 50", "RSI crossed below 50"}:
            return 0.6
        return 0.2

    def _decimal_value(self, value: Hashable) -> Decimal | None:
        if value is None:
            return None

        try:
            return Decimal(str(value))
        except InvalidOperation:
            return None

    def _default_engine(self, period: int) -> IndicatorEngine:
        registry = IndicatorRegistry()
        registry.register(RSIIndicator(period=period))
        return IndicatorEngine(registry)
