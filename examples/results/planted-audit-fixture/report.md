# Document audit report: planted-audit-fixture

> **Fixture run.** Produced by the scripted FakeLLM test backend, not by a language model. It exercises every pipeline stage on real documents; the findings and verdicts are heuristic placeholders and say nothing about model quality.

| | |
|---|---|
| Mode | audit |
| Document A | `examples/planted/cc-by-4.0-planted.txt` (80 paragraphs, sha256 `c6e691013a77`) |
| Runner / backend | python / fake |

## Pipeline

| Stage | Result |
|---|---|
| Section-reader chunks | 2 |
| Findings emitted by agents | 4 |
| Rejected by the quote verifier | 0 (0.0%) |
| Deterministic sweep findings | 2 |
| Evidence match levels (accepted) | exact 4; re-attributed 0 |
| Findings after merge | 3 |
| Skeptic 'missed' findings | 0 reported, 0 rejected, 0 duplicates attached |
| Skeptic verdicts | 3 (upheld 2, weakened 1); ungrounded refutations 1 |
| Final status | downgraded 1, upheld 2 |
| LLM calls / tokens / cost | 7 calls, 28889 in, 637 out, $0.0000 |

## Summary

3 findings survived quote verification and the skeptic stage (2 major, 1 info). The first to read is F003: Cross-reference to a non-existent target: Section 9(a). Its evidence reads "Section 9(a)". 0 findings were refuted by skeptics and 0 are low-confidence.

- **broken_reference (1)**: F003
- **undefined_term (1)**: F001
- **omission (1)**: F002

## Findings (3)

major: 2, info: 1

### F003 [major] broken_reference: Cross-reference to a non-existent target: Section 9(a)

Confidence 0.98 (upheld). Reported by reader-c02, sweep.

The text refers to Section 9(a), but no Section 9 in this document.

- [A:p0065](#a-p0065) (exact): "Section 9(a)"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F001 [major] undefined_term: 'Granted Rights' is used like a defined term but is never defined

Confidence 0.88 (upheld). Reported by crossref, reader-c01.

The capitalised phrase 'Granted Rights' reads like a defined term, but no definition exists.

- [A:p0029](#a-p0029) (exact): "uthorizes You to exercise the Granted Rights in all media and formats whet"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F002 [info] omission: Numbering gap: item 3 is missing

Confidence 0.54 (downgraded, severity lowered from minor). Reported by crossref, sweep.

Item 4 follows the item before it, but 3 was expected; an item may have been deleted or the list renumbered incompletely.

- [A:p0050](#a-p0050) (exact): "2. You may satisfy the conditions in Section"
- [A:p0051](#a-p0051) (exact): "4. If You Share Adapted Material You produce,"
- Skeptic skeptic-b02-v1: **weakened** (said refuted). The numbering may be intentional.
  - note: ungrounded refutation: no verified counter-evidence, treated as weakened

## Cited paragraphs

<a id="a-p0029"></a>**A:p0029** (Section 2 -- Scope.)

> 4. Media and formats; technical modifications allowed. The Licensor authorizes You to exercise the Granted Rights in all media and formats whether now known or hereafter created, and to make technical modifications necessary to do so. The Licensor waives and/or agrees not to assert any right or authority to forbid You from making technical modifications necessary to exercise the Licensed Rights, including technical modifications necessary to circumvent Effective Technological Measures. For purposes of this Public License, simply making modifications authorized by this Section 2(a) (4) never produces Adapted Material.

<a id="a-p0050"></a>**A:p0050** (Section 3 -- License Conditions.)

> 2. You may satisfy the conditions in Section 3(a)(1) in any reasonable manner based on the medium, means, and context in which You Share the Licensed Material. For example, it may be reasonable to satisfy the conditions by providing a URI or hyperlink to a resource that includes the required information.

<a id="a-p0051"></a>**A:p0051** (Section 3 -- License Conditions.)

> 4. If You Share Adapted Material You produce, the Adapter's License You apply must not prevent recipients of the Adapted Material from complying with this Public License.

<a id="a-p0065"></a>**A:p0065** (Section 6 -- Term and Termination.)

> b. Where Your right to use the Licensed Material has terminated under Section 9(a), it reinstates:
