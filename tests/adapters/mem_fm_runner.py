from sblex.fm.fm_runner import FmRunner, InflectionRow


class MemFmRunner(FmRunner):
    def __init__(self, paradigms: dict[str, dict[str, list[InflectionRow]]]) -> None:
        self.paradigms = paradigms

    def inflection(self, paradigm: str, word: str) -> list[InflectionRow]:
        return self.paradigms.get(paradigm, {}).get(word) or []
