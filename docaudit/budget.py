"""Token and cost caps for the Python runner.

Caps are checked before every call against what has been spent plus what is
reserved by calls in flight, using an estimate of the input size and an
expected output size. Actual usage from the API replaces the reservation when
the call returns. A call that is already in flight can therefore overshoot a
cap by at most one response per worker; no new call starts once a cap is hit.
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass

from .llm.base import BudgetExceeded, FatalError, Usage

# USD per million tokens: (input, output, cache read). Cache writes are billed
# at 1.25x input. Source: Anthropic pricing as cached on 2026-11-03; check the
# current price list before relying on cost caps, or override with
# DOCAUDIT_PRICE_IN_PER_MTOK / DOCAUDIT_PRICE_OUT_PER_MTOK / DOCAUDIT_PRICE_CACHE_READ_PER_MTOK.
PRICES = {
    "claude-opus-5-5": (4.00, 20.00, 0.20),
    "claude-opus-5": (5.00, 25.00, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00, 0.10),
    "claude-sonnet-5": (2.00, 10.00, 0.20),
    "claude-haiku-5-5": (0.10, 0.50, 0.01),
    "claude-fable-5-2": (8.00, 40.00, 0.20),
}


def price_for(model: str | None) -> tuple[float, float, float] | None:
    pin = os.environ.get("DOCAUDIT_PRICE_IN_PER_MTOK")
    pout = os.environ.get("DOCAUDIT_PRICE_OUT_PER_MTOK")
    if pin and pout:
        pcr = os.environ.get("DOCAUDIT_PRICE_CACHE_READ_PER_MTOK")
        return float(pin), float(pout), float(pcr) if pcr else float(pin) * 0.1
    if model is None:
        return None
    return PRICES.get(model)


def cost_usd(usage: Usage, price: tuple[float, float, float] | None) -> float:
    if price is None:
        return 0.0
    pin, pout, pcr = price
    return (usage.input_tokens * pin + usage.output_tokens * pout + usage.cache_read_tokens * pcr
            + usage.cache_write_tokens * pin * 1.25) / 1_000_000


@dataclass
class _Reservation:
    input_tokens: int
    output_tokens: int
    cost: float


class Budget:
    def __init__(self, max_input_tokens: int | None = None, max_output_tokens: int | None = None,
                 max_cost_usd: float | None = None, model: str | None = None, expected_output_tokens: int = 4000,
                 price: tuple[float, float, float] | None = None) -> None:
        self.max_input = max_input_tokens
        self.max_output = max_output_tokens
        self.max_cost = max_cost_usd
        self.price = price if price is not None else price_for(model)
        if max_cost_usd is not None and self.price is None:
            raise FatalError(f"no price known for model {model!r}: set DOCAUDIT_PRICE_IN_PER_MTOK and DOCAUDIT_PRICE_OUT_PER_MTOK to use a cost cap")
        self.expected_output = expected_output_tokens
        self.lock = threading.Lock()
        self.spent = Usage()
        self.spent_cost = 0.0
        self.pending: list[_Reservation] = []
        self.calls = 0
        self.exhausted: str | None = None

    def _pending(self) -> tuple[int, int, float]:
        return (sum(r.input_tokens for r in self.pending), sum(r.output_tokens for r in self.pending),
                sum(r.cost for r in self.pending))

    def reserve(self, est_input_tokens: int) -> _Reservation:
        est_out = self.expected_output
        est_cost = cost_usd(Usage(est_input_tokens, est_out), self.price)
        with self.lock:
            if self.exhausted:
                raise BudgetExceeded(self.exhausted)
            pi, po, pc = self._pending()
            if self.max_input is not None and self.spent.input_tokens + pi + est_input_tokens > self.max_input:
                raise BudgetExceeded(f"input token cap {self.max_input} would be exceeded")
            if self.max_output is not None and self.spent.output_tokens + po + est_out > self.max_output:
                raise BudgetExceeded(f"output token cap {self.max_output} would be exceeded")
            if self.max_cost is not None and self.spent_cost + pc + est_cost > self.max_cost:
                raise BudgetExceeded(f"cost cap ${self.max_cost:.2f} would be exceeded")
            r = _Reservation(est_input_tokens, est_out, est_cost)
            self.pending.append(r)
            return r

    def release(self, r: _Reservation) -> None:
        with self.lock:
            if r in self.pending:
                self.pending.remove(r)

    def commit(self, r: _Reservation, usage: Usage) -> float:
        c = cost_usd(usage, self.price)
        with self.lock:
            if r in self.pending:
                self.pending.remove(r)
            self.spent.input_tokens += usage.input_tokens
            self.spent.output_tokens += usage.output_tokens
            self.spent.cache_read_tokens += usage.cache_read_tokens
            self.spent.cache_write_tokens += usage.cache_write_tokens
            self.spent_cost += c
            self.calls += 1
            if self.max_cost is not None and self.spent_cost >= self.max_cost:
                self.exhausted = f"cost cap ${self.max_cost:.2f} reached"
            if self.max_output is not None and self.spent.output_tokens >= self.max_output:
                self.exhausted = f"output token cap {self.max_output} reached"
            if self.max_input is not None and self.spent.input_tokens >= self.max_input:
                self.exhausted = f"input token cap {self.max_input} reached"
        return c

    def totals(self) -> dict:
        return {
            "calls": self.calls,
            "input_tokens": self.spent.input_tokens,
            "output_tokens": self.spent.output_tokens,
            "cache_read_tokens": self.spent.cache_read_tokens,
            "cache_write_tokens": self.spent.cache_write_tokens,
            "cost_usd": round(self.spent_cost, 6),
            "caps": {"input_tokens": self.max_input, "output_tokens": self.max_output, "cost_usd": self.max_cost},
            "priced": self.price is not None,
        }
