from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urljoin

import pytest

from mbta.shared import config

if TYPE_CHECKING:
    from requests_mock import Mocker


@pytest.fixture
def mock_api(requests_mock: "Mocker") -> "Mocker":
    cfg = config()
    for data_file in (Path(__file__).parent / "data/mock_api").iterdir():
        requests_mock.get(f"{urljoin(cfg.api_root, data_file.name)}", text=data_file.read_text())
        # requests_mock.get(f"{cfg.api_root}/{data_file.name}", text="")

    return requests_mock
