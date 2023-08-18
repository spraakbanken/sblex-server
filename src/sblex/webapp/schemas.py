from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from sblex.application import is_lemma, is_lexeme
from typing_extensions import Annotated

# Lexeme = Annotated[str, AfterValidator(is_lexeme)]

# Lemma = Annotated[str, AfterValidator(is_lemma)]


class Lexeme(BaseModel):
    root: str


class Lemma(BaseModel):
    root: str
