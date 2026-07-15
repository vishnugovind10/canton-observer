from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from canton_observer.models import ObserverReport


def render_terminal(report: ObserverReport, console: Console) -> None:
    badge = report.source_mode.upper()
    console.print(
        Panel(
            f"[bold]{report.subject_party.display_name}[/bold]  [{badge}]", title="Canton Observer"
        )
    )
    console.print(f"Visibility coverage: {report.horizon.coverage_ratio:.1%}")
    table = Table("Claim", "Reducibility")
    for claim, classification in report.reducibility.items():
        table.add_row(claim, classification.value)
    console.print(table)
    for party, estimate in report.consensus_distances.items():
        label = "lower bound" if estimate.is_lower_bound else "exact simulation"
        console.print(f"Consensus distance to {party}: {estimate.distance:.3f} ({label})")
