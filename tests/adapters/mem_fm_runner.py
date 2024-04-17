from sblex.fm.fm_runner import FmRunner, InflectionRow


class MemFmRunner(FmRunner):
    def __init__(
        self,
        paradigms: dict[str, dict[str, list[InflectionRow]]],
        word_to_paradigm: dict[str, list[str]],
    ) -> None:
        self._paradigms = paradigms
        self._word_to_paradigm = word_to_paradigm

    def inflection(self, paradigm: str, word: str) -> list[InflectionRow]:
        return self._paradigms.get(paradigm, {}).get(word) or []

    def paradigms(self, words: list[str]):
        return self._word_to_paradigm.get(words[0], [])
