from typing import Any

import jinja2
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sblex import main


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


def init_template_engine(settings: main.Settings) -> Jinja2Templates:
    templates = Jinja2Templates(directory="templates")
    templates.env.globals["url_for"] = custom_url_for
    return templates


@jinja2.pass_context
def custom_url_for(context: dict, name: str, **path_params) -> str:
    request = context["request"]
    http_url = request.url_for(name, **path_params)
    return http_url
