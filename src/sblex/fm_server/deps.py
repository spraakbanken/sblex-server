from fastapi import Request

from sblex.fm import Morphology


def get_morphology(request: Request) -> Morphology:
    return request.app.state._morph
