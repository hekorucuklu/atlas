from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from atlas.contracts import MarketDataProvider
from atlas.domain.shared import Instrument, OHLCV
from atlas.providers import OpenBBMarketDataProvider


@dataclass(frozen=True, slots=True)
class FakeOpenBBResponse:
    results: list[dict[str, Any]]


class FakeHistoricalPriceEndpoint:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self.calls: list[dict[str, Any]] = []

    def historical(self, *, symbol: str, interval: str, limit: int) -> FakeOpenBBResponse:
        self.calls.append({"symbol": symbol, "interval": interval, "limit": limit})
        return FakeOpenBBResponse(results=self.rows)


class FakeEquityClient:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.price = FakeHistoricalPriceEndpoint(rows)


class FakeOpenBBClient:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.equity = FakeEquityClient(rows)


ROW = {
    "date": "2026-01-02",
    "open": "100.10",
    "high": "105.20",
    "low": "99.90",
    "close": "104.30",
    "volume": "12345",
}


def test_openbb_provider_can_be_used_as_market_data_provider() -> None:
    provider: MarketDataProvider = OpenBBMarketDataProvider(client=FakeOpenBBClient([ROW]))

    bars = provider.get_ohlcv(Instrument(symbol="AAPL"))

    assert len(bars) == 1
    assert isinstance(bars[0], OHLCV)


def test_history_returns_domain_ohlcv_objects() -> None:
    client = FakeOpenBBClient([ROW])
    provider = OpenBBMarketDataProvider(client=client)
    instrument = Instrument(symbol="AAPL", exchange="NASDAQ")

    bars = provider.history(instrument=instrument, timeframe="1d", bars=1)

    assert bars == [
        OHLCV(
            instrument=instrument,
            timestamp=datetime(2026, 1, 2),
            open=Decimal("100.10"),
            high=Decimal("105.20"),
            low=Decimal("99.90"),
            close=Decimal("104.30"),
            volume=Decimal("12345"),
            metadata={"provider": "openbb", "timeframe": "1d"},
        )
    ]


def test_history_passes_request_to_openbb_client() -> None:
    client = FakeOpenBBClient([ROW])
    provider = OpenBBMarketDataProvider(client=client)

    provider.history(Instrument(symbol="MSFT"), timeframe="1h", bars=20)

    assert client.equity.price.calls == [
        {"symbol": "MSFT", "interval": "1h", "limit": 20},
    ]
