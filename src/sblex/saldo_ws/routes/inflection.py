import sys

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, ORJSONResponse
from opentelemetry import trace
from pydantic.dataclasses import dataclass
from sblex.application.queries.inflection import InflectionTableQuery
from sblex.saldo_ws import deps, schemas, templating

router = APIRouter()


@router.get(
    "/json/{paradigm}/{word}",
    response_model=list[schemas.InflectionRow],
    response_class=ORJSONResponse,
    name="inflections:gen-json",
)
async def inflection_table_json(
    paradigm: str,
    word: str,
    inflection_table_query: InflectionTableQuery = Depends(deps.get_inflection_table_query),  # noqa: B008
):
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        return ORJSONResponse(inflection_table_query.query(paradigm, word))


@router.get(
    "/html/{paradigm}/{word}",
    response_model=list[schemas.InflectionRow],
    response_class=ORJSONResponse,
    name="inflections:gen-html",
)
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
            title = f'{json_data[0]["p"]} "{json_data[0]["gf"]}"'
            data = prepare_for_html(json_data, word=word, paradigm=paradigm)
        else:
            title = f'{paradigm} "{word}"'
            data = None
        return templates.TemplateResponse(
            request=request,
            name="saldo_gen.html",
            context=templating.build_context(
                request=request,
                title=title,
                service="gen",
                show_bar=False,
                paradigm=paradigm,
                data=data,
            ),
        )


@dataclass
class InflectionByMsd:
    msd: str
    value: str


@dataclass
class ParadigmWord:
    word: str
    paradigm: str
    pos: str
    inflections_by_msd: list[InflectionByMsd]
    inherent_features: str | None = None


def prepare_for_html(json_data: list[dict], *, word: str, paradigm: str) -> ParadigmWord:
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

        return ParadigmWord(
            word=word,
            paradigm=paradigm,
            pos=head_word["pos"],
            inherent_features=inherent_features,
            inflections_by_msd=inflections_by_msd,
        )


def group_msd(j: list[dict]) -> dict[str, list[str]]:
    with trace.get_tracer(__name__).start_as_current_span(
        sys._getframe().f_code.co_name
    ) as _process_api_span:
        grouped_msd = {}
        for x in j:
            msd = x["msd"]
            wf = x["form"]
            if msd in grouped_msd:
                grouped_msd[msd].append(wf)
            else:
                grouped_msd[msd] = [wf]
        return grouped_msd


def collect_by_msd(
    json_data: list[dict], forms_by_msd: dict[str, list[str]]
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
