from pydantic import BaseModel

# Lexeme = Annotated[str, AfterValidator(is_lexeme)]

# Lemma = Annotated[str, AfterValidator(is_lemma)]


class Lexeme(BaseModel):
    root: str


class Lemma(BaseModel):
    root: str
