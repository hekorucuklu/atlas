from decimal import Decimal

from atlas.domain.shared import OHLCV
from atlas.indicators.result import IndicatorResult

RSI_NAME = "rsi"
RSI_MIN = Decimal("0")
RSI_MIDPOINT = Decimal("50")
RSI_MAX = Decimal("100")


class RSIIndicator:
    name = RSI_NAME

    def __init__(self, period: int = 14) -> None:
        if period <= 0:
            raise ValueError("RSI period must be greater than 0.")

        self.period = period

    def calculate(self, bars: list[OHLCV]) -> IndicatorResult:
        if len(bars) <= self.period:
            return IndicatorResult(
                name=self.name,
                value=None,
                metadata={"period": self.period, "reason": "insufficient_bars"},
            )

        changes = self._changes(bars)
        average_gain, average_loss = self._initial_averages(changes[: self.period])

        for change in changes[self.period :]:
            gain, loss = self._gain_loss(change)
            average_gain = ((average_gain * (self.period - 1)) + gain) / self.period
            average_loss = ((average_loss * (self.period - 1)) + loss) / self.period

        return IndicatorResult(
            name=self.name,
            value=self._rsi(average_gain, average_loss),
            metadata={"period": self.period},
        )

    def _changes(self, bars: list[OHLCV]) -> list[Decimal]:
        return [current.close - previous.close for previous, current in zip(bars, bars[1:])]

    def _initial_averages(self, changes: list[Decimal]) -> tuple[Decimal, Decimal]:
        gains: list[Decimal] = []
        losses: list[Decimal] = []

        for change in changes:
            gain, loss = self._gain_loss(change)
            gains.append(gain)
            losses.append(loss)

        return sum(gains, Decimal("0")) / self.period, sum(losses, Decimal("0")) / self.period

    def _gain_loss(self, change: Decimal) -> tuple[Decimal, Decimal]:
        if change > 0:
            return change, Decimal("0")
        if change < 0:
            return Decimal("0"), abs(change)
        return Decimal("0"), Decimal("0")

    def _rsi(self, average_gain: Decimal, average_loss: Decimal) -> Decimal:
        if average_gain == 0 and average_loss == 0:
            return RSI_MIDPOINT
        if average_loss == 0:
            return RSI_MAX
        if average_gain == 0:
            return RSI_MIN

        relative_strength = average_gain / average_loss
        return RSI_MAX - (RSI_MAX / (Decimal("1") + relative_strength))
