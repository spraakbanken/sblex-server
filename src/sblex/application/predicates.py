def is_lemma(s):
    i = s.rfind(".")
    return False if (i == -1) else s[i - 1] != "."


def is_lexeme(s):
    if s == "rnd":
        return True
    i = s.rfind(".")
    return False if (i == -1) else s[i - 1] == "."
