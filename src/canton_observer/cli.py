from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Literal

import typer
from rich.console import Console

from canton_observer.analysis.consensus import consensus_distance, visible_contract_ids
from canton_observer.analysis.reducibility import classify_claims
from canton_observer.analysis.visibility import compute_visibility_horizon
from canton_observer.ingest.simulation import load_scenario, scenario_names
from canton_observer.models import (
    ConsensusEstimate,
    ObserverReport,
    ReducibilityClass,
    ReportSummary,
)
from canton_observer.report.html_out import render_html
from canton_observer.report.json_out import render_json
from canton_observer.report.terminal import render_terminal

app = typer.Typer(help="Measure what a bounded Canton observer can see and prove.")
scenarios_app = typer.Typer(help="Inspect bundled simulation scenarios.")
app.add_typer(scenarios_app, name="scenarios")
console = Console()


def build_simulation_report(scenario_name: str, party_id: str) -> ObserverReport:
    scenario = load_scenario(scenario_name)
    parties = {party.party_id: party for party in scenario.parties}
    if party_id not in parties:
        raise ValueError(f"Unknown party: {party_id}")
    horizon = compute_visibility_horizon(scenario, party_id)
    reducibility = classify_claims(scenario, party_id, horizon)
    subject_acs = visible_contract_ids(scenario.contracts, party_id)
    distances = {
        counterparty: ConsensusEstimate(
            distance=consensus_distance(
                subject_acs, visible_contract_ids(scenario.contracts, counterparty)
            ),
            is_lower_bound=False,
        )
        for counterparty in horizon.visible_counterparties
    }
    total = len(reducibility) or 1
    summary = ReportSummary(
        locally_derivable_pct=100
        * sum(value == ReducibilityClass.LOCALLY_DERIVABLE for value in reducibility.values())
        / total,
        trust_required_pct=100
        * sum(value == ReducibilityClass.TRUST_REQUIRED for value in reducibility.values())
        / total,
        invisible_pct=100
        * sum(value == ReducibilityClass.INVISIBLE for value in reducibility.values())
        / total,
    )
    return ObserverReport(
        subject_party=parties[party_id],
        generated_at=datetime.now(UTC),
        source_mode="simulation",
        horizon=horizon,
        reducibility=reducibility,
        consensus_distances=distances,
        summary=summary,
    )


@app.command()
def audit(
    scenario: Annotated[str, typer.Option(help="Bundled simulation scenario")],
    party: Annotated[str, typer.Option(help="Subject party ID")],
    format_: Annotated[Literal["terminal", "json", "html"], typer.Option("--format")] = "terminal",
    out: Annotated[Path | None, typer.Option(help="Output path for HTML or JSON")] = None,
) -> None:
    try:
        report = build_simulation_report(scenario, party)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2) from exc
    if format_ == "terminal":
        render_terminal(report, console)
        return
    content = render_json(report) if format_ == "json" else render_html(report)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        console.print(str(out))
    else:
        typer.echo(content)


@scenarios_app.command("list")
def list_scenarios() -> None:
    for name in scenario_names():
        typer.echo(name)


@app.command()
def explain(metric: Annotated[str, typer.Argument()]) -> None:
    explanations = {
        "visibility": "Visible contracts divided by visible contracts plus detected known unknowns.",
        "reducibility": "Claims are locally derivable, trust required, or invisible.",
        "consensus": "Jaccard distance between party contract sets; live mode can only bound it.",
    }
    if metric not in explanations:
        raise typer.BadParameter("Choose visibility, reducibility, or consensus")
    typer.echo(explanations[metric])
