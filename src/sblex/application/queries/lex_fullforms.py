import abc


class FullformLexQuery(abc.ABC):
    @abc.abstractmethod
    async def query(self, segment: str) -> list[dict]:
        ...
