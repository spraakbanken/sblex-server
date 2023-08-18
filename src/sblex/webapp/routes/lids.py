import logging
from typing import Any, Union
from typing_extensions import Annotated

from asgi_matomo.trackers import PerfMsTracker
from fastapi import APIRouter, Depends, Path, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from sblex import formatting
from sblex.application.queries import LookupLid
from sblex.application.queries.lookup_lid import LemmaNotFound, LexemeNotFound
from sblex.application.predicates import is_lemma, is_lexeme
from sblex.webapp import deps, templating
from sblex.webapp.responses import XMLResponse
from sblex.webapp.schemas import Lemma, Lexeme

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/json/{lid}", response_model=None)
async def lookup_lid_json(
    request: Request,
    lid: Annotated[
        str,
        Path(
            title="Lid",
        ),
    ],
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
    # response_model=None,
) -> Response | None | dict[str, Any]:
    if not is_lemma(lid) and not is_lexeme(lid):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": f"{lid} is neither a lemma or a lexeme"},
        )
    with PerfMsTracker(scope=request.scope, key="pf_srv"):
        lemma_or_lexeme = await lookup_lid.get_by_lid(lid)
    return lemma_or_lexeme


@router.get(
    "/xml/{lid}",
    response_class=XMLResponse,
)
async def lookup_lid_xml(
    request: Request,
    lid: str,
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
):
    if not is_lemma(lid) and not is_lexeme(lid):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": f"{lid} is neither a lemma or a lexeme"},
        )
    templates = request.app.state.templates

    try:
        with PerfMsTracker(scope=request.scope, key="pf_srv"):
            lemma_or_lexeme = await lookup_lid.get_by_lid(lid)
    except LemmaNotFound:
        lemma_or_lexeme = {}
    except LexemeNotFound:
        lemma_or_lexeme = {}

    # if isinstance(lid, Lemma):
    if is_lemma(lid):
        return templates.TemplateResponse(
            "saldo_lid_lemma.xml",
            {"request": request, "j": lemma_or_lexeme},
            media_type="application/xml",
        )
    return templates.TemplateResponse(
        "saldo_lid_lexeme.xml",
        {"request": request, "j": lemma_or_lexeme},
        media_type="application/xml",
    )


@router.get("/html/{lid}", response_class=HTMLResponse, name="lids:lid-html")
async def lookup_lid_html(
    request: Request,
    lid: str,  # Union[Lexeme, Lemma],
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
):
    if not is_lemma(lid) and not is_lexeme(lid):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": f"{lid} is neither a lemma or a lexeme"},
        )
    templates = request.app.state.templates
    print(f"{lid=}")
    try:
        lemma_or_lexeme = await lookup_lid.get_by_lid(lid)
    except LemmaNotFound:
        return templates.TemplateResponse(
            "saldo_lid_lemma_saknas.html",
            context=templating.build_context(
                request, title=lid, service="lid", show_bar=False, lid=lid
            ),
        )
        # {
        #     "request": request,
        #     "bar": False,
        #     "title": lid,
        #     "lid": lid,
        #     "tracking_base_url": settings["tracking.matomo.frontend.base_url"],
        #     "tracking_site_id": settings["tracking.matomo.frontend.site_id"],
        # },
    except LexemeNotFound:
        return templates.TemplateResponse(
            "saldo_lid_lexeme_saknas.html",
            context=templating.build_context(
                request, title=lid, service="lid", show_bar=False, lid=lid
            ),
        )

    # if isinstance(lid, Lemma):
    if is_lemma(lid):
        return templates.TemplateResponse(
            "saldo_table.html",
            context=templating.build_context(
                request,
                title=lid,
                service="lid",
                show_bar=False,
                lid=lid,
                j=lemma_or_lexeme,
            )
            # {
            #     "request": request,
            #     "bar": True,
            #     "title": lid,
            #     "j": lemma_or_lexeme,
            # },
        )

    prepared_json = await prepare_lexeme_json(
        lemma_or_lexeme, lexeme=lid, lookup_lid=lookup_lid
    )
    logger.info("prepared_json = %s", prepared_json)

    templates.env.globals["lemma"] = formatting.lemma
    return templates.TemplateResponse(
        "saldo_lid_lexeme.html",
        context=templating.build_context(
            request, title=lid, service="lid", show_bar=False, data=prepared_json
        )
        # {"request": request, "bar": True, "title": lid, "data": prepared_json},
    )


@router.get("/graph/{lid}", response_class=HTMLResponse, name="lids:lid-graph")
async def lookup_lid_graph(
    request: Request,
    lid: str,
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
):
    if not is_lemma(lid) and not is_lexeme(lid):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": f"{lid} is neither a lemma or a lexeme"},
        )
    _templates = request.app.state.templates

    raise NotImplementedError("lids:lid-graph")


async def prepare_lexeme_json(
    j: dict[str, Any], *, lexeme: str, lookup_lid: LookupLid
) -> dict[str, Any]:
    lem = "" if lexeme == "PRIM..1" else j["l"]
    sorted_pf = (
        "*"
        if lexeme == "PRIM..1"
        else await sort_children(j["pf"], "m", lookup_lid=lookup_lid)
    )
    return {
        "h1": formatting.prlex(j["lex"]),
        "depth": depth(j["lex"], j["path"]),
        "fm": lexeme_ref(j["fm"]),
        "fp": lexeme_ref(j["fp"]),
        "lem": lem,
        "lex": j["lex"],
        "l": list(j["l"]),
        "mf": j["mf"],
        "pf": j["pf"],
        "sorted_mf": await sort_children(j["mf"], "p", lookup_lid=lookup_lid),
        "sorted_pf": sorted_pf,
        "lexeme": lexeme,
    }


def depth(s, pths):
    return 0 if s == "PRIM..1" else len(pths) + 1


def lexeme_ref(lids: str) -> str | list[str]:
    return lids.split() if lids else "*"


async def sort_children(lexemes, mp, *, lookup_lid: LookupLid) -> Union[str, list]:
    if lexemes == []:
        return "*"
    children: dict[str, list] = {}
    for lexeme in lexemes:
        l_lookup = await lookup_lid.get_by_lid(lexeme)
        p = l_lookup["fp"] if mp == "p" else l_lookup["fm"]
        if p in children:
            children[p].append(lexeme)
        else:
            children[p] = [lexeme]
    xs = []
    if "PRIM..1" in children:
        prim_lexs = children["PRIM..1"]
        del children["PRIM..1"]
        xs = sorted(children.items())
        xs.insert(0, ("PRIM..1", prim_lexs))
    else:
        xs = sorted(children.items())
    return xs
