from datetime import UTC, datetime

import pytest

from canton_observer.analysis.consensus import consensus_distance, live_consensus_lower_bound
from canton_observer.analysis.reducibility import classify_claims
from canton_observer.analysis.visibility import compute_visibility_horizon
from canton_observer.models import (
    Claim,
    Contract,
    Party,
    ReducibilityClass,
    Scenario,
)


def bilateral_repo() -> Scenario:
    created = datetime(2026, 7, 15, tzinfo=UTC)
    return Scenario(
        name="bilateral_repo",
        description="Hand-computed fixture",
        parties=[
            Party(party_id="BankA", display_name="Bank A", validator="validator-a"),
            Party(party_id="BankB", display_name="Bank B", validator="validator-b"),
        ],
        contracts=[
            Contract(
                contract_id="#repo",
                template_id="Repo:Agreement",
                signatories=["BankA", "BankB"],
                observers=[],
                payload_fields={"notional": 10_000_000, "references": ["#collateral"]},
                created_at=created,
            ),
            Contract(
                contract_id="#collateral",
                template_id="Repo:Collateral",
                signatories=["BankB"],
                observers=["BankA"],
                payload_fields={"market_value": 10_250_000, "references": ["#rehyp"]},
                created_at=created,
            ),
            Contract(
                contract_id="#rehyp",
                template_id="Repo:Rehypothecation",
                signatories=["BankB"],
                observers=[],
                payload_fields={"amount": 2_000_000},
                created_at=created,
            ),
        ],
        claims=[
            Claim(
                claim_id="repo-notional",
                subject_party="BankA",
                fact="repo_notional",
                contract_id="#repo",
                input_contracts=["#repo"],
            ),
            Claim(
                claim_id="collateral-value",
                subject_party="BankA",
                fact="collateral_value",
                contract_id="#collateral",
                input_contracts=["#repo", "#collateral"],
                counterparty_asserted=True,
            ),
            Claim(
                claim_id="rehypothecation",
                subject_party="BankA",
                fact="downstream_rehypothecation",
                contract_id="#repo",
                input_contracts=["#rehyp"],
            ),
        ],
    )


def test_visibility_horizon_has_hand_computed_bilateral_values() -> None:
    scenario = bilateral_repo()
    horizon = compute_visibility_horizon(scenario, "BankA")

    # BankA sees #repo and #collateral, while #rehyp is referenced but undisclosed.
    assert horizon.visible_contracts == ["#collateral", "#repo"]
    assert horizon.visible_counterparties == ["BankB"]
    assert horizon.known_unknowns == ["#rehyp"]
    assert horizon.coverage_ratio == pytest.approx(2 / 3)


def test_reducibility_classifies_local_trust_and_invisible_claims() -> None:
    scenario = bilateral_repo()
    horizon = compute_visibility_horizon(scenario, "BankA")

    result = classify_claims(scenario, "BankA", horizon)

    assert result == {
        "repo-notional": ReducibilityClass.LOCALLY_DERIVABLE,
        "collateral-value": ReducibilityClass.TRUST_REQUIRED,
        "rehypothecation": ReducibilityClass.INVISIBLE,
    }


def test_consensus_distance_uses_jaccard_distance() -> None:
    # BankA ACS={repo, collateral}; BankB ACS={repo, collateral, rehyp}; distance=1-2/3.
    assert consensus_distance(
        {"#repo", "#collateral"}, {"#repo", "#collateral", "#rehyp"}
    ) == pytest.approx(1 / 3)
    assert consensus_distance(set(), set()) == 0.0


def test_live_consensus_is_explicitly_a_lower_bound() -> None:
    estimate = live_consensus_lower_bound(shared_visible=2, subject_visible=5)
    assert estimate.distance == pytest.approx(0.6)
    assert estimate.is_lower_bound is True
