from typing import Any

from fastapi import Request


def build_context(
    request: Request, *, title: str, service: str, show_bar: bool = True, **kwargs
) -> dict[str, Any]:
    settings = request.app.state.config
    return {
        "request": request,
        "bar": show_bar,
        "title": title,
        "tracking_base_url": settings["tracking.matomo.frontend.base_url"],
        "tracking_site_id": settings["tracking.matomo.frontend.site_id"],
        **kwargs,
    }
