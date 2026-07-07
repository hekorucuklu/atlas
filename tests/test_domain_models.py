from dataclasses import FrozenInstanceError, fields, is_dataclass
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from atlas.domain.shared import Evidence, Instrument, OHLCV, Recommendation, Signal


def test_instrument_is_frozen_dataclass() -> None:
    instrument = Instrument(symbol="AAPL", exchange="NASDAQ")

    assert is_dataclass(instrument)
    assert instrument.symbol == "AAPL"

    with pytest.raises(FrozenInstanceError):
        instrument.symbol = "MSFT"  # type: ignore[misc]


def test_ohlcv_represents_market_bar_without_business_logic() -> None:
    instrument = Instrument(symbol="AAPL")
    bar = OHLCV(
        instrument=instrument,
        timestamp=datetime(2026, 1, 1, tzinfo=UTC),
        open=Decimal("100.00"),
        high=Decimal("105.00"),
        low=Decimal("99.00"),
        close=Decimal("104.00"),
        volume=Decimal("12345"),
    )

    assert bar.instrument == instrument
    assert bar.close == Decimal("104.00")


def test_evidence_contains_required_fields_and_immutable_metadata() -> None:
    source_metadata = {"source": "fixture"}
    evidence = Evidence(
        category="trend",
        title="Moving average alignment",
        confidence=0.7,
        weight=0.4,
        metadata=source_metadata,
    )
    source_metadata["source"] = "changed"

    assert evidence.category == "trend"
    assert evidence.title == "Moving average alignment"
    assert evidence.confidence == 0.7
    assert evidence.weight == 0.4
    assert evidence.metadata["source"] == "fixture"

    with pytest.raises(TypeError):
        evidence.metadata["source"] = "blocked"  # type: ignore[index]


def test_signal_does_not_contain_recommendation_action() -> None:
    evidence = Evidence(
        category="momentum",
        title="Momentum is rising",
        confidence=0.8,
        weight=0.5,
    )
    signal = Signal(
        instrument=Instrument(symbol="AAPL"),
        name="momentum_rising",
        confidence=0.8,
        evidence=(evidence,),
    )

    signal_field_names = {field.name for field in fields(signal)}

    assert "action" not in signal_field_names
    assert signal.evidence == (evidence,)


def test_recommendation_is_the_only_model_with_action_confidence_and_evidence() -> None:
    evidence = Evidence(
        category="risk",
        title="Risk is acceptable",
        confidence=0.6,
        weight=0.3,
    )
    recommendation = Recommendation(
        instrument=Instrument(symbol="AAPL"),
        action="HOLD",
        confidence=0.6,
        evidence=(evidence,),
    )

    assert recommendation.action == "HOLD"
    assert recommendation.confidence == 0.6
    assert recommendation.evidence == (evidence,)

    models_without_action = [Instrument, OHLCV, Evidence, Signal]
    for model in models_without_action:
        assert "action" not in {field.name for field in fields(model)}
