# Build report

Build date: 2026-07-15. Python: 3.11.9. Source mode exercised: simulation.

| Milestone | Status | Evidence |
|---|---|---|
| M1 Scaffold, models, CI | PARTIAL | `pip install -e ".[dev]"` and `canton-observer --help` pass. GitHub Actions matrix is configured for 3.11/3.12; hosted status is pending the first push. |
| M2 Simulation and scenarios | DONE | Pydantic loads `bilateral_repo`, `fund_tokenization`, and `tri_party_settlement`; `canton-observer scenarios list` prints all three. |
| M3 Three metrics | DONE | Hand-computed bilateral tests cover 2/3 horizon coverage, three reducibility classes, and Jaccard distance 1/3. Analysis coverage: 96%. |
| M4 Reports | DONE | Terminal and JSON tests pass. `audit --scenario tri_party_settlement --party SettlementAgent --format html` produced a self-contained badged HTML file. |
| M5 Ledger API | DONE | Read-only v2 party/ACS client implemented and explicitly labeled experimental. LocalNet test is skipped; no LocalNet verification is claimed. |
| M6 Docs and collaboration | DONE | Required README order, formal methodology, architecture, API notes, templates, DCO instructions, and six seed issues are present. |

## Verification snapshot

```text
ruff: All checks passed!
mypy: Success: no issues found in 4 source files
pytest: 9 passed, 1 skipped
analysis coverage: 96.23%
```

The skipped test requires the official Canton LocalNet. It remains skipped because LocalNet was unavailable in this environment.
