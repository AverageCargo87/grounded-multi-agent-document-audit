"""Anthropic Messages API backend with structured outputs.

* Model from ``--model`` or the ``DOCAUDIT_MODEL`` environment variable. The
  key is never handled here: the SDK resolves ``ANTHROPIC_API_KEY`` (or an
  ``ant auth login`` profile) itself.
* Every role answers through ``output_config.format`` (JSON schema), so the
  response is schema-valid JSON; the runner still validates it.
* ``output_config.effort`` per role, adaptive thinking, and the document text
  sent as a cache-controlled prefix block for roles that read whole documents.
* Server-side refusal fallback (``fallbacks: "default"``) is on by default;
  set ``DOCAUDIT_FALLBACKS=off`` to disable it.
* Older SDKs that do not know a parameter get it through ``extra_body``.
"""

from __future__ import annotations

import inspect
import json
import os

from .base import AuthError, FatalError, LLMRequest, LLMResponse, RefusalError, RetryableError, Usage

FALLBACK_BETA = "server-side-fallback-2026-07-01"
NON_STREAMING_MAX_TOKENS = 16000


class MaxTokensError(RetryableError):
    """The response hit max_tokens; retry with a larger limit."""


class AnthropicBackend:
    name = "anthropic"

    def __init__(self, model: str | None = None, client=None, timeout: float = 600.0) -> None:
        self.model = model or os.environ.get("DOCAUDIT_MODEL")
        if not self.model:
            raise FatalError("no model configured: pass --model or set DOCAUDIT_MODEL (for example claude-opus-5-5)")
        if client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover - depends on environment
                raise FatalError("the anthropic package is not installed: pip install anthropic") from exc
            try:
                client = anthropic.Anthropic(timeout=timeout, max_retries=2)
            except Exception as exc:  # for example no credentials configured
                raise FatalError(f"could not create the Anthropic client: {exc}") from exc
        self.client = client
        fb = os.environ.get("DOCAUDIT_FALLBACKS", "default").strip()
        self.fallbacks = None if fb.lower() in ("", "off", "none", "0") else fb
        self.thinking = os.environ.get("DOCAUDIT_THINKING", "adaptive").strip().lower()
        self._native = self._native_params()

    def _native_params(self) -> set[str]:
        try:
            params = inspect.signature(self.client.messages.create).parameters
        except (TypeError, ValueError):
            return set()
        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()):
            return {"output_config", "thinking"}
        return {n for n in ("output_config", "thinking") if n in params}

    def build_kwargs(self, req: LLMRequest) -> dict:
        if req.prefix:
            content = [
                {"type": "text", "text": req.prefix, "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": req.prompt},
            ]
        else:
            content = req.prompt
        kwargs: dict = {
            "model": self.model,
            "max_tokens": req.max_tokens,
            "system": req.system,
            "messages": [{"role": "user", "content": content}],
        }
        extra_body: dict = {}
        extra_headers: dict = {}
        output_config: dict = {"format": {"type": "json_schema", "schema": req.schema}}
        if req.effort:
            output_config["effort"] = req.effort
        if "output_config" in self._native:
            kwargs["output_config"] = output_config
        else:
            extra_body["output_config"] = output_config
        if self.thinking not in ("off", "omit", "none", ""):
            thinking = {"type": self.thinking}
            if "thinking" in self._native:
                kwargs["thinking"] = thinking
            else:
                extra_body["thinking"] = thinking
        if self.fallbacks:
            extra_headers["anthropic-beta"] = FALLBACK_BETA
            extra_body["fallbacks"] = self.fallbacks
        if extra_body:
            kwargs["extra_body"] = extra_body
        if extra_headers:
            kwargs["extra_headers"] = extra_headers
        return kwargs

    def _send(self, kwargs: dict):
        if kwargs["max_tokens"] > NON_STREAMING_MAX_TOKENS:
            with self.client.messages.stream(**kwargs) as stream:
                return stream.get_final_message()
        return self.client.messages.create(**kwargs)

    def complete(self, req: LLMRequest) -> LLMResponse:
        kwargs = self.build_kwargs(req)
        try:
            import anthropic
        except ImportError:  # a test client without the SDK installed
            anthropic = None
        try:
            msg = self._send(kwargs)
        except Exception as exc:
            if isinstance(exc, TypeError) and "authentication" in str(exc).lower():
                raise AuthError(f"no Anthropic credentials found: {exc}") from exc
            if anthropic is None:
                raise
            if isinstance(exc, (anthropic.AuthenticationError, anthropic.PermissionDeniedError)):
                raise AuthError(f"{type(exc).__name__}: {exc}") from exc
            if isinstance(exc, (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError)):
                raise RetryableError(f"{type(exc).__name__}: {exc}") from exc
            if isinstance(exc, anthropic.APIStatusError):
                if exc.status_code in (408, 409, 429) or exc.status_code >= 500:
                    raise RetryableError(f"HTTP {exc.status_code}: {exc}") from exc
                raise FatalError(f"HTTP {exc.status_code}: {exc}") from exc
            raise
        stop = getattr(msg, "stop_reason", None)
        if stop == "refusal":
            details = getattr(msg, "stop_details", None)
            category = getattr(details, "category", None) if details is not None else None
            raise RefusalError(f"model refused (category: {category})")
        if stop == "max_tokens":
            raise MaxTokensError(f"response hit max_tokens={req.max_tokens}")
        text = "".join(getattr(b, "text", "") for b in msg.content if getattr(b, "type", None) == "text")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RetryableError(f"response is not valid JSON: {exc}") from exc
        u = msg.usage
        usage = Usage(
            input_tokens=getattr(u, "input_tokens", 0) or 0,
            output_tokens=getattr(u, "output_tokens", 0) or 0,
            cache_read_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
            cache_write_tokens=getattr(u, "cache_creation_input_tokens", 0) or 0,
        )
        return LLMResponse(data=data, usage=usage, model=getattr(msg, "model", self.model), stop_reason=stop)
