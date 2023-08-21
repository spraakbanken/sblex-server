def prlex(lex):
    return "+".join([_prlex(le) for le in lex.split()])


def _prlex(lex):
    try:
        s = lex[:-3]
        if lex[-1] == "1":
            return s
        elif lex[-2] == ".":
            return f"{s}<sup>{lex[-1]}</sup>"
        else:
            return lex
    except:  # noqa: E722
        return lex


def lemma(lem):
    # TODO: rewrite with 'rfind'
    rl = lem[::-1]
    i = rl.find("..")
    pos = rl[:i][::-1]
    word = rl[(i + 2) :][::-1]
    return (word, pos)
