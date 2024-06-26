# -*- coding: utf-8 -*-

import utf8
import saldo_util
import cjson
from mod_python import apache
from mod_python import util


def function(format, segment):
    result = print_compound(sorted(compound(segment), comp))

    return (result, apache.OK)


def htmlize(segment, s):
    j = cjson.decode(utf8.d(s))
    if j == []:
        content = "<center><b>" + segment + "</b> saknar analys.</center>"
    else:
        content = "<center><table>"
        len_c = 0
        for ws in j:
            if len_c == 0:
                len_c = len(ws)
            content += "<tr><td>\n"
            content += "<td>".join(
                [
                    pr_it(
                        "<b>"
                        + utf8.e(w["segment"])
                        + "</b>:("
                        + saldo_util.lemma_href(utf8.e(w["id"]))
                        + ", "
                        + utf8.e(w["msd"])
                        + ")",
                        len(ws),
                        len_c,
                    )
                    for w in ws
                ]
            )
            content += "</td></tr>\n"
        content += "</table></center>\n"
    html = saldo_util.html_document(segment, content, bar=False)
    return html


def pr_it(s, n, len_c):
    if n == len_c:
        return s
    else:
        return "<i>" + s + "</i>"


def compound(s, n=1):
    if len(s) < 1:
        return [[]]
    if n > 2:
        return []
    else:
        return [
            [add_prefix(a, pre1)] + c
            for (pre1, suf1) in saldo_util.inits(s)
            if len(pre1) > 1
            for (pre, suf) in sandhi(pre1, suf1)
            for a in saldo_util.lookup_ff(pre)
            if suf != [] or a["msd"] in ["ci", "cm", "c"]
            for c in compound(suf, n + 1)
        ]


def add_prefix(a, pre):
    a["segment"] = utf8.d(pre)
    return a


def ok_compound(c):
    if len(c) == 1:
        return (
            not (c[0]["msd"] in ["ci", "cm", "c"])
            and saldo_util.not_fragment(c[0]["msd"])
            and (c[0]["pos"][-1] != "h")
        )
    else:
        if (
            not (c[-1]["msd"] in ["ci", "cm", "c"])
            and saldo_util.not_fragment(c[0]["msd"])
            and (c[-1]["pos"] in ["nn", "vb", "av", "ab", "pm"] or c[-1]["pos"][-1] == "h")
            and c[0]["msd"] in ["ci", "c"]
        ):
            for i in range(1, len(c) - 1):
                if not (c[i]["msd"] in ["cm", "c"]):
                    return False
            return True
        return False


def print_compound(cs):
    comps_all = [c for c in cs if ok_compound(c)]
    comps = [c for c in comps_all if len(c) <= min([len(x) for x in comps_all]) + 1]
    if len(comps) < 1:
        return "[]"
    else:
        return utf8.e("[\n%s\n]" % (",\n".join([pr_list(c) for c in comps])))


def pr_list(js):
    return " [\n %s\n ]" % (",\n ".join([pr(j) for j in js]))


def pr(j):
    return '{"segment":"%s","gf":"%s","id":"%s","pos":"%s","is":[%s],"msd":"%s","p":"%s"}' % (
        j["segment"],
        j["gf"],
        j["id"],
        j["pos"],
        "%s%s%s" % (cit(j["is"]), '","'.join(j["is"]), cit(j["is"])),
        j["msd"],
        j["p"],
    )


def cit(xs):
    if xs == []:
        return ""
    else:
        return '"'
