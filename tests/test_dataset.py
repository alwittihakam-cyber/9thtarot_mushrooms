"""Tests for the dataset and the grading rules. Run: pytest -q"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("build", ROOT / "analysis" / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def claim(**kw):
    base = dict(claim_id="EV9999", species_id="s", substrate_id="w", substrate_form="log",
                metric_class="production", evidence_level="2", outcome="good", source_id="X")
    base.update(kw)
    return base


def test_dataset_validates():
    assert build.validate() == []


def test_best_level_wins_over_more_claims():
    cells = build.aggregate([claim(evidence_level="1", outcome="poor", claim_id="EV0001"),
                             claim(evidence_level="3", outcome="excellent", claim_id="EV0002"),
                             claim(evidence_level="3", outcome="excellent", claim_id="EV0003")])
    c = cells[("s", "w")]
    assert c["best_level"] == 1 and c["outcome"] == "poor"


def test_median_rounds_down_and_flags_conflict():
    cells = build.aggregate([claim(outcome="excellent", claim_id="EV0001"),
                             claim(outcome="marginal", claim_id="EV0002")])
    c = cells[("s", "w")]
    assert c["outcome"] == "good"          # median 3.0 of (2, 4)
    assert c["conflict"] == "yes"          # spans two steps


def test_log_claims_override_sawdust():
    cells = build.aggregate([claim(substrate_form="sawdust-bed", outcome="excellent", claim_id="EV0001"),
                             claim(substrate_form="log", outcome="marginal", claim_id="EV0002")])
    assert cells[("s", "w")]["outcome"] == "marginal"


def test_non_production_never_grades():
    cells = build.aggregate([claim(metric_class="quality", outcome="excellent")])
    c = cells[("s", "w")]
    assert c["best_level"] == "" and c["other_evidence"] == "quality"
    assert build.verdict(c) == "no production data"


def test_extrapolation_is_never_supported():
    cells = build.aggregate([claim(evidence_level="5", outcome="excellent")])
    assert build.verdict(cells[("s", "w")]) == "hypothesis only"


def test_known_findings_hold():
    """Regression checks on findings the README states."""
    cells = build.aggregate(build.read("evidence"))
    assert build.verdict(cells[("kikurage", "konara")]) == "contradicted"
    assert build.verdict(cells[("reishi", "prunus-mume")]) == "hypothesis only"
    assert cells[("hiratake", "fagus")]["best_level"] == 1


def test_half_step_median_rounds_to_marginal_not_pilot_label():
    cells = build.aggregate([claim(outcome="good", claim_id="EV0001"),
                             claim(outcome="marginal", claim_id="EV0002")])
    assert cells[("s", "w")]["outcome"] == "marginal"
