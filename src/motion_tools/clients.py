"""Provider clients for motion-control generation APIs.

These clients are designed to work with real vendor endpoints when credentials
and base URLs are supplied via environment variables.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any
from urllib import error, request


class MotionToolError(RuntimeError):
    """Raised when a provider API request fails."""


@dataclass(frozen=True)
class ProviderConfig:
    """Configuration required to call a provider endpoint."""

    base_url: str
    api_key: str


def _post_json(url: str, payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise MotionToolError(f"POST {url} failed: {exc.code} {details}") from exc
    except error.URLError as exc:
        raise MotionToolError(f"POST {url} failed: {exc.reason}") from exc


def _get_json(url: str, api_key: str) -> dict[str, Any]:
    req = request.Request(
        url,
        method="GET",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise MotionToolError(f"GET {url} failed: {exc.code} {details}") from exc
    except error.URLError as exc:
        raise MotionToolError(f"GET {url} failed: {exc.reason}") from exc


class WanAnimateClient:
    """Client wrapper for a Wan 2.7 Animate-style endpoint."""

    def __init__(self, config: ProviderConfig | None = None) -> None:
        cfg = config or ProviderConfig(
            base_url=os.getenv("WAN27_BASE_URL", ""),
            api_key=os.getenv("WAN27_API_KEY", ""),
        )
        if not cfg.base_url or not cfg.api_key:
            raise MotionToolError("WAN27_BASE_URL and WAN27_API_KEY are required.")
        self._cfg = cfg

    def create_job(
        self,
        prompt: str,
        image_url: str | None = None,
        motion_strength: float = 0.6,
        duration_seconds: int = 5,
    ) -> dict[str, Any]:
        payload = {
            "prompt": prompt,
            "image_url": image_url,
            "motion_strength": motion_strength,
            "duration_seconds": duration_seconds,
        }
        return _post_json(f"{self._cfg.base_url.rstrip('/')}/v1/animate", payload, self._cfg.api_key)

    def get_job(self, job_id: str) -> dict[str, Any]:
        return _get_json(f"{self._cfg.base_url.rstrip('/')}/v1/jobs/{job_id}", self._cfg.api_key)


class KlingMotionClient:
    """Client wrapper for a Kling 3.0 Motion Control-style endpoint."""

    def __init__(self, config: ProviderConfig | None = None) -> None:
        cfg = config or ProviderConfig(
            base_url=os.getenv("KLING30_BASE_URL", ""),
            api_key=os.getenv("KLING30_API_KEY", ""),
        )
        if not cfg.base_url or not cfg.api_key:
            raise MotionToolError("KLING30_BASE_URL and KLING30_API_KEY are required.")
        self._cfg = cfg

    def create_job(
        self,
        prompt: str,
        video_url: str | None = None,
        camera_control: str = "smooth-pan",
        motion_intensity: float = 0.5,
    ) -> dict[str, Any]:
        payload = {
            "prompt": prompt,
            "video_url": video_url,
            "camera_control": camera_control,
            "motion_intensity": motion_intensity,
        }
        return _post_json(f"{self._cfg.base_url.rstrip('/')}/v3/motion/control", payload, self._cfg.api_key)

    def get_job(self, job_id: str) -> dict[str, Any]:
        return _get_json(f"{self._cfg.base_url.rstrip('/')}/v3/jobs/{job_id}", self._cfg.api_key)
