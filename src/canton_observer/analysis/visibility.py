from collections.abc import Iterable
from typing import Any

from canton_observer.models import Scenario, VisibilityHorizon


def _strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _strings(nested)


def compute_visibility_horizon(scenario: Scenario, party_id: str) -> VisibilityHorizon:
    party_ids = {party.party_id for party in scenario.parties}
    if party_id not in party_ids:
        raise ValueError(f"Unknown party: {party_id}")
    visible = [
        contract
        for contract in scenario.contracts
        if party_id in contract.signatories or party_id in contract.observers
    ]
    visible_ids = {contract.contract_id for contract in visible}
    all_ids = {contract.contract_id for contract in scenario.contracts}
    references = {
        value
        for contract in visible
        for value in _strings(contract.payload_fields)
        if value in all_ids or value.startswith("#")
    }
    known_unknowns = sorted(references - visible_ids)
    counterparties = sorted(
        {
            other
            for contract in visible
            for other in contract.signatories + contract.observers
            if other != party_id
        }
    )
    denominator = len(visible_ids) + len(known_unknowns)
    return VisibilityHorizon(
        party_id=party_id,
        visible_contracts=sorted(visible_ids),
        visible_counterparties=counterparties,
        known_unknowns=known_unknowns,
        coverage_ratio=len(visible_ids) / denominator if denominator else 1.0,
    )
