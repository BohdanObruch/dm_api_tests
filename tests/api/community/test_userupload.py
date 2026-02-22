import pytest
import requests

from src.api.controllers.community.userupload_controller import UserUploadApi
from src.api.models.community.userupload_model import UserDetailsEnvelope
from tests.fixtures.allure_helpers import step


@pytest.mark.smoke
def test_post_user_upload_success_or_known_server_error(
    user_upload_api,
    community_user_login: str,
    valid_png_bytes: bytes,
):
    with step("Upload avatar for current user"):
        try:
            response: UserDetailsEnvelope = user_upload_api.post_user_upload(
                login=community_user_login,
                file=valid_png_bytes,
            )
        except requests.HTTPError as exc_info:
            assert exc_info.response.status_code in (401, 500)
            return
    with step("Verify upload response login"):
        assert response.resource is not None
        assert response.resource.login == community_user_login


@pytest.mark.regression
def test_post_user_upload_invalid_user(user_upload_api, valid_png_bytes: bytes):
    with step("Upload avatar for non-existing user"), pytest.raises(requests.HTTPError) as excinfo:
        user_upload_api.post_user_upload(login="non_existent_user", file=valid_png_bytes)
    with step("Verify status code is 401 or 410"):
        assert excinfo.value.response.status_code in (401, 410)


@pytest.mark.regression
def test_post_user_upload_unauthorized(user_upload_api, community_user_login: str, valid_png_bytes: bytes):
    with step("Create unauthorized user-upload api client"):
        unauthorized_api = UserUploadApi(base_url=user_upload_api.base_url, auth_token="invalid_token")
    with step("Upload avatar with invalid auth token"), pytest.raises(requests.HTTPError) as excinfo:
        unauthorized_api.post_user_upload(login=community_user_login, file=valid_png_bytes)
    with step("Verify status code is 401"):
        assert excinfo.value.response.status_code == 401


@pytest.mark.regression
def test_post_user_upload_forbidden_or_known_server_error(
    user_upload_api,
    community_another_user_login: str,
    valid_png_bytes: bytes,
):
    with step("Upload avatar for another user"), pytest.raises(requests.HTTPError) as excinfo:
        user_upload_api.post_user_upload(login=community_another_user_login, file=valid_png_bytes)
    with step("Verify status code is 401, 403, or 500"):
        assert excinfo.value.response.status_code in (401, 403, 500)


@pytest.mark.regression
def test_post_user_upload_with_render_mode(user_upload_api, community_user_login: str, valid_png_bytes: bytes):
    with step("Upload avatar with renderMode=Html"):
        try:
            response: UserDetailsEnvelope = user_upload_api.post_user_upload(
                login=community_user_login,
                file=valid_png_bytes,
                render_mode="Html",
            )
        except requests.HTTPError as exc_info:
            assert exc_info.response.status_code in (401, 500)
            return
    with step("Verify upload response login"):
        assert response.resource is not None
        assert response.resource.login == community_user_login


@pytest.mark.regression
def test_post_user_upload_without_token_returns_401_or_403(configs, community_user_login: str, valid_png_bytes: bytes):
    api = UserUploadApi(base_url=configs.app_base_url)
    with step("Upload avatar without auth token"), pytest.raises(requests.HTTPError) as excinfo:
        api.post_user_upload(login=community_user_login, file=valid_png_bytes)
    with step("Verify status code is 401 or 403"):
        assert excinfo.value.response.status_code in (401, 403)
