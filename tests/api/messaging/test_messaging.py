import pytest
import requests

from src.api.controllers.messaging.messaging_controller import MessagingApi
from src.api.models.messaging.messaging_model import ConversationListEnvelope
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_get_conversations_returns_list(messaging_api: MessagingApi):
    with step("Get conversations with page size 10"):
        response = messaging_api.get_conversations(size=10)
    with step("Verify conversations response type and resources"):
        assert isinstance(response, ConversationListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_visavi_conversation_not_exists_returns_410(messaging_api: MessagingApi):
    with step("Request visavi conversation for non-existing user"), pytest.raises(requests.HTTPError) as exc_info:
        messaging_api.get_visavi_conversation(login="non_existent_user_12345")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_messages_from_not_existing_conversation_returns_410(messaging_api: MessagingApi):
    with step("Request messages for non-existing conversation"), pytest.raises(requests.HTTPError) as exc_info:
        messaging_api.get_messages(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_message_not_exists_returns_410(messaging_api: MessagingApi):
    with step("Request non-existing message by id"), pytest.raises(requests.HTTPError) as exc_info:
        messaging_api.get_message(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_message_not_exists_returns_501_or_410(messaging_api: MessagingApi):
    with step("Delete non-existing message by id"), pytest.raises(requests.HTTPError) as exc_info:
        messaging_api.delete_message(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410 or 501"):
        assert exc_info.value.response.status_code in (410, 501)


@pytest.mark.regression
def test_get_messages_requires_valid_conversation_id(messaging_api: MessagingApi):
    with step("Request messages with invalid conversation id format"), pytest.raises(requests.HTTPError):
        messaging_api.get_messages(id="not-a-uuid")
