from atlas.assessment.models import Assessment
from atlas.domain.shared import Evidence, Signal


class AssessmentEngine:
    def assess(self, signals: list[Signal]) -> Assessment:
        if not signals:
            raise ValueError("Assessment requires at least one signal.")

        signal_tuple = tuple(signals)
        evidence = self._collect_evidence(signal_tuple)
        confidence = self._aggregate_confidence(signal_tuple)

        return Assessment(
            summary=self._summary(signal_tuple, evidence, confidence),
            confidence=confidence,
            signals=signal_tuple,
            evidence=evidence,
        )

    def _aggregate_confidence(self, signals: tuple[Signal, ...]) -> float:
        return sum(signal.confidence for signal in signals) / len(signals)

    def _collect_evidence(self, signals: tuple[Signal, ...]) -> tuple[Evidence, ...]:
        return tuple(evidence for signal in signals for evidence in signal.evidence)

    def _summary(
        self,
        signals: tuple[Signal, ...],
        evidence: tuple[Evidence, ...],
        confidence: float,
    ) -> str:
        signal_count = len(signals)
        evidence_count = len(evidence)
        signal_word = "signal" if signal_count == 1 else "signals"
        evidence_word = "evidence item" if evidence_count == 1 else "evidence items"

        return (
            f"Assessment based on {signal_count} {signal_word} "
            f"and {evidence_count} {evidence_word}; confidence {confidence:.2f}."
        )
