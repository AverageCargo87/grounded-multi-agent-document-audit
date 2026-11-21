# Document diff report: planted-diff-fixture

> **Fixture run.** Produced by the scripted FakeLLM test backend, not by a language model. It exercises every pipeline stage on real documents; the findings and verdicts are heuristic placeholders and say nothing about model quality.

| | |
|---|---|
| Mode | diff |
| Document A | `examples/planted/cc-by-4.0.txt` (79 paragraphs, sha256 `fd3a263fe19e`) |
| Document B | `examples/planted/cc-by-4.0-planted.txt` (80 paragraphs, sha256 `c6e691013a77`) |
| Runner / backend | python / fake |
| Alignment | equal 65, modified 12, inserted 2, deleted 1, moved 1 |

## Pipeline

| Stage | Result |
|---|---|
| Section-reader chunks | 2 |
| Findings emitted by agents | 20 |
| Rejected by the quote verifier | 1 (5.0%) |
| Deterministic sweep findings | 2 |
| Evidence match levels (accepted) | exact 33, normalized 1; re-attributed 1 |
| Findings after merge | 17 |
| Changed operations cited by a finding | first pass 14/16 (87.5%); with gap reader 15/16 (93.8%) |
| Skeptic 'missed' findings | 0 reported, 0 rejected, 0 duplicates attached |
| Skeptic verdicts | 17 (refuted 2, upheld 11, weakened 4); ungrounded refutations 1 |
| Final status | downgraded 4, killed 2, upheld 11 |
| LLM calls / tokens / cost | 9 calls, 62005 in, 3435 out, $0.0000 |

## Summary

15 findings survived quote verification and the skeptic stage (11 major, 3 minor, 1 info). The first to read is F012: Cross-reference to a non-existent target: Section 9(a). Its evidence reads "Section 9(a)". 2 findings were refuted by skeptics and 0 are low-confidence.

- **broken_reference (1)**: F012
- **changed (9)**: F013, F014, F015, F006, F011, F016, F004, F002, F005
- **added (2)**: F001, F010
- **removed (1)**: F009
- **moved (1)**: F017
- **omission (1)**: F008

## Findings (15)

major: 11, minor: 3, info: 1

### F012 [major] broken_reference: Cross-reference to a non-existent target: Section 9(a)

Confidence 0.93 (upheld). Reported by sweep.

The text refers to Section 9(a), but no Section 9 in this document.

- [B:p0065](#b-p0065) (exact): "Section 9(a)"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F013 [major] changed: Value changed in Section 6 -- Term and Termination.: '6(a),' became '9(a),'

Confidence 0.91 (upheld). Reported by crossref, reader-c01.

Version A reads "6(a)," where version B reads "9(a),".

- [A:p0064](#a-p0064) (exact): "has terminated under Section 6(a), it reinstates:"
- [B:p0065](#b-p0065) (exact): "has terminated under Section 9(a), it reinstates:"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F014 [major] changed: Value changed in Section 6 -- Term and Termination.: '30' became '60'

Confidence 0.91 (upheld). Reported by crossref, reader-c01.

Version A reads "30" where version B reads "60".

- [A:p0065](#a-p0065) (exact): "it is cured within 30 days of Your discovery"
- [B:p0066](#b-p0066) (exact): "it is cured within 60 days of Your discovery"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F015 [major] changed: Value changed in Section 6 -- Term and Termination.: '6,' became '(nothing)'

Confidence 0.91 (upheld). Reported by crossref, reader-c01.

Version A reads "6," where version B reads "(nothing)".

- [A:p0069](#a-p0069) (exact): "d. Sections 1, 5, 6, 7, and 8 survive"
- [B:p0070](#b-p0070) (normalized): "D. SECTIONS 1, 5, 7, AND 8 SURVIVE TERMINATION"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F001 [major] added: New text in (front matter): EVALUATION FIXTURE. This file is a deliberately modified ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0001](#b-p0001) (exact): "EVALUATION FIXTURE. This file is a deliberately modified copy of the Creative"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F006 [major] changed: Wording changed in Section 2 -- Scope.: 'not' became '(nothing)'

Confidence 0.78 (upheld). Reported by reader-c01.

Version A reads "not" where version B reads "(nothing)".

- [A:p0031](#a-p0031) (exact): "downstream restrictions. You may not offer or impose any"
- [B:p0032](#b-p0032) (exact): "downstream restrictions. You may offer or impose any additional"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F009 [major] removed: Text removed from Section 3 -- License Conditions.: 3. If requested by the Licensor, You must ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0050](#a-p0050) (exact, re-attributed): "3. If requested by the Licensor, You must remove any of the"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F010 [major] added: New text in Section 3 -- License Conditions.: 5. If You Share the Licensed Material for ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0052](#b-p0052) (exact): "5. If You Share the Licensed Material for commercial purposes, You must"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F011 [major] changed: Wording changed in Section 4 -- Sui Generis Database Rights.: 'must' became 'should'

Confidence 0.78 (upheld). Reported by reader-c01.

Version A reads "must" where version B reads "should".

- [A:p0056](#a-p0056) (exact): "c. You must comply with the conditions"
- [B:p0057](#b-p0057) (exact): "c. You should comply with the conditions"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F016 [major] changed: Wording changed in Section 7 -- Other Terms and Conditions.: 'The Licensor' became 'You'

Confidence 0.78 (upheld). Reported by reader-c02.

Version A reads "The Licensor" where version B reads "You". 1 further edit(s) in the same paragraph.

- [A:p0071](#a-p0071) (exact): "a. The Licensor shall not be bound"
- [B:p0072](#b-p0072) (exact): "a. You shall not be bound"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F004 [major] changed: Cross-check: Value changed in Section 2 -- Scope.: 'specified in Section 6(a).' became 'five years from the date You accept it.'

Confidence 0.70 (upheld). Reported by crossref.

Version A reads "specified in Section 6(a)." where version B reads "five years from the date You accept it.".

- [A:p0027](#a-p0027) (exact): "this Public License is specified in Section 6(a)."
- [B:p0028](#b-p0028) (exact): "this Public License is five years from the date You accept it."
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F017 [minor] moved: Paragraph moved from Section 8 -- Interpretation. to Section 7 -- Other Terms and Conditions.

Confidence 0.39 (downgraded). Reported by reader-c02.

The same provision appears in a different place in version B.

- [A:p0077](#a-p0077) (exact): "d. Nothing in this Public License constitutes or may be interpreted as"
- [B:p0074](#b-p0074) (exact): "c. Nothing in this Public License constitutes or may be interpreted as"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0077](#a-p0077): "d. Nothing in this Public License constitutes or may be interpreted as"

### F002 [minor] changed: Wording changed in Section 1 -- Definitions.: 'translated, altered, arranged, transformed,' became 'translated'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "translated, altered, arranged, transformed," where version B reads "translated". 1 further edit(s) in the same paragraph.

- [A:p0010](#a-p0010) (exact): "the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in"
- [B:p0011](#b-p0011) (exact): "the Licensed Material is translated or altered in a"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0010](#a-p0010): "the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in"

### F005 [minor] changed: Wording changed in Section 2 -- Scope.: 'Licensed' became 'Granted'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "Licensed" where version B reads "Granted".

- [A:p0028](#a-p0028) (exact): "You to exercise the Licensed Rights in all media"
- [B:p0029](#b-p0029) (exact): "You to exercise the Granted Rights in all media"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0028](#a-p0028): "You to exercise the Licensed Rights in all media"

### F008 [info] omission: Numbering gap: item 3 is missing

Confidence 0.54 (downgraded, severity lowered from minor). Reported by crossref, sweep.

Item 4 follows the item before it, but 3 was expected; an item may have been deleted or the list renumbered incompletely.

- [B:p0050](#b-p0050) (exact): "2. You may satisfy the conditions in Section"
- [B:p0051](#b-p0051) (exact): "4. If You Share Adapted Material You produce,"
- Skeptic skeptic-b02-v1: **weakened** (said refuted). The numbering may be intentional.
  - note: ungrounded refutation: no verified counter-evidence, treated as weakened

## Refuted by skeptics (2)

### F003 [minor] changed: Wording changed in Section 1 -- Definitions.: 'communication,' became 'communication'

Confidence 0.60 (killed). Reported by reader-c01.

Version A reads "communication," where version B reads "communication".

- [A:p0018](#a-p0018) (exact): "public performance, distribution, dissemination, communication, or importation, and to"
- [B:p0019](#b-p0019) (exact): "public performance, distribution, dissemination, communication or importation, and to"
- Skeptic skeptic-b01-v1: **refuted**. Only spelling or punctuation differs between the versions; the meaning is unchanged.
  - counter-evidence [A:p0018](#a-p0018): "public performance, distribution, dissemination, communication, or importation, and to"
  - counter-evidence [B:p0019](#b-p0019): "public performance, distribution, dissemination, communication or importation, and to"

### F007 [minor] changed: Wording changed in Section 2 -- Scope.: 'licensed' became 'licenced'

Confidence 0.60 (killed). Reported by reader-c01.

Version A reads "licensed" where version B reads "licenced". 1 further edit(s) in the same paragraph.

- [A:p0035](#a-p0035) (exact): "trademark rights are not licensed under this Public License."
- [B:p0036](#b-p0036) (exact): "trademark rights are not licenced under this Public Licence."
- Skeptic skeptic-b02-v1: **refuted**. Only spelling or punctuation differs between the versions; the meaning is unchanged.
  - counter-evidence [A:p0035](#a-p0035): "trademark rights are not licensed under this Public License."
  - counter-evidence [B:p0036](#b-p0036): "trademark rights are not licenced under this Public Licence."

## Rejected by the quote verifier (1)

| Agent | Kind | Title | Reason |
|---|---|---|---|
| reader-c01 | changed | Wording changed in Section 2 -- Scope.: 'irrevocable' became 'revocable' | B:p0024 quote_not_found (longest common run 38% of quote) |

## Cited paragraphs

<a id="a-p0010"></a>**A:p0010** (Section 1 -- Definitions.)

> a. Adapted Material means material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material and in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission under the Copyright and Similar Rights held by the Licensor. For purposes of this Public License, where the Licensed Material is a musical work, performance, or sound recording, Adapted Material is always produced where the Licensed Material is synched in timed relation with a moving image.

<a id="a-p0018"></a>**A:p0018** (Section 1 -- Definitions.)

> i. Share means to provide material to the public by any means or process that requires permission under the Licensed Rights, such as reproduction, public display, public performance, distribution, dissemination, communication, or importation, and to make material available to the public including in ways that members of the public may access the material from a place and at a time individually chosen by them.

<a id="a-p0027"></a>**A:p0027** (Section 2 -- Scope.)

> 3. Term. The term of this Public License is specified in Section 6(a).

<a id="a-p0028"></a>**A:p0028** (Section 2 -- Scope.)

> 4. Media and formats; technical modifications allowed. The Licensor authorizes You to exercise the Licensed Rights in all media and formats whether now known or hereafter created, and to make technical modifications necessary to do so. The Licensor waives and/or agrees not to assert any right or authority to forbid You from making technical modifications necessary to exercise the Licensed Rights, including technical modifications necessary to circumvent Effective Technological Measures. For purposes of this Public License, simply making modifications authorized by this Section 2(a) (4) never produces Adapted Material.

<a id="a-p0031"></a>**A:p0031** (Section 2 -- Scope.)

> b. No downstream restrictions. You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient of the Licensed Material.

<a id="a-p0035"></a>**A:p0035** (Section 2 -- Scope.)

> 2. Patent and trademark rights are not licensed under this Public License.

<a id="a-p0050"></a>**A:p0050** (Section 3 -- License Conditions.)

> 3. If requested by the Licensor, You must remove any of the information required by Section 3(a)(1)(A) to the extent reasonably practicable.

<a id="a-p0056"></a>**A:p0056** (Section 4 -- Sui Generis Database Rights.)

> c. You must comply with the conditions in Section 3(a) if You Share all or a substantial portion of the contents of the database.

<a id="a-p0064"></a>**A:p0064** (Section 6 -- Term and Termination.)

> b. Where Your right to use the Licensed Material has terminated under Section 6(a), it reinstates:

<a id="a-p0065"></a>**A:p0065** (Section 6 -- Term and Termination.)

> 1. automatically as of the date the violation is cured, provided it is cured within 30 days of Your discovery of the violation; or

<a id="a-p0069"></a>**A:p0069** (Section 6 -- Term and Termination.)

> d. Sections 1, 5, 6, 7, and 8 survive termination of this Public License.

<a id="a-p0071"></a>**A:p0071** (Section 7 -- Other Terms and Conditions.)

> a. The Licensor shall not be bound by any additional or different terms or conditions communicated by You unless expressly agreed.

<a id="a-p0077"></a>**A:p0077** (Section 8 -- Interpretation.)

> d. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities that apply to the Licensor or You, including from the legal processes of any jurisdiction or authority.

<a id="b-p0001"></a>**B:p0001** ((front matter))

> EVALUATION FIXTURE. This file is a deliberately modified copy of the Creative Commons Attribution 4.0 International legal code, made to test document comparison tools. It is not a Creative Commons license and must not be used as one. The planted changes are listed in ground_truth.json.

<a id="b-p0011"></a>**B:p0011** (Section 1 -- Definitions.)

> a. Adapted Material means material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material and in which the Licensed Material is translated or altered in a manner requiring permission under the Copyright and Similar Rights held by the Licensor. For purposes of this Public License, where the Licensed Material is a musical work, performance, or sound recording, Adapted Material is always produced where the Licensed Material is synched in timed relation with a moving image.

<a id="b-p0019"></a>**B:p0019** (Section 1 -- Definitions.)

> i. Share means to provide material to the public by any means or process that requires permission under the Licensed Rights, such as reproduction, public display, public performance, distribution, dissemination, communication or importation, and to make material available to the public including in ways that members of the public may access the material from a place and at a time individually chosen by them.

<a id="b-p0028"></a>**B:p0028** (Section 2 -- Scope.)

> 3. Term. The term of this Public License is five years from the date You accept it.

<a id="b-p0029"></a>**B:p0029** (Section 2 -- Scope.)

> 4. Media and formats; technical modifications allowed. The Licensor authorizes You to exercise the Granted Rights in all media and formats whether now known or hereafter created, and to make technical modifications necessary to do so. The Licensor waives and/or agrees not to assert any right or authority to forbid You from making technical modifications necessary to exercise the Licensed Rights, including technical modifications necessary to circumvent Effective Technological Measures. For purposes of this Public License, simply making modifications authorized by this Section 2(a) (4) never produces Adapted Material.

<a id="b-p0032"></a>**B:p0032** (Section 2 -- Scope.)

> b. No downstream restrictions. You may offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient of the Licensed Material.

<a id="b-p0036"></a>**B:p0036** (Section 2 -- Scope.)

> 2. Patent and trademark rights are not licenced under this Public Licence.

<a id="b-p0050"></a>**B:p0050** (Section 3 -- License Conditions.)

> 2. You may satisfy the conditions in Section 3(a)(1) in any reasonable manner based on the medium, means, and context in which You Share the Licensed Material. For example, it may be reasonable to satisfy the conditions by providing a URI or hyperlink to a resource that includes the required information.

<a id="b-p0051"></a>**B:p0051** (Section 3 -- License Conditions.)

> 4. If You Share Adapted Material You produce, the Adapter's License You apply must not prevent recipients of the Adapted Material from complying with this Public License.

<a id="b-p0052"></a>**B:p0052** (Section 3 -- License Conditions.)

> 5. If You Share the Licensed Material for commercial purposes, You must notify the Licensor in writing at least 10 days in advance.

<a id="b-p0057"></a>**B:p0057** (Section 4 -- Sui Generis Database Rights.)

> c. You should comply with the conditions in Section 3(a) if You Share all or a substantial portion of the contents of the database.

<a id="b-p0065"></a>**B:p0065** (Section 6 -- Term and Termination.)

> b. Where Your right to use the Licensed Material has terminated under Section 9(a), it reinstates:

<a id="b-p0066"></a>**B:p0066** (Section 6 -- Term and Termination.)

> 1. automatically as of the date the violation is cured, provided it is cured within 60 days of Your discovery of the violation; or

<a id="b-p0070"></a>**B:p0070** (Section 6 -- Term and Termination.)

> d. Sections 1, 5, 7, and 8 survive termination of this Public License.

<a id="b-p0072"></a>**B:p0072** (Section 7 -- Other Terms and Conditions.)

> a. You shall not be bound by any additional or different terms or conditions communicated by the Licensor unless expressly agreed.

<a id="b-p0074"></a>**B:p0074** (Section 7 -- Other Terms and Conditions.)

> c. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities that apply to the Licensor or You, including from the legal processes of any jurisdiction or authority.
