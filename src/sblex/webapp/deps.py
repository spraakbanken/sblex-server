from unittest import mock

from fastapi import Depends, Request
from sblex.application.queries import FullformLexQuery, FullformQuery, LookupLid
from sblex.application.services import LookupService
from sblex.fm import Morphology
from sblex.infrastructure.queries import LookupFullformLexQuery


def get_morphology(request: Request) -> Morphology:
    return request.app.state._morph


def get_lookup_lid(request: Request) -> LookupLid:
    return request.app.state._lookup_lid


def get_lookup_service(
    morphology: Morphology = Depends(get_morphology),  # noqa: B008
    lookup_lid: LookupLid = Depends(get_lookup_lid),  # noqa: B008
) -> LookupService:
    return LookupService(morphology=morphology, lookup_lid=lookup_lid)


def get_fullform_query() -> FullformQuery:
    query = mock.Mock(spec=FullformQuery)
    query.query = mock.Mock(return_value=b'{"c":"a"}')
    return query


def get_fullform_lex_query(
    lookup_service: LookupService = Depends(get_lookup_service),  # noqa: B008
) -> FullformLexQuery:
    return LookupFullformLexQuery(lookup_service=lookup_service)
