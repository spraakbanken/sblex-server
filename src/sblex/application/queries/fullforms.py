import abc


class FullformQuery(abc.ABC):
    @abc.abstractmethod
    def query(self, fragment: str) -> bytes:
        ...
