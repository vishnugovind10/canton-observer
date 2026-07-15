import json
from pathlib import Path

from typer.testing import CliRunner

from canton_observer.cli import app
from canton_observer.ingest.simulation import load_scenario, scenario_names

runner = CliRunner()


def test_all_bundled_scenarios_validate() -> None:
    assert scenario_names() == ["bilateral_repo", "fund_tokenization", "tri_party_settlement"]
    for name in scenario_names():
        scenario = load_scenario(name)
        assert scenario.name == name
        assert scenario.parties
        assert scenario.contracts


def test_json_audit_surfaces_simulation_mode() -> None:
    result = runner.invoke(
        app,
        ["audit", "--scenario", "bilateral_repo", "--party", "BankA", "--format", "json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["source_mode"] == "simulation"
    assert payload["horizon"]["known_unknowns"] == ["#repo-rehyp-b"]


def test_html_audit_is_self_contained_and_badged(tmp_path: Path) -> None:
    output = tmp_path / "observer.html"
    result = runner.invoke(
        app,
        [
            "audit",
            "--scenario",
            "tri_party_settlement",
            "--party",
            "SettlementAgent",
            "--format",
            "html",
            "--out",
            str(output),
        ],
    )
    assert result.exit_code == 0, result.output
    html = output.read_text(encoding="utf-8")
    assert "SIMULATION" in html
    assert "<style>" in html
    assert "<script" not in html


def test_unknown_party_is_a_clean_cli_error() -> None:
    result = runner.invoke(
        app,
        ["audit", "--scenario", "bilateral_repo", "--party", "Missing"],
    )
    assert result.exit_code != 0
    assert "Unknown party" in result.output
