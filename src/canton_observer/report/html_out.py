from jinja2 import Template

from canton_observer.models import ObserverReport

_TEMPLATE = Template("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Canton Observer Report</title>
<style>
body{font-family:Arial,sans-serif;color:#172033;max-width:980px;margin:40px auto;padding:0 24px}
h1,h2{font-family:Georgia,serif}.badge{background:#f4c542;padding:5px 9px;font-weight:bold}
table{border-collapse:collapse;width:100%;margin:18px 0}th,td{border:1px solid #ccd3df;padding:8px;text-align:left}
.metric{font-size:2rem}footer{margin-top:36px;border-top:1px solid #ccd3df;padding-top:14px;color:#526079}
</style></head><body>
<span class="badge">{{ report.source_mode.upper() }}</span>
<h1>Observer Completeness Report</h1><p>{{ report.subject_party.display_name }} ({{ report.subject_party.party_id }})</p>
<h2>Visibility horizon</h2><p class="metric">{{ "%.1f"|format(report.horizon.coverage_ratio * 100) }}%</p>
<p>Known unknowns: {{ report.horizon.known_unknowns|join(", ") or "None detected" }}</p>
<h2>Reducibility</h2><table><tr><th>Claim</th><th>Class</th></tr>
{% for claim, value in report.reducibility.items() %}<tr><td>{{ claim }}</td><td>{{ value.value }}</td></tr>{% endfor %}</table>
<h2>Consensus distance</h2><table><tr><th>Counterparty</th><th>Distance</th><th>Bound</th></tr>
{% for party, estimate in report.consensus_distances.items() %}<tr><td>{{ party }}</td><td>{{ "%.3f"|format(estimate.distance) }}</td><td>{{ "lower bound" if estimate.is_lower_bound else "exact simulation" }}</td></tr>{% endfor %}</table>
<footer>Read-only diagnostic output. Not an audit opinion.</footer></body></html>""")


def render_html(report: ObserverReport) -> str:
    return _TEMPLATE.render(report=report)
