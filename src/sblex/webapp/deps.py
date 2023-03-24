from sblex.application.queries import FullformLexQuery
from unittest import mock


def get_fullform_lex_query() -> FullformLexQuery:
    query = mock.Mock(spec=FullformLexQuery)
    query.query = mock.Mock(return_value=[])
    return query
