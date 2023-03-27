from unittest import mock

from fastapi import Request
from sblex.application.queries import FullformLexQuery, LookupLid


def get_fullform_lex_query() -> FullformLexQuery:
    query = mock.Mock(spec=FullformLexQuery)
    query.query = mock.Mock(return_value=[])
    return query


def get_lookup_lid(request: Request) -> LookupLid:
    return request.app.state._lookup_lid
