from collections.abc import Hashable
from inspect import signature
from typing import get_type_hints

from atlas.contracts import Analyzer, DecisionEngine, Indicator, MarketDataProvider
from atlas.domain.shared import Instrument, OHLCV, Recommendation, Signal


def test_contracts_import_from_public_package() -> None:
    assert Analyzer.__name__ == "Analyzer"
    assert Indicator.__name__ == "Indicator"
    assert MarketDataProvider.__name__ == "MarketDataProvider"
    assert DecisionEngine.__name__ == "DecisionEngine"


def test_analyzer_contract_signature() -> None:
    method = Analyzer.analyze

    assert list(signature(method).parameters) == ["self", "instrument", "bars"]
    assert get_type_hints(method) == {
        "instrument": Instrument,
        "bars": list[OHLCV],
        "return": Signal,
    }


def test_indicator_contract_signature() -> None:
    method = Indicator.calculate

    assert list(signature(method).parameters) == ["self", "bars"]
    assert get_type_hints(method) == {
        "bars": list[OHLCV],
        "return": Hashable,
    }


def test_market_data_provider_contract_signature() -> None:
    method = MarketDataProvider.get_ohlcv

    assert list(signature(method).parameters) == ["self", "instrument"]
    assert get_type_hints(method) == {
        "instrument": Instrument,
        "return": list[OHLCV],
    }


def test_decision_engine_contract_signature() -> None:
    method = DecisionEngine.recommend

    assert list(signature(method).parameters) == ["self", "signals"]
    assert get_type_hints(method) == {
        "signals": list[Signal],
        "return": Recommendation,
    }
