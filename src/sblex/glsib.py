import utf8
import saldo_util
import socket
import cjson
import table
from mod_python import apache
from mod_python import util

host = "localhost"
sem_port = 8091
size = 2048


def function(format, lemma):
    result = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, sem_port))
        s.send("rel " + lemma)
        buff = ""
        while True:
            buff = s.recv(size)
            if len(buff) == 0:
                break
            result += buff
        s.close()
        result_code = apache.OK
        if format == "xml":
            result = xmlize(result)
    except:
        result_code = apache.HTTP_SERVICE_UNAVAILABLE
    return (result, result_code)


def xmlize(s):
    j = cjson.decode(utf8.d(s))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    if not (j == []):
        xml += " <sense>" + j["sense"] + "</sense>\n"
        xml += " <ls>\n"
        for l in j["rel"]:
            xml += "   <l>" + l + "</l>\n"
        xml += " </ls>\n"
    xml += "</result>\n"
    return utf8.e(xml)
