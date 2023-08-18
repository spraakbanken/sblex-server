import pytest
from sblex.application.predicates import is_lemma, is_lexeme


@pytest.mark.parametrize(
    "lid, expected", [("vanlig..1", False), ("dväljas..vb.1", True)]
)
def test_is_lemma(lid: str, expected: bool) -> None:  # noqa: FBT001
    assert is_lemma(lid) is expected


@pytest.mark.parametrize(
    "lid, expected", [("vanlig..1", True), ("dväljas..vb.1", False), ("rnd", True)]
)
def test_is_lexeme(lid: str, expected: bool) -> None:  # noqa: FBT001
    assert is_lexeme(lid) is expected
