from __future__ import annotations

import json

import requests


class BaseController:
    def __init__(self, base_url: str, auth_token: str | None = None, default_headers: dict[str, str] | None = None):
        self.base_url = base_url.rstrip("/")
        self.auth_token: str | None = auth_token
        self.default_headers = default_headers or {}
        self._session = requests.Session()

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _headers(self, *, content_type: bool = False, extra_headers: dict[str, str] | None = None) -> dict[str, str]:
        headers = dict(self.default_headers)
        token = self.auth_token
        if token:
            headers["X-Dm-Auth-Token"] = token
        if content_type:
            headers["Content-Type"] = "application/json"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    @staticmethod
    def _extract_data(payload: dict | list) -> dict | list:
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    @staticmethod
    def _response_json(response: requests.Response) -> dict | list:
        if not response.content:
            return {}
        try:
            return response.json()
        except UnicodeDecodeError, json.JSONDecodeError, ValueError:
            text = response.content.decode("utf-8", errors="replace")
            return {"raw": text}

    def _get(
        self,
        endpoint: str,
        params: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict:
        response = self._session.get(
            self._url(endpoint),
            headers=self._headers(extra_headers=headers),
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return self._response_json(response)

    def _post(
        self,
        endpoint: str,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict[str, str] | None = None,
        files: dict[str, bytes] | None = None,
    ) -> dict:
        request_headers = self._headers(content_type=files is None, extra_headers=headers)
        response = self._session.post(
            self._url(endpoint),
            headers=request_headers,
            params=params,
            json=data if files is None else None,
            files=files,
            timeout=30,
        )
        response.raise_for_status()
        return self._response_json(response)

    def _put(
        self,
        endpoint: str,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict:
        response = self._session.put(
            self._url(endpoint),
            headers=self._headers(content_type=True, extra_headers=headers),
            params=params,
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return self._response_json(response)

    def _patch(self, endpoint: str, data: dict | None = None, headers: dict[str, str] | None = None) -> dict:
        response = self._session.patch(
            self._url(endpoint),
            headers=self._headers(content_type=True, extra_headers=headers),
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return self._response_json(response)

    def _delete(
        self,
        endpoint: str,
        params: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict | None:
        response = self._session.delete(
            self._url(endpoint),
            headers=self._headers(extra_headers=headers),
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        if response.content:
            return self._response_json(response)
        return None
