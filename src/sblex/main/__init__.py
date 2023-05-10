from sblex.main import telemetry
from sblex.main.bootstrap import bootstrap_app

__all__ = ["bootstrap_app", "telemetry"]
__version__ = "0.2.3"


def get_version() -> str:
    return __version__
