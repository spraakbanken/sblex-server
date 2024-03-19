from fastapi.responses import Response


class XMLResponse(Response):
    media_type = "application/xml"


class JavascriptResponse(Response):
    media_type = "text/javascript"
