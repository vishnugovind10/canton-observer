import pytest

from canton_observer.ingest.ledger_api import LedgerApiSource


def test_ledger_client_exposes_read_only_operations_only() -> None:
    source = LedgerApiSource("localhost", 7575)
    assert hasattr(source, "list_parties")
    assert hasattr(source, "active_contracts")
    assert not hasattr(source, "submit")
    assert not hasattr(source, "exercise")


@pytest.mark.localnet
@pytest.mark.skip(
    reason="Requires official Canton LocalNet; not available in this build environment"
)
def test_localnet_active_contracts() -> None:
    assert LedgerApiSource("localhost", 7575).active_contracts("BankA")
