# Evaluation

## Ground truth

`examples/planted/ground_truth.json` (generated with the fixture by `scripts/make_planted.py`): 13 substantive planted changes, 5 editorial edits and 1 banner on the CC BY 4.0 legal code. Four substantive items are also internal defects of the planted copy and are scored in audit mode. Details and the full list: `examples/README.md`.

## Metrics (`python -m docaudit score`)

| Metric | Definition |
|---|---|
| recall | substantive items cited by at least one surviving finding (any severity; killed findings do not count). In audit mode the finding kind must be one of the item's `audit_kinds` |
| precision | among surviving findings of severity minor or higher: share that cite a substantive item. Findings on the banner are ignored; findings that cite nothing planted, or only an editorial item, count against precision; `info` findings are excluded |
| editorial_items_flagged | editorial items reported at minor or higher |
| skeptic_false_kills | substantive items whose only matching findings were killed by skeptics |
| quote_verifier.rejection_rate | rejected agent findings / agent findings, from the run's own verification log |

Matching is at paragraph level: a finding matches an item when it cites one of the item's paragraphs. This is deliberately lenient about wording and strict about location.

## Results so far

| Run | Mode | Recall | Precision | Source |
|---|---|---|---|---|
| No-LLM baseline: every changed alignment operation is a finding | diff | 1.00 (13/13) | 0.87 (13/15) | `examples/results/planted-diff-fixture/score-baseline.json` |
| No-LLM baseline: deterministic sweeps only | audit | 0.50 (2/4) | 1.00 (2/2) | `examples/results/planted-audit-fixture/score-baseline.json` |
| Claude, Python runner on the API | diff / audit | pending | pending | |
| Claude, Workflow runner (Claude Opus 5.5 agents, one run) | diff | 1.00 (13/13) | 1.00 (17/17) | `examples/results/planted-diff-claude-workflow/score.json` |
| Claude, Workflow runner | audit | pending | pending | |

The diff baseline already finds every planted change, because every textual change is an alignment operation; its two false positives are the spelling and serial-comma edits. What the agents must add in diff mode is judgement: keep recall at 1.00 while removing editorial noise, and explain and rate each change. In audit mode the sweeps catch the dangling reference and the numbering gap; the contradiction (P11) and the undefined term (P13) need reading.

The fixture runs (`score-fixture.json`) are not listed as results: the FakeLLM heuristics and the planted set were written by the same person, so those scores only show that scoring works end to end.

## Run the real evaluation

```bash
export ANTHROPIC_API_KEY=...            # or: ant auth login
export DOCAUDIT_MODEL=claude-opus-5-5

# Python runner, both modes, with a cost cap
python -m docaudit run --mode diff --a examples/planted/cc-by-4.0.txt --b examples/planted/cc-by-4.0-planted.txt \
  --run runs/planted-diff-claude --backend anthropic --max-cost-usd 5
python -m docaudit run --mode audit --a examples/planted/cc-by-4.0-planted.txt \
  --run runs/planted-audit-claude --backend anthropic --max-cost-usd 5

python -m docaudit score --run runs/planted-diff-claude --truth examples/planted/ground_truth.json --out runs/planted-diff-claude/score.json
python -m docaudit score --run runs/planted-audit-claude --truth examples/planted/ground_truth.json --out runs/planted-audit-claude/score.json
```

For the Workflow runner, see `workflow/README.md`; score its run directory the same way. To publish a run, copy `report.md`, `report.json`, `score.json` and (Python runner) `usage.json` into `examples/results/<run-name>/`; put the full run directory (agent outputs) into `release-assets/` as a zip and list it in `docs/RELEASE_ASSETS.md`.

One run is one sample. Before drawing conclusions, repeat each configuration at least three times and report the spread.
