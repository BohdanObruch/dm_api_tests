import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    mail_hog_url: str

    @property
    def app_base_url(self) -> str:
        return self.base_url

    def __getitem__(self, item: str):
        return getattr(self, item)


@pytest.fixture(scope="session")
def configs() -> Config:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is not set in .env")
    return Config(
        base_url=base_url,
        mail_hog_url=os.getenv("MAIL_HOG_URL", ""),
    )
