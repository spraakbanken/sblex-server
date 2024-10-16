import urllib.error
import urllib.parse
import urllib.request

from fastapi import FastAPI

from sblex.formatting import prlex


def lexeme_ref(lids, *, app: FastAPI):
    if lids == "":
        return "*"
    else:
        return "+".join(
            [
                '<a href="{}">{}</a>'.format(
                    app.url_path_for("lids:lid-html", lid=urllib.parse.quote(lid)),
                    prlex(lid),
                )
                for lid in lids.split()
            ]
        )
