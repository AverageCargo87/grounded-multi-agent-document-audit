# Release assets

Files too large or too detailed for the tracked tree live in `release-assets/` (git-ignored) and are meant to be attached to a GitHub release.

| File | Size | SHA-256 | Contents |
|---|---|---|---|
| `fixture-run-directories.zip` | 329,645 bytes | `da7c2df674c6ef4f7c66cd6d226c8d682cb4c29dc728efe9832a0bb092eb8947` | Full run directories of the three offline FakeLLM fixture runs (`planted-diff-fixture`, `planted-audit-fixture`, `gpl-v2-v3-fixture`): ingested documents, alignment, chunks, every `agents/*.json`, `verified.json`, skeptic batches, `aggregated.json`, `usage.json`, reports. `workflow_args.json` is excluded because it holds absolute local paths. Rebuild with `python scripts/reproduce_results.py`, which writes the same directories under `runs/`. |

Planned: one zip per real model run (Python runner and Workflow runner, diff and audit on the planted set, diff on GPL-2.0 vs GPL-3.0), with its `report.md`, `report.json` and score committed under `examples/results/`.
