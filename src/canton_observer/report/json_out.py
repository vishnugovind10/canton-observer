from canton_observer.models import ObserverReport


def render_json(report: ObserverReport) -> str:
    return report.model_dump_json(indent=2)
