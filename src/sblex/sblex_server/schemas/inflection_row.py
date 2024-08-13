from pydantic import BaseModel


class InflectionRow(BaseModel):
    form: str
    head: str
    pos: str
    inhs: list[str]
    msd: str
    p: str
