import abc
import typing


class Paradigms(abc.ABC):
    @abc.abstractmethod
    def query(self, s: str) -> typing.Tuple[str, list[str]]: ...

    def prepare_args(self, s: str) -> typing.Tuple[str, list[str]]:
        xs = [x.strip() for x in s.split(",") if len(x) > 0]
        baseform, pos = split_word_and_pos(xs[0])
        xs[0] = f"{baseform}:{pos}"
        return baseform, xs


def split_word_and_pos(s: str) -> typing.Tuple[str, str]:
    n = s.find(":")
    if n == -1:
        raise NoPartOfSpeechOnBaseform()
    word = s[:n].strip()
    pos = s[n + 1 :].strip()
    return word, pos


class NoPartOfSpeechOnBaseform(Exception):
    """The baseform must contain a Part-of-Speech tag."""
