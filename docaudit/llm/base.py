"""Backend interface for the Python runner."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class LLMRequest:
    role: str
    label: str
    mode: str
    system: str
    prompt: str
    schema: dict
    prefix: str | None = None  # stable document text, sent first so it can be prompt-cached
    context: dict = field(default_factory=dict)  # in-process data for test doubles; never sent to an API
    max_tokens: int = 16000
    effort: str | None = None


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0


@dataclass
class LLMResponse:
    data: dict
    usage: Usage
    model: str | None = None
    stop_reason: str | None = None


class LLMError(Exception):
    pass


class RetryableError(LLMError):
    """Transient: rate limit, overload, 5xx, connection, invalid JSON, schema mismatch."""


class FatalError(LLMError):
    """Not worth retrying: authentication, bad request, missing configuration."""


class AuthError(FatalError):
    """Credentials missing or rejected: no later call can succeed, so the run stops calling the API."""


class RefusalError(FatalError):
    """The model declined (stop_reason == 'refusal')."""


class BudgetExceeded(LLMError):
    """A token or cost cap would be exceeded by the next call."""


class Backend(Protocol):
    name: str
    model: str | None

    def complete(self, req: LLMRequest) -> LLMResponse: ...
