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
        if format == "xml":
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
