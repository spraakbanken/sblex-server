import sys

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, ORJSONResponse
from opentelemetry import trace
from pydantic.dataclasses import dataclass

from sblex.application import queries
from sblex.application.queries.inflection import InflectionTableQuery
from sblex.sblex_server import deps, schemas, templating
from sblex.sblex_server.responses import XMLResponse

router = APIRouter()


@router.get(
    "/json/{paradigm}/{word}",
    name="inflections:gen-json",
    response_model=list[schemas.InflectionRow],
    responses={404: {"model": schemas.Message}},
)
async def inflection_table_json(
    paradigm: str,
    word: str,
    inflection_table_query: InflectionTableQuery = Depends(deps.get_inflection_table_query),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        inflections = inflection_table_query.query(paradigm, word)
        if len(inflections) == 0:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": f"paradigm '{paradigm}' finns ej"},
            )
        return ORJSONResponse(inflections)


@router.get("/xml/{paradigm}/{word}", name="inflections:gen-xml", response_class=XMLResponse)
async def inflection_table_xml(
    request: Request,
    paradigm: str,
    word: str,
    inflection_table_query: InflectionTableQuery = Depends(deps.get_inflection_table_query),  # noqa: B008
) -> XMLResponse:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        templates = request.app.state.templates
        json_data = inflection_table_query.query(paradigm, word)
        return templates.TemplateResponse(
            request=request,
            name="gen.xml",
            context={"j": json_data, "paradigm": paradigm},
            media_type="application/xml",
        )


@router.get("/html/{paradigm}/{word}", name="inflections:gen-html", response_class=HTMLResponse)
async def inflection_table_html(
    request: Request,
    paradigm: str,
    word: str,
    inflection_table_query: InflectionTableQuery = Depends(deps.get_inflection_table_query),  # noqa: B008
) -> HTMLResponse:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        json_data = inflection_table_query.query(paradigm, word)

        templates = request.app.state.templates
        if len(json_data) > 0:
            title = f'Böjningstabell | {json_data[0]["p"]} "{json_data[0]["gf"]}"'
            data = prepare_for_html(json_data)
        else:
            title = f"Böjningstabell | {paradigm} saknas"
            data = None
        return templates.TemplateResponse(
            request=request,
            name="gen.html",
            context=templating.build_context(
                request=request,
                title=title,
                paradigm=paradigm,
                word=word,
                data=data,
            ),
        )


@dataclass
class InflectionByMsd:
    msd: str
    value: str


@dataclass
class ParadigmWordData:
    pos: str
    inflections_by_msd: list[InflectionByMsd]
    inherent_features: str | None = None


def prepare_for_html(json_data: list[queries.InflectionTableRow]) -> ParadigmWordData:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        head_word = json_data[0]
        if len(head_word["inhs"]) > 0:
            inherent_features = ", ".join(head_word["inhs"])
        else:
            inherent_features = None
        forms_by_msd = group_msd(json_data)
        inflections_by_msd = collect_by_msd(json_data, forms_by_msd)

        return ParadigmWordData(
            pos=head_word["pos"],
            inherent_features=inherent_features,
            inflections_by_msd=inflections_by_msd,
        )


def group_msd(j: list[queries.InflectionTableRow]) -> dict[str, list[str]]:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        grouped_msd: dict[str, list[str]] = {}
        for x in j:
            msd = x["msd"]
            wf = x["form"]
            if msd in grouped_msd:
                grouped_msd[msd].append(wf)
            else:
                grouped_msd[msd] = [wf]
        return grouped_msd


def collect_by_msd(
    json_data: list[queries.InflectionTableRow], forms_by_msd: dict[str, list[str]]
) -> list[InflectionByMsd]:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        inflections_by_msd = []
        prev = ""
        for x in json_data:
            msd = x["msd"]
            if msd != prev:
                forms_by_msd[msd].reverse()
                inflections_by_msd.append(
                    InflectionByMsd(msd=msd, value="/".join(forms_by_msd[msd]))
                )
                prev = msd
        return inflections_by_msd
