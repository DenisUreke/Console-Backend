from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
import json
import time
import urllib.parse
import urllib.request
import urllib.error


@dataclass(frozen=True)
class ApiOk:
    status_code: int
    url: str
    data: Any                 # Parsed JSON (dict/list)
    elapsed_ms: int


@dataclass(frozen=True)
class ApiErr:
    status_code: Optional[int]
    url: str
    error_type: str           # "http", "timeout", "network", "json", "unknown"
    message: str
    body: Optional[str] = None
    elapsed_ms: Optional[int] = None


ApiResult = Union[ApiOk, ApiErr]


class ApiCaller:
    """
    Generic HTTP JSON caller.
    - Builds URL from base + path + query params
    - Executes request
    - Parses JSON
    - Returns ApiOk / ApiErr
    """

    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 6.0,
        default_headers: Optional[Dict[str, str]] = None,
        min_interval_seconds: float = 0.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.default_headers = default_headers or {
            "Accept": "application/json",
            "User-Agent": "Console-Backend/1.0",
        }
        self.min_interval_seconds = float(min_interval_seconds)
        self._last_call_ts: float = 0.0

    def build_url(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        path = "/" + path.lstrip("/")
        url = f"{self.base_url}{path}"

        if params:
            # Drop None values and stringify everything
            clean: Dict[str, str] = {}
            for k, v in params.items():
                if v is None:
                    continue
                if isinstance(v, (list, tuple)):
                    # Common convention: comma-separated list
                    clean[k] = ",".join(str(x) for x in v if x is not None)
                else:
                    clean[k] = str(v)

            query = urllib.parse.urlencode(clean, doseq=False)
            url = f"{url}?{query}"

        return url

    def get_json(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ApiResult:
        url = self.build_url(path, params=params)
        return self.get_json_url(url=url, headers=headers)

    def get_json_url(self, url: str, headers: Optional[Dict[str, str]] = None) -> ApiResult:
        # Simple client-side rate limiting (useful for APIs that throttle)
        now = time.time()
        dt = now - self._last_call_ts
        if self.min_interval_seconds > 0 and dt < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - dt)

        start = time.perf_counter()
        final_headers = dict(self.default_headers)
        if headers:
            final_headers.update(headers)

        req = urllib.request.Request(url, headers=final_headers, method="GET")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                status = getattr(resp, "status", None) or 200
                raw = resp.read().decode("utf-8", errors="replace")

            elapsed_ms = int((time.perf_counter() - start) * 1000)
            self._last_call_ts = time.time()

            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                return ApiErr(
                    status_code=status,
                    url=url,
                    error_type="json",
                    message=f"Failed to parse JSON: {e}",
                    body=raw[:2000],
                    elapsed_ms=elapsed_ms,
                )

            return ApiOk(status_code=status, url=url, data=data, elapsed_ms=elapsed_ms)

        except urllib.error.HTTPError as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            body = None
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            return ApiErr(
                status_code=getattr(e, "code", None),
                url=url,
                error_type="http",
                message=str(e),
                body=(body[:2000] if body else None),
                elapsed_ms=elapsed_ms,
            )

        except urllib.error.URLError as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            msg = str(getattr(e, "reason", e))
            # URLError covers DNS, refused, etc. Timeout is often a socket.timeout inside reason.
            if "timed out" in msg.lower():
                err_type = "timeout"
            else:
                err_type = "network"
            return ApiErr(
                status_code=None,
                url=url,
                error_type=err_type,
                message=msg,
                elapsed_ms=elapsed_ms,
            )

        except Exception as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return ApiErr(
                status_code=None,
                url=url,
                error_type="unknown",
                message=str(e),
                elapsed_ms=elapsed_ms,
            )
