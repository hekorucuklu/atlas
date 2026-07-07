from dataclasses import FrozenInstanceError

import pytest

from atlas.assessment import Assessment, AssessmentEngine
from atlas.domain.shared import Evidence, Instrument, Signal


def make_signal(name: str, confidence: float, evidence: tuple[Evidence, ...]) -> Signal:
    return Signal(
        instrument=Instrument(symbol="AAPL"),
        name=name,
        confidence=confidence,
        evidence=evidence,
    )


def make_evidence(title: str, confidence: float = 0.5) -> Evidence:
    return Evidence(
        category="momentum",
        title=title,
        confidence=confidence,
        weight=1.0,
    )


def test_assess_single_signal() -> None:
    evidence = make_evidence("RSI neutral", confidence=0.2)
    signal = make_signal("rsi_momentum", 0.2, (evidence,))

    assessment = AssessmentEngine().assess([signal])

    assert assessment == Assessment(
        summary="Assessment based on 1 signal and 1 evidence item; confidence 0.20.",
        confidence=0.2,
        signals=(signal,),
        evidence=(evidence,),
    )


def test_assess_multiple_signals() -> None:
    first_evidence = make_evidence("RSI below 30", confidence=0.8)
    second_evidence = make_evidence("Trend improving", confidence=0.6)
    first_signal = make_signal("rsi_momentum", 0.8, (first_evidence,))
    second_signal = make_signal("trend_context", 0.6, (second_evidence,))

    assessment = AssessmentEngine().assess([first_signal, second_signal])

    assert assessment.confidence == pytest.approx(0.7)
    assert assessment.signals == (first_signal, second_signal)
    assert assessment.summary == "Assessment based on 2 signals and 2 evidence items; confidence 0.70."


def test_assess_empty_signal_list() -> None:
    with pytest.raises(ValueError, match="at least one signal"):
        AssessmentEngine().assess([])


def test_assessment_preserves_every_evidence_object() -> None:
    first = make_evidence("First")
    second = make_evidence("Second")
    third = make_evidence("Third")
    first_signal = make_signal("first", 0.4, (first, second))
    second_signal = make_signal("second", 0.8, (third,))

    assessment = AssessmentEngine().assess([first_signal, second_signal])

    assert assessment.evidence == (first, second, third)


def test_assessment_confidence_is_deterministic() -> None:
    signals = [
        make_signal("first", 0.1, (make_evidence("First"),)),
        make_signal("second", 0.4, (make_evidence("Second"),)),
        make_signal("third", 0.7, (make_evidence("Third"),)),
    ]
    engine = AssessmentEngine()

    first_assessment = engine.assess(signals)
    second_assessment = engine.assess(signals)

    assert first_assessment.confidence == pytest.approx(0.4)
    assert second_assessment.confidence == first_assessment.confidence
    assert second_assessment.summary == first_assessment.summary


def test_assessment_is_immutable() -> None:
    assessment = AssessmentEngine().assess([
        make_signal("rsi_momentum", 0.2, (make_evidence("RSI neutral"),))
    ])

    with pytest.raises(FrozenInstanceError):
        assessment.confidence = 0.9  # type: ignore[misc]
