# Workflow runner (Claude Code)

`document-audit.workflow.js` runs the same roles as the Python runner, with the same schemas and the same role prompts, as a Claude Code Workflow script. It never runs more than **2 agents at a time** (a slot limiter inside the script, independent of the harness cap).

Workflow scripts cannot read files or import Python, so the division of labour is:

- **Role agents** (section readers, cross-reference checker, gap reader, skeptics, editor) read their input file from the run directory, write their answer to `agents/<label>.json`, run `python -m docaudit validate` on it until it prints `OK`, and return a small receipt.
- **Build steps** are low-effort agents that run exactly one `python -m docaudit ...` command (verify, recheck-prep, aggregate, report) and return its one-line JSON summary. All verification, merging, coverage, aggregation and reporting is deterministic Python; no model writes or edits those files.

The schemas and role prompts live between the `<generated:workflow-assets>` markers. They are generated from `docaudit/schemas.py` and `docaudit/prompts.py`; after changing either, run `python -m docaudit export-workflow-assets` (a test fails if the copy is stale).

## Run it

From the repository root:

```bash
python -m docaudit prepare --mode diff \
  --a examples/planted/cc-by-4.0.txt --b examples/planted/cc-by-4.0-planted.txt \
  --run runs/planted-diff-workflow --skeptic-batches 4
```

This writes the run directory and `runs/planted-diff-workflow/workflow_args.json` (absolute paths, chunk ids, batch count). Then, in a Claude Code session opened in the repository root, ask for the Workflow tool to run `workflow/document-audit.workflow.js` with `args` set to the JSON object in that file, for example:

> Run the workflow script workflow/document-audit.workflow.js with args = the contents of runs/planted-diff-workflow/workflow_args.json

The session needs permission for the agents to read and write files under `runs/` and to run `python -m docaudit ...` through Bash. If `python` is not the right interpreter, pass `--python <command>` to `prepare`.

## What it writes

| Phase | Files |
|---|---|
| Read, Cross-check | `agents/reader-cNN.json`, `agents/crossref.json` |
| Verify | `verified.json`, `gaps.md`, `gaps.json`, `skeptic/bNN.json` and `.md` |
| Gaps (diff mode) | `agents/gap.json`, then `verified.json` again |
| Skeptics | `agents/skeptic-bNN-v1.json` |
| Recheck | `verified_missed.json`, `skeptic/r01.*`, `agents/recheck-r01-v1.json` (only if the skeptics reported missed findings) |
| Edit | `aggregated.json`, `editor_input.md`, `agents/editor.json` |
| Report | `report.md`, `report.json` |

Score a finished run against the planted ground truth:

```bash
python -m docaudit score --run runs/planted-diff-workflow --truth examples/planted/ground_truth.json
```

For the planted diff the script starts 2 section readers, 1 cross-reference checker, at most 1 gap reader (only if coverage is below 100%), up to 4 skeptics (one per non-empty batch), at most 1 recheck skeptic and 1 editor, plus 4 or 5 build steps (verify, a second verify after the gap reader, recheck-prep, aggregate, report). The offline mock run of this case makes 14 calls: 9 agents and 5 build steps.

## Offline test

`tests/test_workflow_script.py` executes this exact script under Node with mocked `agent`, `parallel`, `phase` and `log` hooks: build steps run their commands, role agents are simulated by `python -m docaudit fake-agent`. The test asserts that at most 2 agents run at once, that the phases run in order, and that the resulting `report.json` and every `agents/*.json` file are identical to the Python runner's on an identically prepared run directory.
