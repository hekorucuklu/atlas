from collections.abc import Iterable, Mapping
from datetime import date, datetime, time
from decimal import Decimal
from importlib import import_module
from typing import Any

from atlas.domain.shared import Instrument, OHLCV

DEFAULT_TIMEFRAME = "1d"
DEFAULT_BARS = 500


class OpenBBMarketDataProvider:
    def __init__(self, client: Any | None = None) -> None:
        self._client = client

    def get_ohlcv(self, instrument: Instrument) -> list[OHLCV]:
        return self.history(instrument, DEFAULT_TIMEFRAME, DEFAULT_BARS)

    def history(self, instrument: Instrument, timeframe: str, bars: int) -> list[OHLCV]:
        response = self._historical_price(instrument, timeframe, bars)
        return [self._to_ohlcv(instrument, row, timeframe) for row in self._iter_rows(response)]

    @property
    def client(self) -> Any:
        if self._client is None:
            self._client = import_module("openbb").obb
        return self._client

    def _historical_price(self, instrument: Instrument, timeframe: str, bars: int) -> Any:
        return self.client.equity.price.historical(
            symbol=instrument.symbol,
            interval=timeframe,
            limit=bars,
        )

    def _iter_rows(self, response: Any) -> Iterable[Any]:
        if hasattr(response, "to_df"):
            return response.to_df().to_dict("records")

        results = getattr(response, "results", response)
        if hasattr(results, "to_dict"):
            return results.to_dict("records")

        return results

    def _to_ohlcv(self, instrument: Instrument, row: Any, timeframe: str) -> OHLCV:
        return OHLCV(
            instrument=instrument,
            timestamp=self._timestamp(row),
            open=self._decimal(row, "open"),
            high=self._decimal(row, "high"),
            low=self._decimal(row, "low"),
            close=self._decimal(row, "close"),
            volume=self._decimal(row, "volume"),
            metadata={"provider": "openbb", "timeframe": timeframe},
        )

    def _timestamp(self, row: Any) -> datetime:
        value = self._value(row, "timestamp", "datetime", "date")
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, time.min)
        if isinstance(value, str):
            return datetime.fromisoformat(value)

        raise TypeError("OpenBB row does not contain a supported timestamp value.")

    def _decimal(self, row: Any, key: str) -> Decimal:
        value = self._value(row, key)
        return Decimal(str(value))

    def _value(self, row: Any, *keys: str) -> Any:
        for key in keys:
            if isinstance(row, Mapping) and key in row:
                return row[key]
            if hasattr(row, key):
                return getattr(row, key)

        joined_keys = ", ".join(keys)
        raise KeyError(f"OpenBB row is missing required field: {joined_keys}")
