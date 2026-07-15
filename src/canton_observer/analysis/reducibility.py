from canton_observer.models import ReducibilityClass, Scenario, VisibilityHorizon


def classify_claims(
    scenario: Scenario, party_id: str, horizon: VisibilityHorizon
) -> dict[str, ReducibilityClass]:
    contracts = {contract.contract_id: contract for contract in scenario.contracts}
    unknowns = set(horizon.known_unknowns)
    classifications: dict[str, ReducibilityClass] = {}
    for claim in scenario.claims:
        if claim.subject_party != party_id:
            continue
        if any(contract_id in unknowns for contract_id in claim.input_contracts):
            classifications[claim.claim_id] = ReducibilityClass.INVISIBLE
            continue
        inputs = [contracts[contract_id] for contract_id in claim.input_contracts]
        if claim.counterparty_asserted or any(party_id not in item.signatories for item in inputs):
            classifications[claim.claim_id] = ReducibilityClass.TRUST_REQUIRED
        else:
            classifications[claim.claim_id] = ReducibilityClass.LOCALLY_DERIVABLE
    return classifications
