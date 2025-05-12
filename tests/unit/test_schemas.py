import pydantic
import pytest

from sblex.saldo_ws.schemas import Lemma, Lexeme


class WithLemma(pydantic.BaseModel):
    a: Lemma


class WithLexeme(pydantic.BaseModel):
    a: Lexeme


@pytest.mark.parametrize("word", ["lemma..nn.1"])
def test_lemma_schema_work(word: str) -> None:
    _lemma = WithLemma(a=word)


@pytest.mark.parametrize("word", ["lexeme..1"])
def test_non_lemma_raises_validation_error(word: str) -> None:
    with pytest.raises(pydantic.ValidationError):
        _lemma = WithLemma(a=word)


@pytest.mark.parametrize("word", ["lexeme..1"])
def test_lexeme_schema_work(word: str) -> None:
    _lemma = WithLexeme(a=word)


@pytest.mark.parametrize("word", ["lemma..nn.1"])
def test_non_lexeme_raises_validation_error(word: str) -> None:
    with pytest.raises(pydantic.ValidationError):
        _lemma = WithLexeme(a=word)
