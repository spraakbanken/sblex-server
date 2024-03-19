# -*- coding: utf-8 -*-

import utf8
import socket
import saldo_util
import cjson
from mod_python import apache
from mod_python import util

host = "localhost"
sem_port = 8091
size = 2048


def function(format, lexeme):
    result = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, sem_port))
        s.send("lex " + lexeme)
        buff = ""
        while True:
            buff = s.recv(size)
            if len(buff) == 0:
                break
            result += buff
        s.close()
        result_code = apache.OK
    except:
        result_code = apache.HTTP_SERVICE_UNAVAILABLE
        return ("", result_code)
    if lexeme == "rnd" and format == "json":
        j = cjson.decode(utf8.d(result))
        ws = saldo_util.wordforms(utf8.e(j["lex"]))
        j["fs"] = ws
        s = (
            '{\n "lex":"%s",\n "fm":"%s",\n "fp":"%s",\n "mf":%s,\n "pf":%s,\n "l":%s,\n "fs":%s\n}'
            % (
                j["lex"],
                j["fm"],
                j["fp"],
                pr_list(j["mf"]),
                pr_list(j["pf"]),
                pr_list(j["l"]),
                pr_list(ws),
            )
        )
        result = utf8.e(s)
    return (result, result_code)


def pr_list(xs):
    xs = list(set(xs))
    xs.sort()
    if xs == []:
        return "[]"
    else:
        return '["%s"]' % ('","'.join(xs))
