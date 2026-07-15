# Contributing

The widest contribution door is scenario authoring: a settlement, custody, lending, or fund-domain expert can add a validated YAML scenario without changing Python.

## Development

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m mypy src/canton_observer/analysis
python -m pytest --cov=canton_observer.analysis --cov-fail-under=80
```

## Scenario authoring

Copy a file in `src/canton_observer/scenarios/`. Define parties, contracts, disclosure roles, payload references, and two or three party-scoped claims. Use stable illustrative identifiers and simulated values only. Add a validation test and document the hand-computed horizon, reducibility classes, and pairwise distance.

Analysis code is strict-mypy checked. Keep transport logic outside `analysis/`, preserve the read-only boundary, and add a failing test before behavior. Commit with a DCO sign-off: `git commit -s`.
