from abc import ABC, abstractmethod

from canton_observer.models import Contract, Party


class LedgerSource(ABC):
    """Read-only source contract. Mutation methods intentionally do not exist."""

    @abstractmethod
    def list_parties(self) -> list[Party]:
        raise NotImplementedError

    @abstractmethod
    def active_contracts(self, party_id: str) -> list[Contract]:
        raise NotImplementedError
