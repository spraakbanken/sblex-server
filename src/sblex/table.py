import utf8
import os
import codecs
from mod_python import apache
from mod_python import util
import popen2
import cjson
import saldo_util


def function(format, paradigm, word):
    result = ""
    try:
        j = cjson.decode(utf8.d(result))
        if format == "html":
            result = htmlize(paradigm, word, j)
        elif format == "xml":
            result = xmlize(paradigm, j)
        result_code = apache.OK
    except:
        result_code = apache.HTTP_SERVICE_UNAVAILABLE
    return (utf8.e(result), result_code)


def xmlize(paradigm, j):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    xml += "<table>\n"
    xml += "\n".join(
        [
            "<w><form>%s</form><gf>%s</gf><pos>%s</pos><is>%s</is><msd>%s</msd><p>%s</p></w>"
            % (
                x["word"],
                x["head"],
                x["pos"],
                " ".join(x["inhs"]),
                x["param"],
                utf8.d(paradigm),
            )
            for x in j
        ]
    )
    xml += "</table>\n"
    xml += "</result>\n"
    return xml


def htmlize(paradigm, word, j):
    if j == []:
        content = "<center><p>paradigm " + utf8.d(paradigm) + " finns ej.</p></center>"
        return saldo_util.html_document(utf8.d(paradigm) + ' "' + utf8.d(word) + '"', content)
    content = '<table border="1"><tr><td><b>grundform</b></td><td>%s</td></tr>' % utf8.d(word)
    content += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (
        "mönster".decode("UTF-8"),
        utf8.d(paradigm),
    )
    content += "<tr><td><b>%s</b></td><td>%s</td></tr>" % ("ordklass", j[0]["pos"])
    if len(j[0]["inhs"]) > 0:
        content += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (
            "inherenta drag",
            ", ".join(j[0]["inhs"]),
        )
    content += (
        '<tr><td colspan="2" style="text-align:center;"><b>böjningstabell</b></td></tr>'.decode(
            "UTF-8"
        )
    )
    data = group_msd(j)
    prev = ""
    for x in j:
        msd = x["param"]
        if msd != prev:
            data[msd].reverse()
            content += "<tr><td><i>%s</i></td><td>%s</td></tr>" % (
                msd,
                "/".join(data[msd]),
            )
            prev = msd
    content += "</table></center>"
    return saldo_util.html_document(j[0]["p"] + ' "' + j[0]["head"] + '"', content, bar=False)


def group_msd(j):
    dict = {}
    for x in j:
        msd = x["param"]
        wf = x["word"]
        if msd in dict:
            dict[msd].append(wf)
        else:
            dict[msd] = [wf]
    return dict
