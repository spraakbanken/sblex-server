import utf8
from mod_python import apache
import cjson
import saldo_util


def function(format, s):
    result = ""
    # try:

    xs = [x.strip() for x in s.split(",") if len(x) > 0]
    if xs[0].find(":") == -1 and format == "html":
        return (
            saldo_util.html_pdocument(
                "SALDO",
                "<center><p>Grundformen måste förses med ordklass (grundform:ordklass).</p></center>",
            ),
            apache.OK,
        )

    result = ""

    if result.strip() == "":
        result = "[]"
    j = cjson.decode(utf8.d(result))

    if format == "xml":
        result = xmlize(j).encode("UTF-8")
    result_code = apache.OK
    #        except:
    # result_code = apache.HTTP_NOT_FOUND
    return (result, result_code)


def xmlize(j):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<paradigms>\n"
    xml += "".join(["<p>" + x + "</p>" for x in j])
    xml += "</paradigms>\n"
    return xml
