import logging
from typing import Any, Union

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from sblex import formatting
from sblex.application.queries import LookupLid
from sblex.application.queries.lookup_lid import LemmaNotFound, LexemeNotFound
from sblex.webapp import deps
from sblex.webapp.responses import XMLResponse
from sblex.webapp.schemas import Lemma, Lexeme

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/json/{lid}")
async def lookup_lid_json(
    lid: Union[Lexeme, Lemma],
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
):
    return lookup_lid.get_by_lid(lid)


@router.get(
    "/xml/{lid}",
    response_class=XMLResponse,
)
async def lookup_lid_xml(
    request: Request,
    lid: Union[Lexeme, Lemma],
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
):
    templates = request.app.state.templates

    try:
        lemma_or_lexeme = lookup_lid.get_by_lid(lid)
    except LemmaNotFound:
        lemma_or_lexeme = {}
    except LexemeNotFound:
        lemma_or_lexeme = {}

    if isinstance(lid, Lemma):
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
    lid: Union[Lexeme, Lemma],
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
):
    templates = request.app.state.templates

    try:
        lemma_or_lexeme = lookup_lid.get_by_lid(lid)
    except LemmaNotFound:
        return templates.TemplateResponse(
            "saldo_lid_lemma_saknas.html",
            context={"request": request, "bar": False, "title": lid, "lid": lid},
        )
    except LexemeNotFound:
        return templates.TemplateResponse(
            "saldo_lid_lexeme_saknas.html",
            context={"request": request, "bar": False, "title": lid, "lid": lid},
        )

    if isinstance(lid, Lemma):
        return templates.TemplateResponse(
            "saldo_lid_lemma.html",
            context={
                "request": request,
                "bar": True,
                "title": lid,
                "j": lemma_or_lexeme,
            },
        )

    prepared_json = prepare_lexeme_json(
        lemma_or_lexeme, lexeme=lid, lookup_lid=lookup_lid
    )
    logger.info("prepared_json = %s", prepared_json)

    templates.env.globals["lemma"] = formatting.lemma
    return templates.TemplateResponse(
        "saldo_lid_lexeme.html",
        context={"request": request, "bar": True, "title": lid, "data": prepared_json},
    )


@router.get("/graph/{lid}", response_class=HTMLResponse, name="lids:lid-graph")
async def lookup_lid_graph(
    request: Request,
    lid: Union[Lexeme, Lemma],
    lookup_lid: LookupLid = Depends(deps.get_lookup_lid),  # noqa: B008
):
    templates = request.app.state.templates

    raise NotImplementedError("lids:lid-graph")


def prepare_lexeme_json(
    j: dict[str, Any], *, lexeme: str, lookup_lid: LookupLid
) -> dict[str, Any]:
    lem = "" if lexeme == "PRIM..1" else j["l"]
    sorted_pf = (
        "*"
        if lexeme == "PRIM..1"
        else sort_children(j["pf"], "m", lookup_lid=lookup_lid)
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
        "sorted_mf": sort_children(j["mf"], "p", lookup_lid=lookup_lid),
        "sorted_pf": sorted_pf,
        "lexeme": lexeme,
    }


def depth(s, pths):
    return 0 if s == "PRIM..1" else len(pths) + 1


def lexeme_ref(lids: str) -> str | list[str]:
    return lids.split() if lids else "*"


def sort_children(lexemes, mp, *, lookup_lid: LookupLid) -> Union[str, list]:
    if lexemes == []:
        return "*"
    children = {}
    for l in lexemes:
        if mp == "p":
            p = lookup_lid.get_by_lid(l)["fp"]
        else:
            p = lookup_lid.get_by_lid(l)["fm"]
        if p in children:
            children[p].append(l)
        else:
            children[p] = [l]
    s = "<table>"
    xs = []
    if "PRIM..1" in children:
        prim_lexs = children["PRIM..1"]
        del children["PRIM..1"]
        xs = sorted(children.items())
        xs.insert(0, ("PRIM..1", prim_lexs))
    else:
        xs = sorted(children.items())
    return xs
