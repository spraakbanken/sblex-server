import abc


class FullformQuery(abc.ABC):
    @abc.abstractmethod
    async def query(self, fragment: str) -> bytes:
        ...
