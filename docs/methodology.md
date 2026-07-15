# Methodology

## Visibility horizon

For party `p`, `ACS_p` contains contracts where `p` is a signatory or observer. `U_p` contains identifiers referenced by `ACS_p` but absent from it. Coverage is `|ACS_p| / (|ACS_p| + |U_p|)`. A zero-information view has coverage 1 only when no references are detectable; this is not evidence of global completeness.

Simulation references resolve against the scenario's global contract set. Live references are detected from contract-ID-shaped payload strings and can produce false negatives.

## Reducibility

A claim is locally derivable when every configured input is visible and subject-signed. It is trust-required when at least one input is observer-only or counterparty-asserted. It is invisible when a configured dependency is a known unknown. Percentages divide each class count by configured claims for the subject.

## Consensus distance

Simulation computes `D(p,q) = 1 - |ACS_p ∩ ACS_q| / |ACS_p ∪ ACS_q|`, with distance zero for two empty sets. A live single-party query cannot observe `ACS_q`; any estimate derived from `p`'s visible overlap is labeled a lower bound. Exact live distance requires disclosure from both parties.
