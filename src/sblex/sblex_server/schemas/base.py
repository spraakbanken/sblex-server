from typing import Annotated

from pydantic import StringConstraints

Lexeme = Annotated[str, StringConstraints(pattern=r".*\.\.\d+")]
Lemma = Annotated[str, StringConstraints(pattern=r".*\.\.\w+\.\d+")]
