# Design

## Principles

1. **Agents propose, code disposes.** A model may claim anything; a finding counts only after code has found every quoted piece of evidence in the cited paragraph.
2. **Deterministic first.** Ingest, alignment, cross-reference resolution, numbering checks, verification, merging, coverage, aggregation and the report are plain Python. Agents get small, precise inputs and are judged by code afterwards.
3. **Skeptics get the last word.** Every surviving finding is reviewed by an agent whose only job is to refute it. The editor that runs afterwards can reorder and summarise, never add, upgrade or resurrect.
4. **Nothing is silently dropped.** Rejected findings, refuted findings, low-confidence findings, agent failures and budget stops all appear in the report with their reason.
5. **One file contract, two runners.** The Python runner and the Claude Code Workflow script write the same `agents/*.json` files and call the same deterministic stages. A test runs both on the same input and requires identical output.

## Pipeline

| Stage | Kind | Input | Output |
|---|---|---|---|
| prepare | code | documents | `docs/`, `alignment.json`, `sweeps.json`, `chunks/`, `index.md`, `plan.json` |
| section readers (one per chunk) | LLM | `chunks/cNN.md` | `agents/reader-cNN.json` |
| cross-reference checker | LLM | `index.md` + full documents | `agents/crossref.json` |
| verify | code | all reader, checker and gap outputs + sweeps | `verified.json`, `gaps.md`, skeptic batches |
| gap reader (diff mode, if coverage < 100%) | LLM | `gaps.md` | `agents/gap.json`, then verify again |
| skeptics (one per batch, `--skeptic-votes` each) | LLM | `skeptic/bNN.md` + full documents | `agents/skeptic-bNN-vK.json` |
| recheck-prep | code | skeptics' `missed` lists | `verified_missed.json`, `skeptic/r01.*` |
| recheck skeptic | LLM | `skeptic/r01.md` | `agents/recheck-r01-vK.json` |
| aggregate | code | findings + all verdicts | `aggregated.json`, `editor_input.md` |
| editor | LLM | `editor_input.md` | `agents/editor.json` |
| report | code | everything above | `report.md`, `report.json` |

## Ingest

Blank-line blocks become paragraphs; decoration lines (`=====`) are dropped; Markdown headings, bullets and code fences are split out; PDF text blocks come from PyMuPDF. Headings and numbered clauses open sections (`Section 1 -- Definitions.`, `0. Definitions.`, or a top-level `0. This License applies ...` clause). Ids are sequential (`p0001`, ...) and a pure function of the file bytes. Each paragraph also carries a fingerprint of its loose-normalised text, which is independent of line wrapping, typographic quotes and line-break hyphenation.

## Alignment (diff mode)

1. Paragraphs whose fingerprints are unique in both versions are anchor candidates; the longest increasing subsequence of those pairs becomes the anchor set.
2. Between anchors, a monotone dynamic programme pairs paragraphs, maximising the sum of `similarity - 0.3` over kept pairs. Similarity is `difflib` ratio over word tokens, behind a token-set Jaccard prefilter.
3. Leftover A and B paragraphs with similarity >= 0.75 are paired as moves.
4. The rest are insertions and deletions. Operations are ordered by position in B.

Section pairs are derived from the paragraph pairs. Chunks for section readers group consecutive B sections with at least one changed operation, up to about 12,000 characters, and show unchanged paragraphs only as one-line context.

## Deterministic sweeps

- **Cross-references**: `Section 6(b)`, `Sections 1, 5, 6, 7, and 8`, `Section 3(a)(1)(A)(i)` are resolved against the document's own section numbers and its list-item tree (nesting by the column where item text starts, which handles right-aligned roman numerals). Only a missing section or a missing first-level item becomes a finding; deeper misses are listed in the index for the cross-reference checker.
- **Numbering**: per section and nesting level, digits, letters and roman numerals must increase by one; section numbers too.
- **Index only**: defined terms (`X means`, `"X" refers to`, `("X")`) and numeric expressions.

In diff mode only problems that A does not already have are reported, so a pre-existing defect is not blamed on the edit.

## Roles and schemas

All schemas are in `docaudit/schemas.py` and use only the subset that structured outputs accept: every object has `additionalProperties: false` and every property required; ranges such as `0 <= confidence <= 1` are enforced in code.

| Role | Output | Default effort |
|---|---|---|
| section_reader | `{findings[], coverage_note}` | medium |
| cross_reference_checker | `{findings[], coverage_note}` | high |
| gap_reader | `{findings[], coverage_note}` | medium |
| skeptic | `{verdicts[], missed[]}` | high |
| editor | `{executive_summary, themes[], ordered_finding_ids[]}` | medium |

A finding is `{kind, title, description, severity, confidence, evidence: [{doc, para_id, quote}]}`. Kinds: `added`, `removed`, `changed`, `moved` (diff) and `contradiction`, `inconsistent_value`, `broken_reference`, `undefined_term`, `ambiguity`, `omission`, `other` (audit; diff mode also allows the first four of these for defects an edit introduced). A verdict is `{finding_id, verdict: upheld | weakened | refuted, reason, suggested_severity, counter_evidence[]}`.

## Quote verifier

| Match level | Rule |
|---|---|
| exact | substring of the paragraph after whitespace collapse (re-wrapping is never a fabrication) |
| normalized | substring after NFKC, ASCII folding of quotes and dashes, removal of soft and line-break hyphens, case folding |
| elided | `...` joins verbatim segments of two or more words each, found in order |

A quote found in another paragraph of the same document is **re-attributed** to the nearest occurrence and flagged. Everything else rejects the whole finding:

| Code | Meaning |
|---|---|
| `schema_invalid` | the finding does not match the schema |
| `kind_not_allowed_in_<mode>_mode` | for example `added` in audit mode |
| `no_evidence` | empty evidence list |
| `unknown_document` | evidence cites a document that is not in the run |
| `quote_too_short` | under 6 characters after normalisation |
| `quote_not_found` | not in the document at any level; the report shows the longest common run as a fraction of the quote |
| `quote_in_other_doc_only` | the quote exists, but only in the other version |
| `added_text_present_in_A` | text quoted as added already occurs somewhere in A |
| `removed_text_present_in_B` | text quoted as removed still occurs somewhere in B |
| `changed_without_difference` | every quote of a "changed" claim occurs in both versions |
| `added_needs_B_evidence`, `removed_needs_A_evidence`, `changed_needs_both_sides`, `moved_needs_both_sides` | the evidence cannot show the claim |

The rejection rate (rejected agent findings / agent findings) is reported per run; deterministic sweep findings are counted separately.

## Merge

Accepted findings are clustered with union-find. Two findings are the same issue when they are in the same family (change kinds vs defect kinds), cite at least one common paragraph, and either their quoted spans in that paragraph intersect or their titles and descriptions share at least 35% of content words. A merged finding keeps the union of evidence, the most severe severity, and a noisy-OR of member confidences (each clipped to 0.05..0.95, result capped at 0.99). Ids (`F001`, ...) follow document order.

## Coverage, gaps and misses

In diff mode every non-equal alignment operation should be cited by at least one accepted finding. Coverage is reported for the first pass and after the gap reader. Uncovered operations go to the gap reader, which must either report each one or name it as editorial. Skeptics may also report `missed` issues; those are verified like any finding, attached to an existing finding when they duplicate one, and otherwise reviewed by a separate recheck skeptic. Missed findings reported during the recheck are not accepted, so the loop terminates.

## Aggregation

| Skeptic outcome | Status | Severity | Confidence |
|---|---|---|---|
| no verdicts (stage skipped or failed) | unreviewed | unchanged | x 0.8 |
| grounded refutations from a strict majority | killed (moved to an appendix) | n/a | n/a |
| any refutation or weakening, otherwise | downgraded | lowest severity a non-upholding skeptic suggests; a refutation that suggests nothing lower costs one level; "weakened" with "keep" (or the current severity) leaves it; a suggestion above the current severity counts as one level down, so skeptics never raise severity | x 0.6 |
| all upheld | upheld | unchanged | c + (1 - c) x 0.25 |

A "refuted" verdict without at least one verified counter-quote is treated as "weakened": an ungrounded refutation cannot kill a grounded finding. Skeptics can never raise severity. Findings below confidence 0.25 move to a low-confidence section.

## Editor constraints (checked in code)

Ids not among surviving findings are ignored and reported; refuted ids are ignored and reported; omitted ids are appended in code order; themes lose unknown ids; any double-quoted passage of four or more words in the summary is searched in the documents and flagged if absent.

## Runners

**Python runner** (`docaudit/pipeline.py`): a thread pool (default 4 workers) per stage; per-call retries with exponential backoff and deterministic jitter for transient errors, invalid JSON and schema mismatches (the retry prompt carries the validation errors); `max_tokens` doubles on truncation up to 64,000; authentication errors and refusals are not retried, and an authentication error stops all later calls. Token and cost caps are checked before each call against spent plus in-flight reservations; once a cap is hit no new call starts and the report is marked incomplete.

**Anthropic backend** (`docaudit/llm/anthropic_backend.py`): model from `--model` or `DOCAUDIT_MODEL`, credentials resolved by the SDK; structured outputs through `output_config.format`; `output_config.effort` per role; adaptive thinking; the full documents sent as a cache-controlled prefix block for the checker and skeptics; server-side refusal fallback on by default. Parameters an older SDK does not know are sent through `extra_body`.

**Workflow runner** (`workflow/document-audit.workflow.js`): see `workflow/README.md`.

## Where the method comes from

The design generalises three earlier multi-agent document reviews. Their inputs and outputs are not part of this repository, so they are described by method only:

- a **checklist audit of one long document**: parallel section readers, cross-document checkers, a deterministic term sweep, one synthesiser, and the rule that no critical finding is accepted until it is checked word for word against the source;
- a **diff of two long agreements**: finders per group of sections, an independent agent whose job was to refute each finding and to hunt for misses, and a re-check of whatever the refuter added; a provision present anywhere in the other document did not count as new;
- a **research pipeline** where researchers bound to a schema fed skeptic agents, and the synthesis sided with the skeptics on every disagreement.

What changed when turning them into code: the word-for-word check moved from a manual step into the verifier; "present anywhere in the other document" became the `added_text_present_in_A` / `removed_text_present_in_B` checks; the hunt for misses became a measured coverage loop; the skeptics' last word became an explicit aggregation table; and the refuter itself has to quote.

## Failure analysis

Failure modes the design targets, and the mechanism for each:

| Failure mode | Mechanism |
|---|---|
| A quote the model invented or "improved" | quote verifier; match level shown per evidence item |
| Right quote, wrong paragraph id | re-attribution, flagged in the report |
| "New clause" that already exists elsewhere in the old version | absence check over the whole other document |
| A reader silently skipping part of its chunk | coverage of changed operations, gap reader, `coverage_note` |
| Several agents reporting the same issue | merge by shared paragraph and intersecting quote spans |
| A plausible but wrong finding | skeptic verdicts with verified counter-evidence |
| An overconfident skeptic killing a real finding | ungrounded refutations cannot kill; kills need a strict majority |
| An editor that embellishes | the editor cannot change findings; its quotes are verified |
| A runaway bill | token and cost caps, no new calls once a cap is reached |

Defects found while building this repository, each now covered by a test:

- **Merge by title similarity was too weak.** Two agents reporting the same edit with differently worded titles ("Payment term doubled" vs "Value changed: thirty to sixty") and partly overlapping quotes stayed separate. Merging now also fires when the quoted spans intersect inside the paragraph (`tests/test_merge_aggregate.py::test_same_change_from_two_agents_is_merged`).
- **The planted-set generator re-wrapped only part of a paragraph**, which would have turned a whitespace-only edit into a real one. It showed up when inspecting the generated diff; a test now requires every changed operation to map to a ground-truth item and the whitespace, typography and hyphenation edits to produce none (`tests/test_align.py::test_planted_alignment_has_only_planted_differences`).
- **A minority refutation with "keep" left severity unchanged.** That made a refutation weaker than a "weakened" verdict; refutations now always cost at least one severity level (`tests/test_merge_aggregate.py::test_minority_refutation_downgrades`).
- **Missing credentials made every agent call fail one by one.** An authentication error now stops all later calls and marks the run incomplete (`tests/test_pipeline.py::test_auth_error_stops_all_later_calls`).
