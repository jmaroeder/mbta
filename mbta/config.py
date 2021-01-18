from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class."""

    api_key: Optional[str] = None
    api_root: str = "https://api-v3.mbta.com/"
