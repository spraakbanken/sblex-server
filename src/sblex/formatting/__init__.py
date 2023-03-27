def prlex(lex):
    return "+".join([_prlex(l) for l in lex.split()])


def _prlex(lex):
    try:
        s = lex[:-3]
        if lex[-1] == "1":
            return s
        elif lex[-2] == ".":
            return s + "<sup>" + lex[-1] + "</sup>"
        else:
            return lex
    except:
        return lex


def lemma(l):
    rl = l[::-1]
    i = rl.find("..")
    pos = rl[:i][::-1]
    word = rl[(i + 2) :][::-1]
    return (word, pos)
