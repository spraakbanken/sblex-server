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
    if format == "xml":
        result = xmlize(result)
    elif format == "graph":
        result = graph(lexeme, result)
    elif format == "html":
        result = htmlize(lexeme, result)
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


def graph(l, s):
    j = cjson.decode(utf8.d(s))
    if l != "PRIM..1":
        fm = (
            "document.location.href = 'http://spraakbanken.gu.se/ws/saldo-ws/lid/graph/%s';"
            % j["fm"]
        )
    else:
        fm = ""
    content = """
  <div style="width: 500px; height: 500px;">
  <script type="text/javascript" src="https://svn.spraakdata.gu.se/repos/sblex/pub/js/protovis-r3.2.js"></script>
  <script type="text/javascript" src="http://spraakbanken.gu.se/ws/saldo-ws/lid/protojs/%s"></script>
  <script type="text/javascript+protovis">

var vis = new pv.Panel()
   .width(500)
    .height(500);

var tree = vis.add(pv.Layout.Tree)
    .nodes(pv.dom(flare).root("%s").nodes())
    .depth(150)
    .breadth(100)
    .orient("radial");

tree.link.add(pv.Line);

tree.node.add(pv.Dot)
    .fillStyle(function(n) n.firstChild ? "#ffffff" : "#ffffff")
    .size(10)
    .event("mouseover", function() this.fillStyle("blue"))
    .event("mouseout", function() this.fillStyle(undefined))
    .event("click", function(n) {
    if(n.nodeValue != undefined){
    document.location.href = n.nodeValue;
    }
    else{
    %s
    }
    });

tree.label.add(pv.Label)
   .text(function(n) n.nodeName.replace('..1','').replace('..','_'))
   .font("12px 'Arvo', sans-serif")
   .events("all")
   .cursor("hand")
   .event("click", function(n) {
    if(n.nodeValue != undefined){
      document.location.href = n.nodeValue;
      }
    else{
    %s
    }
    });


vis.render();

    </script>
  </div>""" % (
        l,
        l,
        fm.encode("UTF-8"),
        fm.encode("UTF-8"),
    )
    html = saldo_util.html_document(l, content, bar=False)
    return html
