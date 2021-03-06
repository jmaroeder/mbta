import sys

import singletons
from requests_toolbelt.sessions import BaseUrlSession

from mbta.config import Config


@singletons.GlobalFactory
def config() -> Config:
    """Return the global config object."""
    return Config()


@singletons.GlobalFactory
def mbta_session() -> BaseUrlSession:
    """Return a requests.Session object for accessing the MBTA API."""
    cfg = config()
    session = BaseUrlSession(cfg.api_root)
    if cfg.api_key:
        session.headers.update({"x-api-key": cfg.api_key})
    return session


class _Shared(singletons.SharedModule):
    globals = globals()  # noqa: WPS125, WPS421


sys.modules[__name__] = _Shared()
