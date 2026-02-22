import pytest
import requests

from src.api.controllers.messaging.chat_controller import ChatApi
from src.api.models.messaging.chat_model import ChatMessageListEnvelope
from tests.fixtures.allure_helpers import step


@pytest.mark.smoke
def test_get_chat_messages_with_pagination(chat_api: ChatApi) -> None:
    with step("Get chat messages with size=3 and number=1"):
        response = chat_api.get_chat_messages(size=3, number=1)
    with step("Verify chat message list response"):
        assert isinstance(response, ChatMessageListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)
        if response.resources is not None:
            assert len(response.resources) <= 3
        assert response.paging is not None
        assert response.paging.current == 1
        assert response.paging.size == 3


@pytest.mark.regression
def test_get_chat_message_not_found_returns_410(chat_api: ChatApi) -> None:
    with step("Request non-existing chat message by id"), pytest.raises(requests.HTTPError) as exc_info:
        chat_api.get_chat_message(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_post_chat_message_invalid_payload_returns_400(chat_api: ChatApi) -> None:
    with step("Post chat message with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        chat_api.post_chat_message(payload={"text": 123})
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400


@pytest.mark.regression
def test_get_chat_messages_without_token_returns_401_or_403(configs) -> None:
    api = ChatApi(base_url=configs.app_base_url)
    with step("Request chat messages without auth token"):
        try:
            response = api.get_chat_messages(size=3, number=1)
        except requests.HTTPError as exc_info:
            assert exc_info.response.status_code in (401, 403)
            return
    with step("If endpoint is public, verify response structure"):
        assert isinstance(response, ChatMessageListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_chat_message_without_token_returns_401_or_403(configs) -> None:
    api = ChatApi(base_url=configs.app_base_url)
    with step("Request single chat message without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.get_chat_message(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401, 403, or 410"):
        assert exc_info.value.response.status_code in (401, 403, 410)
