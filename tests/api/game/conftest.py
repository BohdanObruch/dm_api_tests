from __future__ import annotations

import pytest
from faker import Faker

from src.api.controllers.game.attributeschema_controller import AttributeSchemaController
from src.api.controllers.game.character_controller import CharacterApi
from src.api.controllers.game.comment_controller import CommentApi
from src.api.controllers.game.game_controller import GameApi
from src.api.controllers.game.post_controller import PostApi
from src.api.controllers.game.room_controller import RoomApi
from src.api.models.game.attributeschema_model import AttributeSpecificationType, SchemaType
from tests.fixtures.config import Config

fake = Faker()


@pytest.fixture(scope="function")
def game_api(configs: Config, auth_token: str) -> GameApi:
    return GameApi(base_url=configs.app_base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def room_api(configs: Config, auth_token: str) -> RoomApi:
    return RoomApi(base_url=configs.app_base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def post_api(configs: Config, auth_token: str) -> PostApi:
    return PostApi(base_url=configs.app_base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def comment_api(configs: Config, auth_token: str) -> CommentApi:
    return CommentApi(base_url=configs.app_base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def character_api(configs: Config, auth_token: str) -> CharacterApi:
    return CharacterApi(base_url=configs.app_base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def attribute_schema_api(configs: Config, auth_token: str) -> AttributeSchemaController:
    return AttributeSchemaController(base_url=configs.app_base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def valid_attribute_schema_payload() -> dict:
    return {
        "title": fake.sentence(nb_words=3),
        "type": SchemaType.Public.value,
        "specifications": [
            {
                "title": "Strength",
                "required": True,
                "type": AttributeSpecificationType.Number.value,
                "minValue": 1,
                "maxValue": 20,
            }
        ],
    }
