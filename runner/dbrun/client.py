"""Sending System One requests to an endpoint.

The client sends one JSON body per request to `<base URL>/v1/systemone` with the API key as a Bearer token. The key
comes from an environment variable and is never written to disk or printed. Rate-limited and temporarily failing
requests are retried after the wait the endpoint asks for (`retry_after_ms`, or a `Retry-After` header), or after an
exponential backoff, whichever is longer.
"""

from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.request

RETRY_STATUSES = {408, 429, 500, 502, 503, 504}
MAX_WAIT_S = 60.0


def endpoint_url(base_url: str) -> str:
    url = base_url.rstrip("/")
    return url if url.endswith("/systemone") else url + "/v1/systemone"


def _wait_from(payload, headers) -> float | None:
    """The wait, in seconds, a rate-limited response asks for, if it says."""
    if isinstance(payload, dict):
        if isinstance(payload.get("retry_after_ms"), (int, float)):
            return payload["retry_after_ms"] / 1000
        if isinstance(payload.get("retry_after_sec"), (int, float)):
            return float(payload["retry_after_sec"])
    value = (headers or {}).get("Retry-After")
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None


class Client:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        extra_headers: dict[str, str] | None = None,
        timeout_s: float = 120.0,
        max_attempts: int = 10,
        key_header: str = "Authorization",
    ):
        """key_header: where the key goes. "Authorization" (the default) sends `Authorization: Bearer <key>`; any other
        name (for example "api-key", as Microsoft Foundry uses) sends the key as that header's value."""
        self.url = endpoint_url(base_url)
        auth = {"Authorization": f"Bearer {api_key}"} if key_header.lower() == "authorization" else {key_header: api_key}
        self._headers = {"Content-Type": "application/json", **(extra_headers or {}), **auth}
        self.timeout_s = timeout_s
        self.max_attempts = max_attempts

    def send(self, body: dict) -> dict:
        """Sends one request. Returns {outcome, status, answers, usage, model, error, attempts, ms}: outcome is `ok`
        when the response held answers, `error` otherwise."""
        data = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        started = time.monotonic()
        status, error, payload = None, None, None
        for attempt in range(1, self.max_attempts + 1):
            request = urllib.request.Request(self.url, data=data, headers=self._headers, method="POST")
            headers = {}
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                    status, headers = response.status, dict(response.headers)
                    payload = json.loads(response.read() or b"null")
            except urllib.error.HTTPError as e:
                status, headers = e.code, dict(e.headers or {})
                raw = e.read()
                try:
                    payload = json.loads(raw)
                except ValueError:
                    payload = {"detail": raw[:300].decode("utf-8", "replace")}
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                status, payload, error = None, None, f"network: {type(e).__name__}"
            if status == 200 and isinstance(payload, dict) and isinstance(payload.get("answers"), dict):
                return {
                    "outcome": "ok",
                    "status": 200,
                    "answers": payload["answers"],
                    "usage": payload.get("usage"),
                    "model": payload.get("model"),
                    "error": None,
                    "attempts": attempt,
                    "ms": round((time.monotonic() - started) * 1000),
                }
            asked = _wait_from(payload, headers)
            retry = status is None or status in RETRY_STATUSES or asked is not None
            if isinstance(payload, dict):
                error = str(payload.get("error") or payload.get("detail") or payload.get("message") or error)
            if status == 200:
                error, retry = "response held no answers", False
            if not retry or attempt == self.max_attempts:
                break
            # At least the wait the endpoint asks for, growing with each attempt so repeated limits back off.
            backoff = min(MAX_WAIT_S, 2 ** (attempt - 1))
            wait = max(asked, backoff) if asked is not None else backoff
            time.sleep(min(MAX_WAIT_S, wait) + random.uniform(0, 0.5))
        return {
            "outcome": "error",
            "status": status,
            "answers": None,
            "usage": None,
            "model": None,
            "error": error,
            "attempts": attempt,
            "ms": round((time.monotonic() - started) * 1000),
        }
