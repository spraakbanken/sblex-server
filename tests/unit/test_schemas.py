import pydantic
import pytest
from sblex.application.predicates import is_lemma, is_lexeme
from sblex.saldo_ws.schemas import Lemma, Lexeme


class WithLemma(pydantic.BaseModel):
    a: Lemma


class WithLexeme(pydantic.BaseModel):
    a: Lexeme


@pytest.mark.parametrize("word", ["lemma..nn.1", "lexeme..1"])
def test_lemma_schema_work(word: str) -> None:
    if is_lemma(word):
        _lemma = WithLemma(a=word)
    else:
        with pytest.raises(pydantic.ValidationError):
            _lemma = WithLemma(a=word)


@pytest.mark.parametrize("word", ["lemma..nn.1", "lexeme..1"])
def test_lexeme_schema_work(word: str) -> None:
    if is_lexeme(word):
        _lemma = WithLexeme(a=word)
    else:
        with pytest.raises(pydantic.ValidationError):
            _lemma = WithLexeme(a=word)
