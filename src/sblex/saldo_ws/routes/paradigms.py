import sys

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, ORJSONResponse, RedirectResponse
from opentelemetry import trace

from sblex.application.queries import NoPartOfSpeechOnBaseform, Paradigms
from sblex.saldo_ws import deps, templating

router = APIRouter()


@router.get("/json/{words}", response_model=list[str])
async def get_para_json(words: str, paradigms: Paradigms = Depends(deps.get_paradigms)):  # noqa: B008
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        try:
            _baseform, result = paradigms.query(words)
        except NoPartOfSpeechOnBaseform:
            return ORJSONResponse(
                {
                    "msg": {
                        "eng": "First word has no Part-of-Speech tag. Use the form 'word:pos'",
                        "swe": "Grundformen måste förses med ordklass (grundform:ordklass).",
                    }
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return result


@router.get("/xml/{words}", response_model=list[str])
async def get_para_xml(
    request: Request,
    words: str,
    paradigms: Paradigms = Depends(deps.get_paradigms),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        templates = request.app.state.templates
        try:
            _baseform, result = paradigms.query(words)
        except NoPartOfSpeechOnBaseform:
            return templates.TemplateResponse(
                request=request,
                name="paradigms.xml",
                status_code=status.HTTP_400_BAD_REQUEST,
                context={
                    "j": [],
                    "no_pos": True,
                },
            )

        return templates.TemplateResponse(
            request=request,
            name="paradigms.xml",
            context={
                "j": result,
                "no_pos": False,
            },
        )


@router.get("/html", response_class=HTMLResponse, name="paradigms:para-html")
async def paradigm_html(
    request: Request,
    words: str | None = None,
    paradigms: Paradigms = Depends(deps.get_paradigms),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        templates = request.app.state.templates
        if words is None:
            return templates.TemplateResponse(
                request=request,
                name="saldo_paradigms.html",
                context=templating.build_context(
                    request=request,
                    title="Paradigm",
                    input=words,
                    j=[],
                    no_pos=False,
                    w="",
                ),
            )
        title = f"Paradigm | {words}" if words else "Paradigm"
        try:
            baseform, _result = paradigms.query(words)
        except NoPartOfSpeechOnBaseform:
            baseform = words.split(",")[0]
            return templates.TemplateResponse(
                request=request,
                name="saldo_paradigms.html",
                status_code=status.HTTP_400_BAD_REQUEST,
                context=templating.build_context(
                    request=request,
                    title=title,
                    input=words,
                    j=[],
                    no_pos=True,
                    w=baseform,
                ),
            )


@router.get(
    "/html/{words}",
    response_class=HTMLResponse,
)
async def para_html_orig(
    request: Request,
    words: str,
):
    redirect_url = request.url_for("paradigms:para-html").include_query_params(words=words)
    return RedirectResponse(redirect_url)
