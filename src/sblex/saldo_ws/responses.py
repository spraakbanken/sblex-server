import typing as t

from fastapi.responses import JSONResponse as _JSONResponse
from fastapi.responses import Response
from json_arrays import jsonlib


class XMLResponse(Response):
    media_type = "application/xml"


class JavascriptResponse(Response):
    media_type = "text/javascript"


class JSONResponse(_JSONResponse):
    def render(self, content: t.Any) -> bytes:
        return jsonlib.dumps(content)
