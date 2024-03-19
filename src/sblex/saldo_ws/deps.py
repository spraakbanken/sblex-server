from unittest import mock

import httpx
from fastapi import Depends, Request
from sblex.application.queries import FullformLexQuery, FullformQuery, LookupLid
from sblex.application.queries.inflection import InflectionTableQuery
from sblex.application.services import LookupService
from sblex.fm import Morphology
from sblex.fm.fm_runner import FmRunner
from sblex.infrastructure.queries import LookupFullformLexQuery
from sblex.infrastructure.queries.fm_runner_inflection import FmRunnerInflectionTable
from sblex.infrastructure.queries.http_morpology import HttpMorphology


def get_fm_client(request: Request) -> httpx.AsyncClient:
    return request.app.state._fm_client


def get_morphology(
    fm_client: httpx.AsyncClient = Depends(get_fm_client),  # noqa: B008
) -> Morphology:
    return HttpMorphology(http_client=fm_client)


def get_lookup_lid(request: Request) -> LookupLid:
    return request.app.state._lookup_lid


def get_fm_runner(request: Request) -> FmRunner:
    return request.app.state._fm_runner


def get_inflection_table_query(
    fm_runner: FmRunner = Depends(get_fm_runner),  # noqa: B008
) -> InflectionTableQuery:
    return FmRunnerInflectionTable(fm_runner=fm_runner)


def get_lookup_service(
    morphology: Morphology = Depends(get_morphology),  # noqa: B008
    lookup_lid: LookupLid = Depends(get_lookup_lid),  # noqa: B008
    inflection_table_query: InflectionTableQuery = Depends(get_inflection_table_query),  # noqa: B008
) -> LookupService:
    return LookupService(
        morphology=morphology, lookup_lid=lookup_lid, inflection_table=inflection_table_query
    )


def get_fullform_query() -> FullformQuery:
    query = mock.Mock(spec=FullformQuery)
    query.query = mock.Mock(return_value=b'{"c":"a"}')
    return query


def get_fullform_lex_query(
    lookup_service: LookupService = Depends(get_lookup_service),  # noqa: B008
) -> FullformLexQuery:
    return LookupFullformLexQuery(lookup_service=lookup_service)
