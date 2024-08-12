from typing import Annotated

from pydantic import BaseModel, StringConstraints


class Version(BaseModel):
    version: Annotated[str, StringConstraints(pattern=r"\d+\.\d+\.\d+(-\w+\d+)?")]
    date: Annotated[str, StringConstraints(pattern=r"\d{4}-\d{2}-\d{2}")]
