import abc
import logging
from typing import Any

from sblex.application.predicates import is_lemma, is_lexeme

logger = logging.getLogger(__name__)


class LookupLid(abc.ABC):
    @abc.abstractmethod
    def get_lemma(self, lid: str) -> dict[str, Any]:
        """Get lemma with given `lid`.

        Raises
        ------
        LemmaNotFound
            if lemma was not found
        LookupLidError
            custom error
        """
        ...

    @abc.abstractmethod
    def get_lexeme(self, lid: str) -> dict[str, Any]:
        """Get lexeme with given `lid`.

        Raises
        ------
        LexemeNotFound
            if lexeme was not found
        LookupLidError
            custom error
        """
        ...

    def get_by_lid(self, lid: str) -> dict[str, Any]:
        """Get lemma or lexeme with given `lid`.

        This method will analyze `lid` to determine if a lemma or lexeme is requested.

        Raises
        ------
        LemmaNotFound
            if lemma was not found
        LexemeNotFound
            if lexeme was not found
        LookupLidError
            custom error
        """
        if is_lemma(lid):
            logger.debug("calling LookupLid.get_lemma for '%s'", lid)
            return self.get_lemma(lid)
        elif is_lexeme(lid):
            logger.debug("calling LookupLid.get_lexeme for '%s'", lid)
            return self.get_lexeme(lid)
        else:
            return {}


class LookupLidError(Exception):
    """Raised when the SemanticRepository fails."""


class LemmaNotFound(LookupLidError, KeyError):
    """Raised when a Lemma is not found."""


class LexemeNotFound(LookupLidError, KeyError):
    """Raised when a Lexeme is not found."""
