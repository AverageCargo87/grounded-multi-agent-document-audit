"""End-to-end FakeLLM runs plus the runner's retry, budget and concurrency behaviour."""

import json
import types

import pytest

from conftest import CC, PLANTED, ROOT, fake_run
from docaudit import stages
from docaudit.budget import Budget, cost_usd
from docaudit.llm.anthropic_backend import AnthropicBackend, MaxTokensError
from docaudit.llm.base import FatalError, LLMRequest, LLMResponse, RefusalError, RetryableError, Usage
from docaudit.llm.fake import FakeBackend
from docaudit.pipeline import PythonRunner, RunnerConfig
from docaudit.runstore import Run
from docaudit.verify import DocIndex, check_quote

# ---------------------------------------------------------------- end to end


def test_fake_end_to_end_writes_every_stage(planted_diff_run):
    run = Run(planted_diff_run)
    for rel in ("plan.json", "docs/A.json", "docs/B.md", "alignment.json", "sweeps.json", "index.md", "chunks/c01.md",
                "verified.json", "gaps.md", "skeptic/b01.md", "verified_missed.json", "aggregated.json",
                "editor_input.md", "report.md", "report.json", "usage.json", "agents/crossref.json", "agents/editor.json"):
        assert run.exists(rel), rel
    rep = run.read_json("report.json")
    pipe = rep["pipeline"]
    assert rep["run"]["fixture"] is True and "Fixture run" in run.read_text("report.md")
    assert pipe["verification"]["rejected"] >= 1  # the fake injects a fabricated quote
    assert pipe["verification"]["evidence_relocated"] >= 1
    assert pipe["verification"]["evidence_match_levels"].get("normalized", 0) >= 1
    assert pipe["coverage"]["ratio"] > pipe["coverage_first_pass"]["ratio"]  # the gap reader added coverage
    assert pipe["skeptic"]["ungrounded_refutations"] >= 1
    assert len(rep["killed"]) >= 1 and all(f["status"] == "killed" for f in rep["killed"])


def test_every_surviving_quote_verifies_against_the_documents(planted_diff_run):
    run = Run(planted_diff_run)
    ix = DocIndex(run.docs)
    rep = run.read_json("report.json")
    for f in rep["findings"] + rep["low_confidence"]:
        for e in f["evidence"]:
            c = check_quote(ix, e["doc"], e["para_id"], e["quote"])
            assert c.ok and not c.relocated, (f["id"], e)
            assert f"{e['doc']}:{e['para_id']}" in rep["paragraphs"]


def test_gpl_fixture_exercises_rejection_and_recheck(gpl_diff_run):
    from docaudit.llm.fake import _FABRICATED_TAIL
    run = Run(gpl_diff_run)
    rep = run.read_json("report.json")
    pipe = rep["pipeline"]
    injected = sum(json.dumps(obj).count(_FABRICATED_TAIL) for _, obj in run.agent_outputs("*.json"))
    assert injected >= 3
    # every injected fabrication is rejected, and nothing else is
    assert pipe["verification"]["rejection_reasons"] == {"quote_not_found": injected}
    assert pipe["missed_verification"]["agent_findings"] >= 1
    assert any(any(s.endswith(":missed") for s in f["sources"]) for f in rep["findings"])


def test_concurrency_does_not_change_results(tmp_path):
    a = fake_run(tmp_path / "c1", "diff", CC, PLANTED, concurrency=1)
    b = fake_run(tmp_path / "c8", "diff", CC, PLANTED, concurrency=8)
    for r in (a, b):
        r.pop("run")
    assert a == b


# ---------------------------------------------------------------- retries and budgets


class Flaky:
    """Fails the first ``fail`` calls of one role, then behaves like FakeBackend."""

    name = "flaky"
    model = None

    def __init__(self, role, fail, error=RetryableError("overloaded")):
        self.inner = FakeBackend()
        self.role, self.fail, self.error = role, fail, error
        self.seen = 0

    def complete(self, req):
        if req.role == self.role and self.seen < self.fail:
            self.seen += 1
            raise self.error
        return self.inner.complete(req)


def prepared(tmp_path):
    run_dir = tmp_path / "run"
    stages.prepare(run_dir, "diff", CC, PLANTED, repo_dir=ROOT)
    return run_dir


def test_retry_with_backoff_then_success(tmp_path):
    run_dir = prepared(tmp_path)
    sleeps = []
    runner = PythonRunner(run_dir, Flaky("editor", 2), config=RunnerConfig(retries=3, base_delay=1.0), sleep=sleeps.append, log=lambda m: None)
    runner.run()
    rec = next(c for c in runner.calls if c["label"] == "editor")
    assert rec["ok"] and rec["attempts"] == 3
    assert len(sleeps) == 2 and 1.0 <= sleeps[0] <= 1.5 and 2.0 <= sleeps[1] <= 2.5
    assert Run(run_dir).exists("agents/editor.json")


def test_retries_exhausted_is_recorded_and_report_still_built(tmp_path):
    run_dir = prepared(tmp_path)
    runner = PythonRunner(run_dir, Flaky("cross_reference_checker", 99), config=RunnerConfig(retries=2), sleep=lambda s: None, log=lambda m: None)
    rep = runner.run()
    assert not Run(run_dir).exists("agents/crossref.json")
    fails = rep["pipeline"]["agent_failures"]
    assert any(f["agent"] == "crossref" and "gave up after 3" in f["error"] for f in fails)
    assert rep["findings"]


def test_fatal_error_is_not_retried(tmp_path):
    run_dir = prepared(tmp_path)
    backend = Flaky("editor", 5, error=RefusalError("model refused"))
    runner = PythonRunner(run_dir, backend, sleep=lambda s: pytest.fail("must not sleep"), log=lambda m: None)
    runner.run()
    assert backend.seen == 1
    assert any(f["agent"] == "editor" and "RefusalError" in f["error"] for f in runner.failures)


def test_auth_error_stops_all_later_calls(tmp_path):
    from docaudit.llm.base import AuthError
    run_dir = prepared(tmp_path)
    backend = Flaky("section_reader", 99, error=AuthError("no credentials"))
    runner = PythonRunner(run_dir, backend, config=RunnerConfig(concurrency=1), log=lambda m: None)
    rep = runner.run()
    assert backend.seen == 1 and "stopped calling the API" in rep["pipeline"]["incomplete"]
    assert not list((run_dir / "agents").glob("*.json"))


class SchemaOnce(FakeBackend):
    name = "schema-once"

    def __init__(self):
        self.bad = True

    def complete(self, req):
        if req.role == "editor" and self.bad:
            self.bad = False
            return LLMResponse(data={"executive_summary": 3}, usage=Usage(10, 10))
        assert req.role != "editor" or "failed validation" in req.prompt
        return super().complete(req)


def test_schema_invalid_output_is_retried_with_the_errors(tmp_path):
    run_dir = prepared(tmp_path)
    runner = PythonRunner(run_dir, SchemaOnce(), sleep=lambda s: None, log=lambda m: None)
    runner.run()
    rec = next(c for c in runner.calls if c["label"] == "editor")
    assert rec["ok"] and rec["attempts"] == 2


class TruncatedThenInvalid(FakeBackend):
    """Editor: first answer hits max_tokens, second is schema-invalid, third is fine."""

    name = "truncated-then-invalid"

    def __init__(self):
        self.editor_max_tokens = []

    def complete(self, req):
        if req.role != "editor":
            return super().complete(req)
        self.editor_max_tokens.append(req.max_tokens)
        if len(self.editor_max_tokens) == 1:
            raise MaxTokensError("response hit max_tokens")
        if len(self.editor_max_tokens) == 2:
            return LLMResponse(data={"executive_summary": 3}, usage=Usage(10, 10))
        return super().complete(req)


def test_max_tokens_increase_survives_a_schema_retry(tmp_path):
    run_dir = prepared(tmp_path)
    backend = TruncatedThenInvalid()
    PythonRunner(run_dir, backend, sleep=lambda s: None, log=lambda m: None).run()
    assert backend.editor_max_tokens == [16000, 32000, 32000]
    assert Run(run_dir).exists("agents/editor.json")


def test_cli_run_exits_nonzero_when_the_run_is_incomplete(tmp_path, capsys):
    from docaudit.cli import main
    code = main(["run", "--mode", "diff", "--a", CC, "--b", PLANTED, "--run", str(tmp_path / "capped"),
                 "--backend", "fake", "--concurrency", "1", "--max-output-tokens", "4500"])
    assert code == 3
    assert "run incomplete" in capsys.readouterr().err
    assert Run(tmp_path / "capped").exists("report.md")  # the partial report is still written


def test_output_token_cap_stops_new_calls_and_flags_incomplete(tmp_path):
    run_dir = prepared(tmp_path)
    budget = Budget(max_output_tokens=4500, expected_output_tokens=4000)
    runner = PythonRunner(run_dir, FakeBackend(), budget=budget, config=RunnerConfig(concurrency=1), log=lambda m: None)
    rep = runner.run()
    assert rep["pipeline"]["incomplete"] and "output token cap" in rep["pipeline"]["incomplete"]
    assert budget.spent.output_tokens <= 4500
    assert "**Incomplete**" in Run(run_dir).read_text("report.md")
    statuses = {f["status"] for f in rep["findings"] + rep["low_confidence"]}
    assert statuses == {"unreviewed"}  # skeptics never ran


def test_cost_cap_and_pricing():
    b = Budget(max_cost_usd=0.1, model="claude-opus-5-5")
    r = b.reserve(1000)
    b.commit(r, Usage(input_tokens=1000, output_tokens=200))
    assert b.totals()["cost_usd"] == pytest.approx((1000 * 4 + 200 * 20) / 1e6)
    with pytest.raises(Exception, match="cost cap"):
        b.reserve(10_000)
    assert cost_usd(Usage(cache_read_tokens=1_000_000), (4.0, 20.0, 0.2)) == pytest.approx(0.2)
    with pytest.raises(FatalError):
        Budget(max_cost_usd=1.0, model="unknown-model")


# ---------------------------------------------------------------- Anthropic backend (mocked client)


class FakeMessages:
    def __init__(self, response):
        self.response = response
        self.kwargs = None

    def create(self, model, max_tokens, system, messages, extra_headers=None, extra_body=None):
        self.kwargs = dict(model=model, max_tokens=max_tokens, system=system, messages=messages,
                           extra_headers=extra_headers, extra_body=extra_body)
        return self.response


def message(text, stop="end_turn"):
    return types.SimpleNamespace(
        content=[types.SimpleNamespace(type="thinking", thinking=""), types.SimpleNamespace(type="text", text=text)],
        stop_reason=stop, stop_details=types.SimpleNamespace(category="cyber"), model="test-model",
        usage=types.SimpleNamespace(input_tokens=1200, output_tokens=300, cache_read_input_tokens=1000, cache_creation_input_tokens=0))


def request(prefix=None):
    return LLMRequest(role="skeptic", label="skeptic-b01-v1", mode="diff", system="sys", prompt="batch",
                      schema={"type": "object"}, prefix=prefix, effort="high")


def backend_with(resp, monkeypatch, **env):
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    msgs = FakeMessages(resp)
    return AnthropicBackend(client=types.SimpleNamespace(messages=msgs)), msgs


def test_anthropic_request_shape(monkeypatch):
    backend, msgs = backend_with(message('{"verdicts": [], "missed": []}'), monkeypatch, DOCAUDIT_MODEL="model-from-env")
    resp = backend.complete(request(prefix="DOCS"))
    k = msgs.kwargs
    assert k["model"] == "model-from-env" and k["system"] == "sys"
    assert k["extra_body"]["output_config"] == {"format": {"type": "json_schema", "schema": {"type": "object"}}, "effort": "high"}
    assert k["extra_body"]["thinking"] == {"type": "adaptive"} and k["extra_body"]["fallbacks"] == "default"
    assert k["extra_headers"]["anthropic-beta"].startswith("server-side-fallback")
    blocks = k["messages"][0]["content"]
    assert blocks[0] == {"type": "text", "text": "DOCS", "cache_control": {"type": "ephemeral"}}
    assert resp.data == {"verdicts": [], "missed": []} and resp.usage.cache_read_tokens == 1000


def test_anthropic_fallbacks_can_be_disabled(monkeypatch):
    backend, msgs = backend_with(message("{}"), monkeypatch, DOCAUDIT_MODEL="m", DOCAUDIT_FALLBACKS="off")
    backend.complete(request())
    assert "fallbacks" not in msgs.kwargs["extra_body"] and not msgs.kwargs["extra_headers"]


def test_anthropic_stop_reasons_and_bad_json(monkeypatch):
    monkeypatch.setenv("DOCAUDIT_MODEL", "m")
    with pytest.raises(RefusalError, match="cyber"):
        backend_with(message("{}", stop="refusal"), monkeypatch)[0].complete(request())
    with pytest.raises(MaxTokensError):
        backend_with(message("{", stop="max_tokens"), monkeypatch)[0].complete(request())
    with pytest.raises(RetryableError, match="not valid JSON"):
        backend_with(message("not json"), monkeypatch)[0].complete(request())


def test_anthropic_requires_a_model(monkeypatch):
    monkeypatch.delenv("DOCAUDIT_MODEL", raising=False)
    with pytest.raises(FatalError, match="DOCAUDIT_MODEL"):
        AnthropicBackend(client=types.SimpleNamespace(messages=FakeMessages(None)))


def test_no_key_or_model_is_hard_coded():
    src = (ROOT / "docaudit" / "llm" / "anthropic_backend.py").read_text(encoding="utf-8")
    assert "sk-ant" not in src and "api_key" not in src
    assert '"claude-' not in src
    assert json.loads(json.dumps({"ok": True}))
