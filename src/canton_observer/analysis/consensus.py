from canton_observer.models import ConsensusEstimate, Contract


def consensus_distance(left: set[str], right: set[str]) -> float:
    union = left | right
    if not union:
        return 0.0
    return 1.0 - (len(left & right) / len(union))


def live_consensus_lower_bound(shared_visible: int, subject_visible: int) -> ConsensusEstimate:
    if shared_visible < 0 or subject_visible < 0 or shared_visible > subject_visible:
        raise ValueError("Expected 0 <= shared_visible <= subject_visible")
    distance = 0.0 if subject_visible == 0 else 1.0 - (shared_visible / subject_visible)
    return ConsensusEstimate(distance=distance, is_lower_bound=True)


def visible_contract_ids(contracts: list[Contract], party_id: str) -> set[str]:
    return {
        contract.contract_id
        for contract in contracts
        if party_id in contract.signatories or party_id in contract.observers
    }
