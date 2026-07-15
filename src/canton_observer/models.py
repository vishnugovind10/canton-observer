from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Party(BaseModel):
    party_id: str
    display_name: str
    validator: str


class Contract(BaseModel):
    contract_id: str
    template_id: str
    signatories: list[str]
    observers: list[str]
    payload_fields: dict[str, Any]
    created_at: datetime


class Claim(BaseModel):
    claim_id: str
    subject_party: str
    fact: str
    contract_id: str
    input_contracts: list[str] = Field(default_factory=list)
    counterparty_asserted: bool = False


class Scenario(BaseModel):
    name: str
    description: str
    parties: list[Party]
    contracts: list[Contract]
    claims: list[Claim]


class VisibilityHorizon(BaseModel):
    party_id: str
    visible_contracts: list[str]
    visible_counterparties: list[str]
    known_unknowns: list[str]
    coverage_ratio: float


class ReducibilityClass(StrEnum):
    LOCALLY_DERIVABLE = "locally_derivable"
    TRUST_REQUIRED = "trust_required"
    INVISIBLE = "invisible"


class ConsensusEstimate(BaseModel):
    distance: float
    is_lower_bound: bool


class ReportSummary(BaseModel):
    locally_derivable_pct: float
    trust_required_pct: float
    invisible_pct: float


class ObserverReport(BaseModel):
    subject_party: Party
    generated_at: datetime
    source_mode: Literal["simulation", "ledger_api"]
    horizon: VisibilityHorizon
    reducibility: dict[str, ReducibilityClass]
    consensus_distances: dict[str, ConsensusEstimate]
    summary: ReportSummary
