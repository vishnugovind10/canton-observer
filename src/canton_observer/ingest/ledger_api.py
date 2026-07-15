from typing import Any

import httpx


class LedgerApiSource:
    """EXPERIMENTAL read-only JSON Ledger API v2 adapter; not LocalNet-verified."""

    def __init__(self, host: str, port: int) -> None:
        self.base_url = f"http://{host}:{port}"

    def _get(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        response = httpx.get(f"{self.base_url}{path}", params=params, timeout=30.0)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data

    def list_parties(self) -> list[dict[str, object]]:
        data = self._get("/v2/parties")
        return list(data.get("partyDetails", []))

    def active_contracts(self, party_id: str) -> list[dict[str, object]]:
        body = {
            "eventFormat": {
                "filtersByParty": {
                    party_id: {
                        "cumulative": [{"identifierFilter": {"WildcardFilter": {"value": {}}}}]
                    }
                },
                "filtersForAnyParty": None,
                "verbose": True,
            },
            "verbose": True,
        }
        response = httpx.post(f"{self.base_url}/v2/state/active-contracts", json=body, timeout=30.0)
        response.raise_for_status()
        payload: list[dict[str, object]] = response.json()
        return payload
