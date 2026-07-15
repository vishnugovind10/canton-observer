# Architecture

```mermaid
flowchart LR
  Y["Validated YAML scenario"] --> L["SimulatedLedger"]
  J["Experimental JSON Ledger API v2"] --> I["LedgerSource"]
  L --> I
  I --> V["Visibility horizon"] --> R["Reducibility"] --> C["Consensus distance"]
  C --> O["Terminal / JSON / static HTML"]
```

The source boundary is read-only. Analysis accepts validated models and has no transport dependency. Reporters consume one `ObserverReport`, keeping terminal, JSON, and HTML semantics aligned.
