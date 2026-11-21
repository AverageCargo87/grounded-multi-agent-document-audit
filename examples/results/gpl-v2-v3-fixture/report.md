# Document diff report: gpl-v2-v3-fixture

> **Fixture run.** Produced by the scripted FakeLLM test backend, not by a language model. It exercises every pipeline stage on real documents; the findings and verdicts are heuristic placeholders and say nothing about model quality.

| | |
|---|---|
| Mode | diff |
| Document A | `examples/gpl/GPL-2.0.txt` (59 paragraphs, sha256 `8177f9751321`) |
| Document B | `examples/gpl/GPL-3.0.txt` (122 paragraphs, sha256 `3972dc9744f6`) |
| Runner / backend | python / fake |
| Alignment | equal 8, modified 35, inserted 79, deleted 16, moved 0 |

## Pipeline

| Stage | Result |
|---|---|
| Section-reader chunks | 6 |
| Findings emitted by agents | 130 |
| Rejected by the quote verifier | 10 (7.7%) |
| Deterministic sweep findings | 0 |
| Evidence match levels (accepted) | exact 147, normalized 7; re-attributed 8 |
| Findings after merge | 130 |
| Changed operations cited by a finding | first pass 97/130 (74.6%); with gap reader 114/130 (87.7%) |
| Skeptic 'missed' findings | 16 reported, 0 rejected, 0 duplicates attached |
| Skeptic verdicts | 130 (upheld 87, weakened 43); ungrounded refutations 0 |
| Final status | downgraded 43, upheld 87 |
| LLM calls / tokens / cost | 14 calls, 157302 in, 22948 out, $0.0000 |

## Summary

130 findings survived quote verification and the skeptic stage (87 major, 43 minor). The first to read is F001: Value changed in (front matter): '2,' became '3, 29'. Its evidence reads "GENERAL PUBLIC LICENSE Version 3, 29 June 2007". 0 findings were refuted by skeptics and 0 are low-confidence.

- **changed (35)**: F001, F002, F090, F101, F102, F109, F036, F038, F076, F129, F004, F115, F005, F006, F007, F008, F010, F011, F035, F119, F048, F049, F121, F050, F124, F078, F128, F097, F106, F107, F108, F130, F110, F111, F114
- **removed (16)**: F012, F013, F039, F040, F041, F042, F120, F051, F052, F092, F127, F098, F113, F091, F093, F112
- **added (79)**: F014, F015, F017, F019, F020, F021, F022, F025, F117, F026, F028, F029, F030, F031, F032, F033, F034, F118, F037, F043, F044, F045, F046, F047, F053, F054, F122, F055, F056, F057, F058, F059, F060, F061, F062, F063, F123, F069, F070, F071, F072, F073, F074, F075, F125, F077, F080, F081, F083, F084, F126, F085, F086, F087, F088, F089, F094, F095, F096, F099, F100, F103, F104, F105, F003, F009, F016, F018, F116, F023, F024, F027, F064, F065, F066, F067, F068, F079, F082

## Findings (130)

major: 87, minor: 43

### F001 [major] changed: Value changed in (front matter): '2,' became '3, 29'

Confidence 0.91 (upheld). Reported by crossref, reader-c01.

Version A reads "2," where version B reads "3, 29". 1 further edit(s) in the same paragraph.

- [A:p0001](#a-p0001) (exact): "GENERAL PUBLIC LICENSE Version 2, June 1991"
- [B:p0001](#b-p0001) (exact): "GENERAL PUBLIC LICENSE Version 3, 29 June 2007"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F002 [major] changed: Value changed in (front matter): '1989, 1991' became '2007'

Confidence 0.91 (upheld). Reported by crossref, reader-c01.

Version A reads "1989, 1991" where version B reads "2007". 1 further edit(s) in the same paragraph.

- [A:p0002](#a-p0002) (exact): "Copyright (C) 1989, 1991 Free Software Foundation, Inc.,"
- [B:p0002](#b-p0002) (exact): "Copyright (C) 2007 Free Software Foundation, Inc."
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F090 [major] changed: Value changed in 12. No Surrender of Others' Freedom.: '7. If, as a consequence of a court judgment or allegation of patent infringement or for any other reason (not limited to patent issues),' became 'If'

Confidence 0.91 (upheld). Reported by crossref, reader-c05.

Version A reads "7. If, as a consequence of a court judgment or allegation of patent infringement or for any other reason (not limited to patent issues)," where version B reads "If". 7 further edit(s) in the same paragraph.

- [A:p0033](#a-p0033) (exact): "7. If, as a consequence of a court judgment or allegation of patent infringement or for any other reason (not limited to patent issues), conditions are imposed on"
- [B:p0095](#b-p0095) (exact): "If conditions are imposed on"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F101 [major] changed: Value changed in 15. Disclaimer of Warranty.: 'NO WARRANTY' became '15. Disclaimer of Warranty.'

Confidence 0.91 (upheld). Reported by crossref, reader-c06.

Version A reads "NO WARRANTY" where version B reads "15. Disclaimer of Warranty.".

- [A:p0041](#a-p0041) (exact): "NO WARRANTY"
- [B:p0103](#b-p0103) (exact): "15. Disclaimer of Warranty."
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F102 [major] changed: Value changed in 15. Disclaimer of Warranty.: '11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE,' became '(nothing)'

Confidence 0.91 (upheld). Reported by crossref, reader-c06.

Version A reads "11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE," where version B reads "(nothing)".

- [A:p0042](#a-p0042) (exact): "11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY"
- [B:p0104](#b-p0104) (exact): "THERE IS NO WARRANTY FOR"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F109 [major] changed: Value changed in How to Apply These Terms to Your New Programs: 'Gnomovision version 69,' became '<program>'

Confidence 0.91 (upheld). Reported by crossref, reader-c06.

Version A reads "Gnomovision version 69," where version B reads "<program>". 2 further edit(s) in the same paragraph.

- [A:p0054](#a-p0054) (exact): "Gnomovision version 69, Copyright (C) year name"
- [B:p0119](#b-p0119) (exact): "<program> Copyright (C) <year> <name"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F012 [major] removed: Text removed from 0. This License applies to any program or ...: 0. This License applies to any program or ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0013](#a-p0013) (exact): "0. This License applies to any program or other work which contains"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F013 [major] removed: Text removed from 0. This License applies to any program or ...: Activities other than copying, distribution and modification are ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0014](#a-p0014) (normalized): "activities other than copying, distribution and modification are not covered by this"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F014 [major] added: New text in 0. Definitions.: 0. Definitions. ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0015](#b-p0015) (exact): "0. Definitions."
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F015 [major] added: New text in 0. Definitions.: "This License" refers to version 3 of the ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0016](#b-p0016) (exact): ""This License" refers to version 3 of the GNU General Public License."
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F017 [major] added: New text in 0. Definitions.: "The Program" refers to any copyrightable work licensed ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0018](#b-p0018) (exact): ""The Program" refers to any copyrightable work licensed under this License. Each"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F019 [major] added: New text in 0. Definitions.: To "propagate" a work means to do anything ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0021](#b-p0021) (exact): "To "propagate" a work means to do anything with it that, without"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F020 [major] added: New text in 0. Definitions.: To "convey" a work means any kind of ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0022](#b-p0022) (exact): "To "convey" a work means any kind of propagation that enables other"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F021 [major] added: New text in 0. Definitions.: An interactive user interface displays "Appropriate Legal Notices" ...

Confidence 0.78 (upheld). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0023](#b-p0023) (exact): "An interactive user interface displays "Appropriate Legal Notices" to the extent that"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F022 [major] added: New text in 1. Source Code.: 1. Source Code. ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0024](#b-p0024) (exact): "1. Source Code."
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F025 [major] added: New text in 1. Source Code.: The "System Libraries" of an executable work include ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0027](#b-p0027) (exact): "The "System Libraries" of an executable work include anything, other than the"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F117 [major] added: New text in 1. Source Code.: The "Corresponding Source" for a work in object ...

Confidence 0.78 (upheld). Reported by skeptic-b01-v1:missed.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0028](#b-p0028) (exact): "The "Corresponding Source" for a work in object code form means all"
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F026 [major] added: New text in 1. Source Code.: The Corresponding Source need not include anything that ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0029](#b-p0029) (exact): "The Corresponding Source need not include anything that users can regenerate automatically"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F028 [major] added: New text in 2. Basic Permissions.: 2. Basic Permissions. ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0031](#b-p0031) (exact): "2. Basic Permissions."
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F029 [major] added: New text in 2. Basic Permissions.: All rights granted under this License are granted ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0032](#b-p0032) (exact, re-attributed): "All rights granted under this License are granted for the term of"
- Skeptic skeptic-b01-v1: **upheld**. Re-read the cited text; the finding holds.

### F030 [major] added: New text in 2. Basic Permissions.: You may make, run and propagate covered works ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0033](#b-p0033) (exact): "You may make, run and propagate covered works that you do not"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F031 [major] added: New text in 2. Basic Permissions.: Conveying under any other circumstances is permitted solely ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0034](#b-p0034) (exact): "Conveying under any other circumstances is permitted solely under the conditions stated"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F032 [major] added: New text in 3. Protecting Users' Legal Rights From Anti-Circumvention Law.: 3. Protecting Users' Legal Rights From Anti-Circumvention Law. ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0035](#b-p0035) (exact): "3. Protecting Users' Legal Rights From Anti-Circumvention Law."
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F033 [major] added: New text in 3. Protecting Users' Legal Rights From Anti-Circumvention Law.: No covered work shall be deemed part of ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0036](#b-p0036) (exact): "No covered work shall be deemed part of an effective technological measure"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F034 [major] added: New text in 3. Protecting Users' Legal Rights From Anti-Circumvention Law.: When you convey a covered work, you waive ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0037](#b-p0037) (normalized): "when you convey a covered work, you waive any legal power to"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F118 [major] added: New text in 4. Conveying Verbatim Copies.: 4. Conveying Verbatim Copies. ...

Confidence 0.78 (upheld). Reported by skeptic-b02-v1:missed.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0038](#b-p0038) (exact): "4. Conveying Verbatim Copies."
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F036 [major] changed: Wording changed in 4. Conveying Verbatim Copies.: 'a fee' became 'any price or no price'

Confidence 0.78 (upheld). Reported by reader-c02.

Version A reads "a fee" where version B reads "any price or no price". 4 further edit(s) in the same paragraph.

- [A:p0016](#a-p0016) (exact): "You may charge a fee for the physical act"
- [B:p0040](#b-p0040) (exact): "You may charge any price or no price for each copy that"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F037 [major] added: New text in 5. Conveying Modified Source Versions.: 5. Conveying Modified Source Versions. ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0041](#b-p0041) (exact): "5. Conveying Modified Source Versions."
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F038 [major] changed: Wording changed in 5. Conveying Modified Source Versions.: 'You' became 'The work'

Confidence 0.78 (upheld). Reported by gap.

Version A reads "You" where version B reads "The work". 3 further edit(s) in the same paragraph.

- [A:p0018](#a-p0018) (exact): "a) You must cause the modified"
- [B:p0043](#b-p0043) (exact): "a) The work must carry prominent notices"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F039 [major] removed: Text removed from 2. You may modify your copy or copies ...: b) You must cause any work that you ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0019](#a-p0019) (exact): "b) You must cause any work that you distribute or publish, that"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F040 [major] removed: Text removed from 2. You may modify your copy or copies ...: c) If the modified program normally reads commands ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0020](#a-p0020) (exact): "c) If the modified program normally reads commands interactively when run, you"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F041 [major] removed: Text removed from 2. You may modify your copy or copies ...: These requirements apply to the modified work as ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0021](#a-p0021) (exact): "These requirements apply to the modified work as a whole. If identifiable"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F042 [major] removed: Text removed from 2. You may modify your copy or copies ...: Thus, it is not the intent of this ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0022](#a-p0022) (exact, re-attributed): "Thus, it is not the intent of this section to claim rights"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F120 [major] removed: Text removed from 2. You may modify your copy or copies ...: In addition, mere aggregation of another work not ...

Confidence 0.78 (upheld). Reported by skeptic-b02-v1:missed.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0023](#a-p0023) (exact): "In addition, mere aggregation of another work not based on the Program"
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F043 [major] added: New text in 5. Conveying Modified Source Versions.: b) The work must carry prominent notices stating ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0044](#b-p0044) (exact): "b) The work must carry prominent notices stating that it is released"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F044 [major] added: New text in 5. Conveying Modified Source Versions.: c) You must license the entire work, as ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0045](#b-p0045) (exact): "c) You must license the entire work, as a whole, under this"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F045 [major] added: New text in 5. Conveying Modified Source Versions.: d) If the work has interactive user interfaces, ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0046](#b-p0046) (exact): "d) If the work has interactive user interfaces, each must display Appropriate"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F046 [major] added: New text in 5. Conveying Modified Source Versions.: A compilation of a covered work with other ...

Confidence 0.78 (upheld). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0047](#b-p0047) (normalized): "a compilation of a covered work with other separate and independent works,"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F047 [major] added: New text in 6. Conveying Non-Source Forms.: 6. Conveying Non-Source Forms. ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0048](#b-p0048) (exact): "6. Conveying Non-Source Forms."
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F051 [major] removed: Text removed from 3. You may copy and distribute the Program ...: The source code for a work means the ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0028](#a-p0028) (exact): "The source code for a work means the preferred form of the"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F052 [major] removed: Text removed from 3. You may copy and distribute the Program ...: If distribution of executable or object code is ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0029](#a-p0029) (exact): "If distribution of executable or object code is made by offering access"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F053 [major] added: New text in 6. Conveying Non-Source Forms.: d) Convey the object code by offering access ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0053](#b-p0053) (exact): "d) Convey the object code by offering access from a designated place"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F054 [major] added: New text in 6. Conveying Non-Source Forms.: e) Convey the object code using peer-to-peer transmission, ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0054](#b-p0054) (exact, re-attributed): "e) Convey the object code using peer-to-peer transmission, provided you inform other"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F122 [major] added: New text in 6. Conveying Non-Source Forms.: A separable portion of the object code, whose ...

Confidence 0.78 (upheld). Reported by skeptic-b02-v1:missed.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0055](#b-p0055) (exact): "A separable portion of the object code, whose source code is excluded"
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F055 [major] added: New text in 6. Conveying Non-Source Forms.: A "User Product" is either (1) a "consumer ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0056](#b-p0056) (exact): "A "User Product" is either (1) a "consumer product", which means any"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F056 [major] added: New text in 6. Conveying Non-Source Forms.: "Installation Information" for a User Product means any ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0057](#b-p0057) (exact): ""Installation Information" for a User Product means any methods, procedures, authorization keys,"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F057 [major] added: New text in 6. Conveying Non-Source Forms.: If you convey an object code work under ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0058](#b-p0058) (exact): "If you convey an object code work under this section in, or"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F058 [major] added: New text in 6. Conveying Non-Source Forms.: The requirement to provide Installation Information does not ...

Confidence 0.78 (upheld). Reported by reader-c03.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0059](#b-p0059) (normalized): "the requirement to provide installation information does not include a requirement to"
- Skeptic skeptic-b02-v1: **upheld**. Re-read the cited text; the finding holds.

### F059 [major] added: New text in 6. Conveying Non-Source Forms.: Corresponding Source conveyed, and Installation Information provided, in ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0060](#b-p0060) (exact): "Corresponding Source conveyed, and Installation Information provided, in accord with this section"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F060 [major] added: New text in 7. Additional Terms.: 7. Additional Terms. ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0061](#b-p0061) (exact): "7. Additional Terms."
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F061 [major] added: New text in 7. Additional Terms.: "Additional permissions" are terms that supplement the terms ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0062](#b-p0062) (exact): ""Additional permissions" are terms that supplement the terms of this License by"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F062 [major] added: New text in 7. Additional Terms.: When you convey a copy of a covered ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0063](#b-p0063) (exact): "When you convey a copy of a covered work, you may at"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F063 [major] added: New text in 7. Additional Terms.: Notwithstanding any other provision of this License, for ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0064](#b-p0064) (exact): "Notwithstanding any other provision of this License, for material you add to"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F123 [major] added: New text in 7. Additional Terms.: a) Disclaiming warranty or limiting liability differently from ...

Confidence 0.78 (upheld). Reported by skeptic-b03-v1:missed.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0065](#b-p0065) (exact): "a) Disclaiming warranty or limiting liability differently from the terms of sections"
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F069 [major] added: New text in 7. Additional Terms.: All other non-permissive additional terms are considered "further ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0071](#b-p0071) (exact): "All other non-permissive additional terms are considered "further restrictions" within the meaning"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F070 [major] added: New text in 7. Additional Terms.: If you add terms to a covered work ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0072](#b-p0072) (exact): "If you add terms to a covered work in accord with this"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F071 [major] added: New text in 7. Additional Terms.: Additional terms, permissive or non-permissive, may be stated ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0073](#b-p0073) (exact): "Additional terms, permissive or non-permissive, may be stated in the form of"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F072 [major] added: New text in 8. Termination.: 8. Termination. ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0074](#b-p0074) (normalized): "8. termination."
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F073 [major] added: New text in 8. Termination.: However, if you cease all violation of this ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0076](#b-p0076) (exact): "However, if you cease all violation of this License, then your license"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F074 [major] added: New text in 8. Termination.: Moreover, your license from a particular copyright holder ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0077](#b-p0077) (exact): "Moreover, your license from a particular copyright holder is reinstated permanently if"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F075 [major] added: New text in 8. Termination.: Termination of your rights under this section does ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0078](#b-p0078) (exact): "Termination of your rights under this section does not terminate the licenses"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F125 [major] added: New text in 9. Acceptance Not Required for Having Copies.: 9. Acceptance Not Required for Having Copies. ...

Confidence 0.78 (upheld). Reported by skeptic-b03-v1:missed.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0079](#b-p0079) (exact): "9. Acceptance Not Required for Having Copies."
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F076 [major] changed: Wording changed in 9. Acceptance Not Required for Having Copies.: 'License, since you have' became 'License in order to receive or'

Confidence 0.78 (upheld). Reported by gap.

Version A reads "License, since you have" where version B reads "License in order to receive or run a copy of the Program. Ancillary propagation of a covered work occurring solely as a consequence of using peer-to-peer transmission to receive a copy likewise does". 8 further edit(s) in the same paragraph.

- [A:p0031](#a-p0031) (exact): "required to accept this License, since you have not signed it. However,"
- [B:p0080](#b-p0080) (exact): "required to accept this License in order to receive or run a copy of the Program. Ancillary propagation of a covered work occurring solely as a consequence of using peer-to-peer transmission to receive a copy likewise does not require acceptance. However,"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F077 [major] added: New text in 10. Automatic Licensing of Downstream Recipients.: 10. Automatic Licensing of Downstream Recipients. ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0081](#b-p0081) (exact): "10. Automatic Licensing of Downstream Recipients."
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F080 [major] added: New text in 10. Automatic Licensing of Downstream Recipients.: You may not impose any further restrictions on ...

Confidence 0.78 (upheld). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0084](#b-p0084) (exact, re-attributed): "You may not impose any further restrictions on the exercise of the"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F081 [major] added: New text in 11. Patents.: 11. Patents. ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0085](#b-p0085) (exact): "11. Patents."
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F083 [major] added: New text in 11. Patents.: A contributor's "essential patent claims" are all patent ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0087](#b-p0087) (exact): "A contributor's "essential patent claims" are all patent claims owned or controlled"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F084 [major] added: New text in 11. Patents.: Each contributor grants you a non-exclusive, worldwide, royalty-free ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0088](#b-p0088) (exact): "Each contributor grants you a non-exclusive, worldwide, royalty-free patent license under the"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F126 [major] added: New text in 11. Patents.: In the following three paragraphs, a "patent license" ...

Confidence 0.78 (upheld). Reported by skeptic-b03-v1:missed.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0089](#b-p0089) (exact): "In the following three paragraphs, a "patent license" is any express agreement"
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F085 [major] added: New text in 11. Patents.: If you convey a covered work, knowingly relying ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0090](#b-p0090) (exact): "If you convey a covered work, knowingly relying on a patent license,"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F086 [major] added: New text in 11. Patents.: If, pursuant to or in connection with a ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0091](#b-p0091) (exact): "If, pursuant to or in connection with a single transaction or arrangement,"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F087 [major] added: New text in 11. Patents.: A patent license is "discriminatory" if it does ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0092](#b-p0092) (exact): "A patent license is "discriminatory" if it does not include within the"
- Skeptic skeptic-b03-v1: **upheld**. Re-read the cited text; the finding holds.

### F088 [major] added: New text in 11. Patents.: Nothing in this License shall be construed as ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0093](#b-p0093) (exact, re-attributed): "Nothing in this License shall be construed as excluding or limiting any"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F089 [major] added: New text in 12. No Surrender of Others' Freedom.: 12. No Surrender of Others' Freedom. ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0094](#b-p0094) (exact): "12. No Surrender of Others' Freedom."
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F092 [major] removed: Text removed from 7. If, as a consequence of a court ...: It is not the purpose of this section ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0035](#a-p0035) (exact): "It is not the purpose of this section to induce you to"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F127 [major] removed: Text removed from 8. If the distribution and/or use of the ...: 8. If the distribution and/or use of the ...

Confidence 0.78 (upheld). Reported by skeptic-b04-v1:missed.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0037](#a-p0037) (exact): "8. If the distribution and/or use of the Program is restricted in"
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F094 [major] added: New text in 13. Use with the GNU Affero General Public License.: 13. Use with the GNU Affero General Public ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0096](#b-p0096) (exact): "13. Use with the GNU Affero General Public License."
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F095 [major] added: New text in 13. Use with the GNU Affero General Public License.: Notwithstanding any other provision of this License, you ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0097](#b-p0097) (exact): "Notwithstanding any other provision of this License, you have permission to link"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F096 [major] added: New text in 14. Revised Versions of this License.: 14. Revised Versions of this License. ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0098](#b-p0098) (exact): "14. Revised Versions of this License."
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F098 [major] removed: Text removed from 10. If you wish to incorporate parts of ...: 10. If you wish to incorporate parts of ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0040](#a-p0040) (exact): "10. If you wish to incorporate parts of the Program into other"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F099 [major] added: New text in 14. Revised Versions of this License.: If the Program specifies that a proxy can ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0101](#b-p0101) (exact): "If the Program specifies that a proxy can decide which future versions"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F100 [major] added: New text in 14. Revised Versions of this License.: Later license versions may give you additional or ...

Confidence 0.78 (upheld). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0102](#b-p0102) (exact): "Later license versions may give you additional or different permissions. However, no"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F103 [major] added: New text in 16. Limitation of Liability.: 16. Limitation of Liability. ...

Confidence 0.78 (upheld). Reported by reader-c06.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0105](#b-p0105) (exact): "16. Limitation of Liability."
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F129 [major] changed: Wording changed in 16. Limitation of Liability.: 'MAY MODIFY' became 'MODIFIES'

Confidence 0.78 (upheld). Reported by skeptic-b04-v1:missed.

Version A reads "MAY MODIFY" where version B reads "MODIFIES". 2 further edit(s) in the same paragraph.

- [A:p0043](#a-p0043) (exact): "ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE THE PROGRAM"
- [B:p0106](#b-p0106) (exact): "ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM"
- Skeptic recheck-r01-v1: **upheld**. Re-read the cited text; the finding holds.

### F104 [major] added: New text in 17. Interpretation of Sections 15 and 16.: 17. Interpretation of Sections 15 and 16. ...

Confidence 0.78 (upheld). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0107](#b-p0107) (exact): "17. Interpretation of Sections 15 and 16."
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F105 [major] added: New text in 17. Interpretation of Sections 15 and 16.: If the disclaimer of warranty and limitation of ...

Confidence 0.78 (upheld). Reported by reader-c06.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0108](#b-p0108) (exact): "If the disclaimer of warranty and limitation of liability provided above cannot"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F113 [major] removed: Text removed from How to Apply These Terms to Your New Programs: <signature of Ty Coon>, 1 April 1989 Ty ...

Confidence 0.78 (upheld). Reported by gap.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0058](#a-p0058) (exact): "<signature of Ty Coon>, 1 April 1989 Ty Coon, President of Vice"
- Skeptic skeptic-b04-v1: **upheld**. Re-read the cited text; the finding holds.

### F003 [minor] added: New text in Preamble: The GNU General Public License is a free, ...

Confidence 0.36 (downgraded). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0004](#b-p0004) (exact): "The GNU General Public License is a free, copyleft license for software"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0004](#b-p0004): "The GNU General Public License is a free, copyleft license for software"

### F004 [minor] changed: Wording changed in Preamble: '(nothing)' became 'and other practical works'

Confidence 0.36 (downgraded). Reported by gap.

Version A reads "(nothing)" where version B reads "and other practical works". 9 further edit(s) in the same paragraph.

- [A:p0004](#a-p0004) (exact): "licenses for most software are designed to take away"
- [B:p0005](#b-p0005) (exact): "licenses for most software and other practical works are designed to take"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0004](#a-p0004): "licenses for most software are designed to take away"

### F115 [minor] changed: Wording changed in Preamble: 'this service' became 'them'

Confidence 0.36 (downgraded). Reported by skeptic-b01-v1:missed.

Version A reads "this service" where version B reads "them". 1 further edit(s) in the same paragraph.

- [A:p0005](#a-p0005) (exact): "software (and charge for this service if you wish), that"
- [B:p0006](#b-p0006) (exact): "software (and charge for them if you wish), that"
- Skeptic recheck-r01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0005](#a-p0005): "software (and charge for this service if you wish), that"

### F005 [minor] changed: Wording changed in Preamble: 'make restrictions that forbid anyone to' became 'prevent others from denying'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "make restrictions that forbid anyone to deny" where version B reads "prevent others from denying". 4 further edit(s) in the same paragraph.

- [A:p0006](#a-p0006) (exact): "rights, we need to make restrictions that forbid anyone to deny you these rights or"
- [B:p0007](#b-p0007) (exact): "rights, we need to prevent others from denying you these rights or"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0006](#a-p0006): "rights, we need to make restrictions that forbid anyone to deny you these rights or"

### F006 [minor] changed: Wording changed in Preamble: 'give' became 'pass on to'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "give" where version B reads "pass on to". 3 further edit(s) in the same paragraph.

- [A:p0007](#a-p0007) (exact): "a fee, you must give the recipients all the"
- [B:p0008](#b-p0008) (exact): "a fee, you must pass on to the recipients the same"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0007](#a-p0007): "a fee, you must give the recipients all the"

### F007 [minor] changed: Wording changed in Preamble: 'We' became 'Developers that use the GNU GPL'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "We" where version B reads "Developers that use the GNU GPL". 4 further edit(s) in the same paragraph.

- [A:p0008](#a-p0008) (exact): "We protect your rights with"
- [B:p0009](#b-p0009) (exact): "Developers that use the GNU GPL protect your rights with"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0008](#a-p0008): "We protect your rights with"

### F008 [minor] changed: Wording changed in Preamble: 'Also,' became '(nothing)'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "Also," where version B reads "(nothing)". 8 further edit(s) in the same paragraph.

- [A:p0009](#a-p0009) (exact): "Also, for each author's protection"
- [B:p0010](#b-p0010) (exact, re-attributed): "For the developers' and authors'"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0009](#a-p0009): "Also, for each author's protection"

### F009 [minor] added: New text in Preamble: Some devices are designed to deny users access ...

Confidence 0.36 (downgraded). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0011](#b-p0011) (exact): "Some devices are designed to deny users access to install or run"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0011](#b-p0011): "Some devices are designed to deny users access to install or run"

### F010 [minor] changed: Wording changed in Preamble: 'any free' became 'every'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "any free" where version B reads "every". 7 further edit(s) in the same paragraph.

- [A:p0010](#a-p0010) (exact): "Finally, any free program is threatened constantly"
- [B:p0012](#b-p0012) (exact): "Finally, every program is threatened constantly"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0010](#a-p0010): "Finally, any free program is threatened constantly"

### F011 [minor] changed: Wording changed in TERMS AND CONDITIONS: 'GNU GENERAL PUBLIC LICENSE' became '(nothing)'

Confidence 0.36 (downgraded). Reported by reader-c01.

Version A reads "GNU GENERAL PUBLIC LICENSE" where version B reads "(nothing)". 1 further edit(s) in the same paragraph.

- [A:p0012](#a-p0012) (exact): "GNU GENERAL PUBLIC LICENSE TERMS AND CONDITIONS FOR"
- [B:p0014](#b-p0014) (exact): "TERMS AND CONDITIONS"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0012](#a-p0012): "GNU GENERAL PUBLIC LICENSE TERMS AND CONDITIONS FOR"

### F016 [minor] added: New text in 0. Definitions.: "Copyright" also means copyright-like laws that apply to ...

Confidence 0.36 (downgraded). Reported by reader-c01.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0017](#b-p0017) (exact): ""Copyright" also means copyright-like laws that apply to other kinds of works,"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0017](#b-p0017): ""Copyright" also means copyright-like laws that apply to other kinds of works,"

### F018 [minor] added: New text in 0. Definitions.: To "modify" a work means to copy from ...

Confidence 0.36 (downgraded). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0019](#b-p0019) (exact): "To "modify" a work means to copy from or adapt all or"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0019](#b-p0019): "To "modify" a work means to copy from or adapt all or"

### F116 [minor] added: New text in 0. Definitions.: A "covered work" means either the unmodified Program ...

Confidence 0.36 (downgraded). Reported by skeptic-b01-v1:missed.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0020](#b-p0020) (exact): "A "covered work" means either the unmodified Program or a work based"
- Skeptic recheck-r01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0020](#b-p0020): "A "covered work" means either the unmodified Program or a work based"

### F023 [minor] added: New text in 1. Source Code.: The "source code" for a work means the ...

Confidence 0.36 (downgraded). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0025](#b-p0025) (exact): "The "source code" for a work means the preferred form of the"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0025](#b-p0025): "The "source code" for a work means the preferred form of the"

### F024 [minor] added: New text in 1. Source Code.: A "Standard Interface" means an interface that either ...

Confidence 0.36 (downgraded). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0026](#b-p0026) (exact): "A "Standard Interface" means an interface that either is an official standard"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0026](#b-p0026): "A "Standard Interface" means an interface that either is an official standard"

### F027 [minor] added: New text in 1. Source Code.: The Corresponding Source for a work in source ...

Confidence 0.36 (downgraded). Reported by reader-c02.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0030](#b-p0030) (exact): "The Corresponding Source for a work in source code form is that"
- Skeptic skeptic-b01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0030](#b-p0030): "The Corresponding Source for a work in source code form is that"

### F035 [minor] changed: Wording changed in 4. Conveying Verbatim Copies.: 'copy and distribute' became 'convey'

Confidence 0.36 (downgraded). Reported by reader-c02.

Version A reads "copy and distribute" where version B reads "convey". 9 further edit(s) in the same paragraph.

- [A:p0015](#a-p0015) (exact): "1. You may copy and distribute verbatim copies of the"
- [B:p0039](#b-p0039) (exact): "You may convey verbatim copies of the"
- Skeptic skeptic-b02-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0015](#a-p0015): "1. You may copy and distribute verbatim copies of the"

### F119 [minor] changed: Wording changed in 5. Conveying Modified Source Versions.: 'modify your copy or copies of' became 'convey'

Confidence 0.36 (downgraded). Reported by skeptic-b02-v1:missed.

Version A reads "modify your copy or copies of the Program or any portion of it, thus forming" where version B reads "convey". 4 further edit(s) in the same paragraph.

- [A:p0017](#a-p0017) (exact): "2. You may modify your copy or copies of the Program or any portion of it, thus forming a work based on"
- [B:p0042](#b-p0042) (exact): "You may convey a work based on"
- Skeptic recheck-r01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0017](#a-p0017): "2. You may modify your copy or copies of the Program or any portion of it, thus forming a work based on"

### F048 [minor] changed: Wording changed in 6. Conveying Non-Source Forms.: 'copy and distribute the Program (or' became 'convey'

Confidence 0.36 (downgraded). Reported by reader-c03.

Version A reads "copy and distribute the Program (or" where version B reads "convey". 8 further edit(s) in the same paragraph.

- [A:p0024](#a-p0024) (exact): "3. You may copy and distribute the Program (or a work based on"
- [B:p0049](#b-p0049) (exact): "You may convey a covered work in"
- Skeptic skeptic-b02-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0024](#a-p0024): "3. You may copy and distribute the Program (or a work based on"

### F049 [minor] changed: Wording changed in 6. Conveying Non-Source Forms.: 'Accompany it with' became 'Convey'

Confidence 0.36 (downgraded). Reported by reader-c03.

Version A reads "Accompany it with" where version B reads "Convey". 5 further edit(s) in the same paragraph.

- [A:p0025](#a-p0025) (exact): "a) Accompany it with the complete corresponding machine-readable"
- [B:p0050](#b-p0050) (exact): "a) Convey the object code in,"
- Skeptic skeptic-b02-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0025](#a-p0025): "a) Accompany it with the complete corresponding machine-readable"

### F121 [minor] changed: Wording changed in 6. Conveying Non-Source Forms.: 'Accompany it with' became 'Convey the object code in, or'

Confidence 0.36 (downgraded). Reported by skeptic-b02-v1:missed.

Version A reads "Accompany it with" where version B reads "Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by". 7 further edit(s) in the same paragraph.

- [A:p0026](#a-p0026) (exact): "b) Accompany it with a written offer, valid"
- [B:p0051](#b-p0051) (exact): "b) Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by a written offer, valid"
- Skeptic recheck-r01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0026](#a-p0026): "b) Accompany it with a written offer, valid"

### F050 [minor] changed: Wording changed in 6. Conveying Non-Source Forms.: 'Accompany it' became 'Convey individual copies of the object'

Confidence 0.36 (downgraded). Reported by gap.

Version A reads "Accompany it" where version B reads "Convey individual copies of the object code". 8 further edit(s) in the same paragraph.

- [A:p0027](#a-p0027) (exact): "c) Accompany it with the information you"
- [B:p0052](#b-p0052) (exact): "c) Convey individual copies of the object code with a copy of"
- Skeptic skeptic-b02-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0027](#a-p0027): "c) Accompany it with the information you"

### F064 [minor] added: New text in 7. Additional Terms.: b) Requiring preservation of specified reasonable legal notices ...

Confidence 0.36 (downgraded). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0066](#b-p0066) (exact): "b) Requiring preservation of specified reasonable legal notices or author attributions in"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0066](#b-p0066): "b) Requiring preservation of specified reasonable legal notices or author attributions in"

### F065 [minor] added: New text in 7. Additional Terms.: c) Prohibiting misrepresentation of the origin of that ...

Confidence 0.36 (downgraded). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0067](#b-p0067) (exact): "c) Prohibiting misrepresentation of the origin of that material, or requiring that"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0067](#b-p0067): "c) Prohibiting misrepresentation of the origin of that material, or requiring that"

### F066 [minor] added: New text in 7. Additional Terms.: d) Limiting the use for publicity purposes of ...

Confidence 0.36 (downgraded). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0068](#b-p0068) (exact): "d) Limiting the use for publicity purposes of names of licensors or"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0068](#b-p0068): "d) Limiting the use for publicity purposes of names of licensors or"

### F067 [minor] added: New text in 7. Additional Terms.: e) Declining to grant rights under trademark law ...

Confidence 0.36 (downgraded). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0069](#b-p0069) (exact, re-attributed): "e) Declining to grant rights under trademark law for use of some"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0069](#b-p0069): "e) Declining to grant rights under trademark law for use of some"

### F068 [minor] added: New text in 7. Additional Terms.: f) Requiring indemnification of licensors and authors of ...

Confidence 0.36 (downgraded). Reported by gap.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0070](#b-p0070) (exact): "f) Requiring indemnification of licensors and authors of that material by anyone"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0070](#b-p0070): "f) Requiring indemnification of licensors and authors of that material by anyone"

### F124 [minor] changed: Wording changed in 8. Termination.: 'copy, modify, sublicense,' became 'propagate'

Confidence 0.36 (downgraded). Reported by skeptic-b03-v1:missed.

Version A reads "copy, modify, sublicense," where version B reads "propagate". 6 further edit(s) in the same paragraph.

- [A:p0030](#a-p0030) (exact): "4. You may not copy, modify, sublicense, or distribute the Program"
- [B:p0075](#b-p0075) (exact): "You may not propagate or modify a covered"
- Skeptic recheck-r01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0030](#a-p0030): "4. You may not copy, modify, sublicense, or distribute the Program"

### F078 [minor] changed: Wording changed in 10. Automatic Licensing of Downstream Recipients.: 'redistribute the Program (or any work' became 'convey a covered work,'

Confidence 0.36 (downgraded). Reported by reader-c04.

Version A reads "redistribute the Program (or any work based on the Program)," where version B reads "convey a covered work,". 6 further edit(s) in the same paragraph.

- [A:p0032](#a-p0032) (exact): "6. Each time you redistribute the Program (or any work based on the Program), the recipient automatically receives"
- [B:p0082](#b-p0082) (exact): "Each time you convey a covered work, the recipient automatically receives"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0032](#a-p0032): "6. Each time you redistribute the Program (or any work based on the Program), the recipient automatically receives"

### F079 [minor] added: New text in 10. Automatic Licensing of Downstream Recipients.: An "entity transaction" is a transaction transferring control ...

Confidence 0.36 (downgraded). Reported by reader-c04.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0083](#b-p0083) (exact): "An "entity transaction" is a transaction transferring control of an organization, or"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0083](#b-p0083): "An "entity transaction" is a transaction transferring control of an organization, or"

### F082 [minor] added: New text in 11. Patents.: A "contributor" is a copyright holder who authorizes ...

Confidence 0.36 (downgraded). Reported by reader-c05.

Version B contains this paragraph and version A has no counterpart for it.

- [B:p0086](#b-p0086) (exact): "A "contributor" is a copyright holder who authorizes use under this License"
- Skeptic skeptic-b03-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [B:p0086](#b-p0086): "A "contributor" is a copyright holder who authorizes use under this License"

### F091 [minor] removed: Text removed from 7. If, as a consequence of a court ...: If any portion of this section is held ...

Confidence 0.36 (downgraded). Reported by reader-c05.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0034](#a-p0034) (exact): "If any portion of this section is held invalid or unenforceable under"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0034](#a-p0034): "If any portion of this section is held invalid or unenforceable under"

### F093 [minor] removed: Text removed from 7. If, as a consequence of a court ...: This section is intended to make thoroughly clear ...

Confidence 0.36 (downgraded). Reported by reader-c05.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0036](#a-p0036) (normalized): "this section is intended to make thoroughly clear what is believed to"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0036](#a-p0036): "this section is intended to make thoroughly clear what is believed to"

### F128 [minor] changed: Wording changed in 14. Revised Versions of this License.: '(nothing)' became 'GNU'

Confidence 0.36 (downgraded). Reported by skeptic-b04-v1:missed.

Version A reads "(nothing)" where version B reads "GNU". 1 further edit(s) in the same paragraph.

- [A:p0038](#a-p0038) (exact): "new versions of the General Public License from time"
- [B:p0099](#b-p0099) (exact): "new versions of the GNU General Public License from"
- Skeptic recheck-r01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0038](#a-p0038): "new versions of the General Public License from time"

### F097 [minor] changed: Wording changed in 14. Revised Versions of this License.: '(nothing)' became 'that'

Confidence 0.36 (downgraded). Reported by gap.

Version A reads "(nothing)" where version B reads "that". 7 further edit(s) in the same paragraph.

- [A:p0039](#a-p0039) (exact): "If the Program specifies a version number of this"
- [B:p0100](#b-p0100) (exact): "If the Program specifies that a certain numbered version"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0039](#a-p0039): "If the Program specifies a version number of this"

### F106 [minor] changed: Wording changed in How to Apply These Terms to Your New Programs: 'convey' became 'state'

Confidence 0.36 (downgraded). Reported by reader-c06.

Version A reads "convey" where version B reads "state".

- [A:p0047](#a-p0047) (exact): "file to most effectively convey the exclusion of warranty;"
- [B:p0112](#b-p0112) (exact): "file to most effectively state the exclusion of warranty;"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0047](#a-p0047): "file to most effectively convey the exclusion of warranty;"

### F107 [minor] changed: Wording changed in How to Apply These Terms to Your New Programs: 'software;' became 'software:'

Confidence 0.36 (downgraded). Reported by reader-c06.

Version A reads "software;" where version B reads "software:". 2 further edit(s) in the same paragraph.

- [A:p0049](#a-p0049) (exact): "This program is free software; you can redistribute it"
- [B:p0114](#b-p0114) (exact): "This program is free software: you can redistribute it"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0049](#a-p0049): "This program is free software; you can redistribute it"

### F108 [minor] changed: Wording changed in How to Apply These Terms to Your New Programs: 'program;' became 'program.'

Confidence 0.36 (downgraded). Reported by reader-c06.

Version A reads "program;" where version B reads "program.". 1 further edit(s) in the same paragraph.

- [A:p0051](#a-p0051) (exact): "License along with this program; if not, write to"
- [B:p0116](#b-p0116) (exact, re-attributed): "License along with this program. If not, see <https://www.gnu.org/licenses/>."
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0051](#a-p0051): "License along with this program; if not, write to"

### F130 [minor] changed: Wording changed in How to Apply These Terms to Your New Programs: 'is interactive,' became 'does terminal interaction,'

Confidence 0.36 (downgraded). Reported by skeptic-b04-v1:missed.

Version A reads "is interactive," where version B reads "does terminal interaction,".

- [A:p0053](#a-p0053) (exact): "If the program is interactive, make it output a"
- [B:p0118](#b-p0118) (exact): "If the program does terminal interaction, make it output a"
- Skeptic recheck-r01-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0053](#a-p0053): "If the program is interactive, make it output a"

### F110 [minor] changed: Wording changed in How to Apply These Terms to Your New Programs: 'the' became 'your program's'

Confidence 0.36 (downgraded). Reported by reader-c06.

Version A reads "the" where version B reads "your program's". 3 further edit(s) in the same paragraph.

- [A:p0055](#a-p0055) (exact): "Public License. Of course, the commands you use may"
- [B:p0120](#b-p0120) (exact): "Public License. Of course, your program's commands might be different;"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0055](#a-p0055): "Public License. Of course, the commands you use may"

### F111 [minor] changed: Wording changed in How to Apply These Terms to Your New Programs: 'your' became '(nothing)'

Confidence 0.36 (downgraded). Reported by reader-c06.

Version A reads "your" where version B reads "(nothing)". 2 further edit(s) in the same paragraph.

- [A:p0056](#a-p0056) (exact): "as a programmer) or your school, if any, to"
- [B:p0121](#b-p0121) (exact): "as a programmer) or school, if any, to sign"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0056](#a-p0056): "as a programmer) or your school, if any, to"

### F112 [minor] removed: Text removed from How to Apply These Terms to Your New Programs: Yoyodyne, Inc., hereby disclaims all copyright interest in ...

Confidence 0.36 (downgraded). Reported by reader-c06.

Version A contains this paragraph and version B has no counterpart for it.

- [A:p0057](#a-p0057) (normalized): "yoyodyne, inc., hereby disclaims all copyright interest in the program `gnomovision' (which"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0057](#a-p0057): "yoyodyne, inc., hereby disclaims all copyright interest in the program `gnomovision' (which"

### F114 [minor] changed: Wording changed in How to Apply These Terms to Your New Programs: 'This' became 'The GNU'

Confidence 0.36 (downgraded). Reported by reader-c06.

Version A reads "This" where version B reads "The GNU". 1 further edit(s) in the same paragraph.

- [A:p0059](#a-p0059) (exact): "This General Public License does"
- [B:p0122](#b-p0122) (exact): "The GNU General Public License does"
- Skeptic skeptic-b04-v1: **weakened**. Real, but the practical effect is limited.
  - counter-evidence [A:p0059](#a-p0059): "This General Public License does"

## Rejected by the quote verifier (10)

| Agent | Kind | Title | Reason |
|---|---|---|---|
| reader-c01 | changed | Wording changed in Preamble: '(nothing)' became 'and other practical works' | B:p0005 quote_not_found (longest common run 22% of quote) |
| reader-c01 | added | New text in 0. Definitions.: To "modify" a work means to copy from ... | B:p0019 quote_not_found (longest common run 17% of quote) |
| reader-c02 | added | New text in 1. Source Code.: The "System Libraries" of an executable work include ... | B:p0027 quote_not_found (longest common run 25% of quote) |
| reader-c02 | changed | Wording changed in 5. Conveying Modified Source Versions.: 'modify your copy or copies of' | B:p0042 quote_not_found (longest common run 18% of quote) |
| reader-c03 | changed | Wording changed in 6. Conveying Non-Source Forms.: 'Accompany it with' became 'Convey the  | B:p0051 quote_not_found (longest common run 17% of quote) |
| reader-c04 | added | New text in 7. Additional Terms.: Notwithstanding any other provision of this License, for | B:p0064 quote_not_found (longest common run 27% of quote) |
| reader-c04 | added | New text in 9. Acceptance Not Required for Having Copies.: 9. Acceptance Not Required for  | B:p0079 quote_not_found (longest common run 21% of quote) |
| reader-c05 | added | New text in 11. Patents.: Each contributor grants you a non-exclusive, worldwide, royalty- | B:p0088 quote_not_found (longest common run 26% of quote) |
| reader-c05 | changed | Wording changed in 14. Revised Versions of this License.: '(nothing)' became 'GNU' | B:p0099 quote_not_found (longest common run 19% of quote) |
| reader-c06 | changed | Wording changed in 16. Limitation of Liability.: 'MAY MODIFY' became 'MODIFIES' | B:p0106 quote_not_found (longest common run 19% of quote) |

## Cited paragraphs

<a id="a-p0001"></a>**A:p0001** ((front matter))

> GNU GENERAL PUBLIC LICENSE Version 2, June 1991

<a id="a-p0002"></a>**A:p0002** ((front matter))

> Copyright (C) 1989, 1991 Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

<a id="a-p0004"></a>**A:p0004** (Preamble)

> The licenses for most software are designed to take away your freedom to share and change it. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change free software--to make sure the software is free for all its users. This General Public License applies to most of the Free Software Foundation's software and to any other program whose authors commit to using it. (Some other Free Software Foundation software is covered by the GNU Lesser General Public License instead.) You can apply it to your programs, too.

<a id="a-p0005"></a>**A:p0005** (Preamble)

> When we speak of free software, we are referring to freedom, not price. Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for this service if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs; and that you know you can do these things.

<a id="a-p0006"></a>**A:p0006** (Preamble)

> To protect your rights, we need to make restrictions that forbid anyone to deny you these rights or to ask you to surrender the rights. These restrictions translate to certain responsibilities for you if you distribute copies of the software, or if you modify it.

<a id="a-p0007"></a>**A:p0007** (Preamble)

> For example, if you distribute copies of such a program, whether gratis or for a fee, you must give the recipients all the rights that you have. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights.

<a id="a-p0008"></a>**A:p0008** (Preamble)

> We protect your rights with two steps: (1) copyright the software, and (2) offer you this license which gives you legal permission to copy, distribute and/or modify the software.

<a id="a-p0009"></a>**A:p0009** (Preamble)

> Also, for each author's protection and ours, we want to make certain that everyone understands that there is no warranty for this free software. If the software is modified by someone else and passed on, we want its recipients to know that what they have is not the original, so that any problems introduced by others will not reflect on the original authors' reputations.

<a id="a-p0010"></a>**A:p0010** (Preamble)

> Finally, any free program is threatened constantly by software patents. We wish to avoid the danger that redistributors of a free program will individually obtain patent licenses, in effect making the program proprietary. To prevent this, we have made it clear that any patent must be licensed for everyone's free use or not licensed at all.

<a id="a-p0012"></a>**A:p0012** (Preamble)

> GNU GENERAL PUBLIC LICENSE TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

<a id="a-p0013"></a>**A:p0013** (0. This License applies to any program or ...)

> 0. This License applies to any program or other work which contains a notice placed by the copyright holder saying it may be distributed under the terms of this General Public License. The "Program", below, refers to any such program or work, and a "work based on the Program" means either the Program or any derivative work under copyright law: that is to say, a work containing the Program or a portion of it, either verbatim or with modifications and/or translated into another language. (Hereinafter, translation is included without limitation in the term "modification".) Each licensee is addressed as "you".

<a id="a-p0014"></a>**A:p0014** (0. This License applies to any program or ...)

> Activities other than copying, distribution and modification are not covered by this License; they are outside its scope. The act of running the Program is not restricted, and the output from the Program is covered only if its contents constitute a work based on the Program (independent of having been made by running the Program). Whether that is true depends on what the Program does.

<a id="a-p0015"></a>**A:p0015** (1. You may copy and distribute verbatim copies ...)

> 1. You may copy and distribute verbatim copies of the Program's source code as you receive it, in any medium, provided that you conspicuously and appropriately publish on each copy an appropriate copyright notice and disclaimer of warranty; keep intact all the notices that refer to this License and to the absence of any warranty; and give any other recipients of the Program a copy of this License along with the Program.

<a id="a-p0016"></a>**A:p0016** (1. You may copy and distribute verbatim copies ...)

> You may charge a fee for the physical act of transferring a copy, and you may at your option offer warranty protection in exchange for a fee.

<a id="a-p0017"></a>**A:p0017** (2. You may modify your copy or copies ...)

> 2. You may modify your copy or copies of the Program or any portion of it, thus forming a work based on the Program, and copy and distribute such modifications or work under the terms of Section 1 above, provided that you also meet all of these conditions:

<a id="a-p0018"></a>**A:p0018** (2. You may modify your copy or copies ...)

> a) You must cause the modified files to carry prominent notices stating that you changed the files and the date of any change.

<a id="a-p0019"></a>**A:p0019** (2. You may modify your copy or copies ...)

> b) You must cause any work that you distribute or publish, that in whole or in part contains or is derived from the Program or any part thereof, to be licensed as a whole at no charge to all third parties under the terms of this License.

<a id="a-p0020"></a>**A:p0020** (2. You may modify your copy or copies ...)

> c) If the modified program normally reads commands interactively when run, you must cause it, when started running for such interactive use in the most ordinary way, to print or display an announcement including an appropriate copyright notice and a notice that there is no warranty (or else, saying that you provide a warranty) and that users may redistribute the program under these conditions, and telling the user how to view a copy of this License. (Exception: if the Program itself is interactive but does not normally print such an announcement, your work based on the Program is not required to print an announcement.)

<a id="a-p0021"></a>**A:p0021** (2. You may modify your copy or copies ...)

> These requirements apply to the modified work as a whole. If identifiable sections of that work are not derived from the Program, and can be reasonably considered independent and separate works in themselves, then this License, and its terms, do not apply to those sections when you distribute them as separate works. But when you distribute the same sections as part of a whole which is a work based on the Program, the distribution of the whole must be on the terms of this License, whose permissions for other licensees extend to the entire whole, and thus to each and every part regardless of who wrote it.

<a id="a-p0022"></a>**A:p0022** (2. You may modify your copy or copies ...)

> Thus, it is not the intent of this section to claim rights or contest your rights to work written entirely by you; rather, the intent is to exercise the right to control the distribution of derivative or collective works based on the Program.

<a id="a-p0023"></a>**A:p0023** (2. You may modify your copy or copies ...)

> In addition, mere aggregation of another work not based on the Program with the Program (or with a work based on the Program) on a volume of a storage or distribution medium does not bring the other work under the scope of this License.

<a id="a-p0024"></a>**A:p0024** (3. You may copy and distribute the Program ...)

> 3. You may copy and distribute the Program (or a work based on it, under Section 2) in object code or executable form under the terms of Sections 1 and 2 above provided that you also do one of the following:

<a id="a-p0025"></a>**A:p0025** (3. You may copy and distribute the Program ...)

> a) Accompany it with the complete corresponding machine-readable source code, which must be distributed under the terms of Sections 1 and 2 above on a medium customarily used for software interchange; or,

<a id="a-p0026"></a>**A:p0026** (3. You may copy and distribute the Program ...)

> b) Accompany it with a written offer, valid for at least three years, to give any third party, for a charge no more than your cost of physically performing source distribution, a complete machine-readable copy of the corresponding source code, to be distributed under the terms of Sections 1 and 2 above on a medium customarily used for software interchange; or,

<a id="a-p0027"></a>**A:p0027** (3. You may copy and distribute the Program ...)

> c) Accompany it with the information you received as to the offer to distribute corresponding source code. (This alternative is allowed only for noncommercial distribution and only if you received the program in object code or executable form with such an offer, in accord with Subsection b above.)

<a id="a-p0028"></a>**A:p0028** (3. You may copy and distribute the Program ...)

> The source code for a work means the preferred form of the work for making modifications to it. For an executable work, complete source code means all the source code for all modules it contains, plus any associated interface definition files, plus the scripts used to control compilation and installation of the executable. However, as a special exception, the source code distributed need not include anything that is normally distributed (in either source or binary form) with the major components (compiler, kernel, and so on) of the operating system on which the executable runs, unless that component itself accompanies the executable.

<a id="a-p0029"></a>**A:p0029** (3. You may copy and distribute the Program ...)

> If distribution of executable or object code is made by offering access to copy from a designated place, then offering equivalent access to copy the source code from the same place counts as distribution of the source code, even though third parties are not compelled to copy the source along with the object code.

<a id="a-p0030"></a>**A:p0030** (4. You may not copy, modify, sublicense, or ...)

> 4. You may not copy, modify, sublicense, or distribute the Program except as expressly provided under this License. Any attempt otherwise to copy, modify, sublicense or distribute the Program is void, and will automatically terminate your rights under this License. However, parties who have received copies, or rights, from you under this License will not have their licenses terminated so long as such parties remain in full compliance.

<a id="a-p0031"></a>**A:p0031** (5. You are not required to accept this ...)

> 5. You are not required to accept this License, since you have not signed it. However, nothing else grants you permission to modify or distribute the Program or its derivative works. These actions are prohibited by law if you do not accept this License. Therefore, by modifying or distributing the Program (or any work based on the Program), you indicate your acceptance of this License to do so, and all its terms and conditions for copying, distributing or modifying the Program or works based on it.

<a id="a-p0032"></a>**A:p0032** (6. Each time you redistribute the Program (or ...)

> 6. Each time you redistribute the Program (or any work based on the Program), the recipient automatically receives a license from the original licensor to copy, distribute or modify the Program subject to these terms and conditions. You may not impose any further restrictions on the recipients' exercise of the rights granted herein. You are not responsible for enforcing compliance by third parties to this License.

<a id="a-p0033"></a>**A:p0033** (7. If, as a consequence of a court ...)

> 7. If, as a consequence of a court judgment or allegation of patent infringement or for any other reason (not limited to patent issues), conditions are imposed on you (whether by court order, agreement or otherwise) that contradict the conditions of this License, they do not excuse you from the conditions of this License. If you cannot distribute so as to satisfy simultaneously your obligations under this License and any other pertinent obligations, then as a consequence you may not distribute the Program at all. For example, if a patent license would not permit royalty-free redistribution of the Program by all those who receive copies directly or indirectly through you, then the only way you could satisfy both it and this License would be to refrain entirely from distribution of the Program.

<a id="a-p0034"></a>**A:p0034** (7. If, as a consequence of a court ...)

> If any portion of this section is held invalid or unenforceable under any particular circumstance, the balance of the section is intended to apply and the section as a whole is intended to apply in other circumstances.

<a id="a-p0035"></a>**A:p0035** (7. If, as a consequence of a court ...)

> It is not the purpose of this section to induce you to infringe any patents or other property right claims or to contest validity of any such claims; this section has the sole purpose of protecting the integrity of the free software distribution system, which is implemented by public license practices. Many people have made generous contributions to the wide range of software distributed through that system in reliance on consistent application of that system; it is up to the author/donor to decide if he or she is willing to distribute software through any other system and a licensee cannot impose that choice.

<a id="a-p0036"></a>**A:p0036** (7. If, as a consequence of a court ...)

> This section is intended to make thoroughly clear what is believed to be a consequence of the rest of this License.

<a id="a-p0037"></a>**A:p0037** (8. If the distribution and/or use of the ...)

> 8. If the distribution and/or use of the Program is restricted in certain countries either by patents or by copyrighted interfaces, the original copyright holder who places the Program under this License may add an explicit geographical distribution limitation excluding those countries, so that distribution is permitted only in or among countries not thus excluded. In such case, this License incorporates the limitation as if written in the body of this License.

<a id="a-p0038"></a>**A:p0038** (9. The Free Software Foundation may publish revised ...)

> 9. The Free Software Foundation may publish revised and/or new versions of the General Public License from time to time. Such new versions will be similar in spirit to the present version, but may differ in detail to address new problems or concerns.

<a id="a-p0039"></a>**A:p0039** (9. The Free Software Foundation may publish revised ...)

> Each version is given a distinguishing version number. If the Program specifies a version number of this License which applies to it and "any later version", you have the option of following the terms and conditions either of that version or of any later version published by the Free Software Foundation. If the Program does not specify a version number of this License, you may choose any version ever published by the Free Software Foundation.

<a id="a-p0040"></a>**A:p0040** (10. If you wish to incorporate parts of ...)

> 10. If you wish to incorporate parts of the Program into other free programs whose distribution conditions are different, write to the author to ask for permission. For software which is copyrighted by the Free Software Foundation, write to the Free Software Foundation; we sometimes make exceptions for this. Our decision will be guided by the two goals of preserving the free status of all derivatives of our free software and of promoting the sharing and reuse of software generally.

<a id="a-p0041"></a>**A:p0041** (NO WARRANTY)

> NO WARRANTY

<a id="a-p0042"></a>**A:p0042** (11. BECAUSE THE PROGRAM IS LICENSED FREE OF ...)

> 11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

<a id="a-p0043"></a>**A:p0043** (12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE ...)

> 12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

<a id="a-p0047"></a>**A:p0047** (How to Apply These Terms to Your New Programs)

> To do so, attach the following notices to the program. It is safest to attach them to the start of each source file to most effectively convey the exclusion of warranty; and each file should have at least the "copyright" line and a pointer to where the full notice is found.

<a id="a-p0049"></a>**A:p0049** (How to Apply These Terms to Your New Programs)

> This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

<a id="a-p0051"></a>**A:p0051** (How to Apply These Terms to Your New Programs)

> You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

<a id="a-p0053"></a>**A:p0053** (How to Apply These Terms to Your New Programs)

> If the program is interactive, make it output a short notice like this when it starts in an interactive mode:

<a id="a-p0054"></a>**A:p0054** (How to Apply These Terms to Your New Programs)

> Gnomovision version 69, Copyright (C) year name of author Gnomovision comes with ABSOLUTELY NO WARRANTY; for details type `show w'. This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.

<a id="a-p0055"></a>**A:p0055** (How to Apply These Terms to Your New Programs)

> The hypothetical commands `show w' and `show c' should show the appropriate parts of the General Public License. Of course, the commands you use may be called something other than `show w' and `show c'; they could even be mouse-clicks or menu items--whatever suits your program.

<a id="a-p0056"></a>**A:p0056** (How to Apply These Terms to Your New Programs)

> You should also get your employer (if you work as a programmer) or your school, if any, to sign a "copyright disclaimer" for the program, if necessary. Here is a sample; alter the names:

<a id="a-p0057"></a>**A:p0057** (How to Apply These Terms to Your New Programs)

> Yoyodyne, Inc., hereby disclaims all copyright interest in the program `Gnomovision' (which makes passes at compilers) written by James Hacker.

<a id="a-p0058"></a>**A:p0058** (How to Apply These Terms to Your New Programs)

> <signature of Ty Coon>, 1 April 1989 Ty Coon, President of Vice

<a id="a-p0059"></a>**A:p0059** (How to Apply These Terms to Your New Programs)

> This General Public License does not permit incorporating your program into proprietary programs. If your program is a subroutine library, you may consider it more useful to permit linking proprietary applications with the library. If this is what you want to do, use the GNU Lesser General Public License instead of this License.

<a id="b-p0001"></a>**B:p0001** ((front matter))

> GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

<a id="b-p0002"></a>**B:p0002** ((front matter))

> Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/> Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

<a id="b-p0004"></a>**B:p0004** (Preamble)

> The GNU General Public License is a free, copyleft license for software and other kinds of works.

<a id="b-p0005"></a>**B:p0005** (Preamble)

> The licenses for most software and other practical works are designed to take away your freedom to share and change the works. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change all versions of a program--to make sure it remains free software for all its users. We, the Free Software Foundation, use the GNU General Public License for most of our software; it applies also to any other work released this way by its authors. You can apply it to your programs, too.

<a id="b-p0006"></a>**B:p0006** (Preamble)

> When we speak of free software, we are referring to freedom, not price. Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for them if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs, and that you know you can do these things.

<a id="b-p0007"></a>**B:p0007** (Preamble)

> To protect your rights, we need to prevent others from denying you these rights or asking you to surrender the rights. Therefore, you have certain responsibilities if you distribute copies of the software, or if you modify it: responsibilities to respect the freedom of others.

<a id="b-p0008"></a>**B:p0008** (Preamble)

> For example, if you distribute copies of such a program, whether gratis or for a fee, you must pass on to the recipients the same freedoms that you received. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights.

<a id="b-p0009"></a>**B:p0009** (Preamble)

> Developers that use the GNU GPL protect your rights with two steps: (1) assert copyright on the software, and (2) offer you this License giving you legal permission to copy, distribute and/or modify it.

<a id="b-p0010"></a>**B:p0010** (Preamble)

> For the developers' and authors' protection, the GPL clearly explains that there is no warranty for this free software. For both users' and authors' sake, the GPL requires that modified versions be marked as changed, so that their problems will not be attributed erroneously to authors of previous versions.

<a id="b-p0011"></a>**B:p0011** (Preamble)

> Some devices are designed to deny users access to install or run modified versions of the software inside them, although the manufacturer can do so. This is fundamentally incompatible with the aim of protecting users' freedom to change the software. The systematic pattern of such abuse occurs in the area of products for individuals to use, which is precisely where it is most unacceptable. Therefore, we have designed this version of the GPL to prohibit the practice for those products. If such problems arise substantially in other domains, we stand ready to extend this provision to those domains in future versions of the GPL, as needed to protect the freedom of users.

<a id="b-p0012"></a>**B:p0012** (Preamble)

> Finally, every program is threatened constantly by software patents. States should not allow patents to restrict development and use of software on general-purpose computers, but in those that do, we wish to avoid the special danger that patents applied to a free program could make it effectively proprietary. To prevent this, the GPL assures that patents cannot be used to render the program non-free.

<a id="b-p0014"></a>**B:p0014** (TERMS AND CONDITIONS)

> TERMS AND CONDITIONS

<a id="b-p0015"></a>**B:p0015** (0. Definitions.)

> 0. Definitions.

<a id="b-p0016"></a>**B:p0016** (0. Definitions.)

> "This License" refers to version 3 of the GNU General Public License.

<a id="b-p0017"></a>**B:p0017** (0. Definitions.)

> "Copyright" also means copyright-like laws that apply to other kinds of works, such as semiconductor masks.

<a id="b-p0018"></a>**B:p0018** (0. Definitions.)

> "The Program" refers to any copyrightable work licensed under this License. Each licensee is addressed as "you". "Licensees" and "recipients" may be individuals or organizations.

<a id="b-p0019"></a>**B:p0019** (0. Definitions.)

> To "modify" a work means to copy from or adapt all or part of the work in a fashion requiring copyright permission, other than the making of an exact copy. The resulting work is called a "modified version" of the earlier work or a work "based on" the earlier work.

<a id="b-p0020"></a>**B:p0020** (0. Definitions.)

> A "covered work" means either the unmodified Program or a work based on the Program.

<a id="b-p0021"></a>**B:p0021** (0. Definitions.)

> To "propagate" a work means to do anything with it that, without permission, would make you directly or secondarily liable for infringement under applicable copyright law, except executing it on a computer or modifying a private copy. Propagation includes copying, distribution (with or without modification), making available to the public, and in some countries other activities as well.

<a id="b-p0022"></a>**B:p0022** (0. Definitions.)

> To "convey" a work means any kind of propagation that enables other parties to make or receive copies. Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying.

<a id="b-p0023"></a>**B:p0023** (0. Definitions.)

> An interactive user interface displays "Appropriate Legal Notices" to the extent that it includes a convenient and prominently visible feature that (1) displays an appropriate copyright notice, and (2) tells the user that there is no warranty for the work (except to the extent that warranties are provided), that licensees may convey the work under this License, and how to view a copy of this License. If the interface presents a list of user commands or options, such as a menu, a prominent item in the list meets this criterion.

<a id="b-p0024"></a>**B:p0024** (1. Source Code.)

> 1. Source Code.

<a id="b-p0025"></a>**B:p0025** (1. Source Code.)

> The "source code" for a work means the preferred form of the work for making modifications to it. "Object code" means any non-source form of a work.

<a id="b-p0026"></a>**B:p0026** (1. Source Code.)

> A "Standard Interface" means an interface that either is an official standard defined by a recognized standards body, or, in the case of interfaces specified for a particular programming language, one that is widely used among developers working in that language.

<a id="b-p0027"></a>**B:p0027** (1. Source Code.)

> The "System Libraries" of an executable work include anything, other than the work as a whole, that (a) is included in the normal form of packaging a Major Component, but which is not part of that Major Component, and (b) serves only to enable use of the work with that Major Component, or to implement a Standard Interface for which an implementation is available to the public in source code form. A "Major Component", in this context, means a major essential component (kernel, window system, and so on) of the specific operating system (if any) on which the executable work runs, or a compiler used to produce the work, or an object code interpreter used to run it.

<a id="b-p0028"></a>**B:p0028** (1. Source Code.)

> The "Corresponding Source" for a work in object code form means all the source code needed to generate, install, and (for an executable work) run the object code and to modify the work, including scripts to control those activities. However, it does not include the work's System Libraries, or general-purpose tools or generally available free programs which are used unmodified in performing those activities but which are not part of the work. For example, Corresponding Source includes interface definition files associated with source files for the work, and the source code for shared libraries and dynamically linked subprograms that the work is specifically designed to require, such as by intimate data communication or control flow between those subprograms and other parts of the work.

<a id="b-p0029"></a>**B:p0029** (1. Source Code.)

> The Corresponding Source need not include anything that users can regenerate automatically from other parts of the Corresponding Source.

<a id="b-p0030"></a>**B:p0030** (1. Source Code.)

> The Corresponding Source for a work in source code form is that same work.

<a id="b-p0031"></a>**B:p0031** (2. Basic Permissions.)

> 2. Basic Permissions.

<a id="b-p0032"></a>**B:p0032** (2. Basic Permissions.)

> All rights granted under this License are granted for the term of copyright on the Program, and are irrevocable provided the stated conditions are met. This License explicitly affirms your unlimited permission to run the unmodified Program. The output from running a covered work is covered by this License only if the output, given its content, constitutes a covered work. This License acknowledges your rights of fair use or other equivalent, as provided by copyright law.

<a id="b-p0033"></a>**B:p0033** (2. Basic Permissions.)

> You may make, run and propagate covered works that you do not convey, without conditions so long as your license otherwise remains in force. You may convey covered works to others for the sole purpose of having them make modifications exclusively for you, or provide you with facilities for running those works, provided that you comply with the terms of this License in conveying all material for which you do not control copyright. Those thus making or running the covered works for you must do so exclusively on your behalf, under your direction and control, on terms that prohibit them from making any copies of your copyrighted material outside their relationship with you.

<a id="b-p0034"></a>**B:p0034** (2. Basic Permissions.)

> Conveying under any other circumstances is permitted solely under the conditions stated below. Sublicensing is not allowed; section 10 makes it unnecessary.

<a id="b-p0035"></a>**B:p0035** (3. Protecting Users' Legal Rights From Anti-Circumvention Law.)

> 3. Protecting Users' Legal Rights From Anti-Circumvention Law.

<a id="b-p0036"></a>**B:p0036** (3. Protecting Users' Legal Rights From Anti-Circumvention Law.)

> No covered work shall be deemed part of an effective technological measure under any applicable law fulfilling obligations under article 11 of the WIPO copyright treaty adopted on 20 December 1996, or similar laws prohibiting or restricting circumvention of such measures.

<a id="b-p0037"></a>**B:p0037** (3. Protecting Users' Legal Rights From Anti-Circumvention Law.)

> When you convey a covered work, you waive any legal power to forbid circumvention of technological measures to the extent such circumvention is effected by exercising rights under this License with respect to the covered work, and you disclaim any intention to limit operation or modification of the work as a means of enforcing, against the work's users, your or third parties' legal rights to forbid circumvention of technological measures.

<a id="b-p0038"></a>**B:p0038** (4. Conveying Verbatim Copies.)

> 4. Conveying Verbatim Copies.

<a id="b-p0039"></a>**B:p0039** (4. Conveying Verbatim Copies.)

> You may convey verbatim copies of the Program's source code as you receive it, in any medium, provided that you conspicuously and appropriately publish on each copy an appropriate copyright notice; keep intact all notices stating that this License and any non-permissive terms added in accord with section 7 apply to the code; keep intact all notices of the absence of any warranty; and give all recipients a copy of this License along with the Program.

<a id="b-p0040"></a>**B:p0040** (4. Conveying Verbatim Copies.)

> You may charge any price or no price for each copy that you convey, and you may offer support or warranty protection for a fee.

<a id="b-p0041"></a>**B:p0041** (5. Conveying Modified Source Versions.)

> 5. Conveying Modified Source Versions.

<a id="b-p0042"></a>**B:p0042** (5. Conveying Modified Source Versions.)

> You may convey a work based on the Program, or the modifications to produce it from the Program, in the form of source code under the terms of section 4, provided that you also meet all of these conditions:

<a id="b-p0043"></a>**B:p0043** (5. Conveying Modified Source Versions.)

> a) The work must carry prominent notices stating that you modified it, and giving a relevant date.

<a id="b-p0044"></a>**B:p0044** (5. Conveying Modified Source Versions.)

> b) The work must carry prominent notices stating that it is released under this License and any conditions added under section 7. This requirement modifies the requirement in section 4 to "keep intact all notices".

<a id="b-p0045"></a>**B:p0045** (5. Conveying Modified Source Versions.)

> c) You must license the entire work, as a whole, under this License to anyone who comes into possession of a copy. This License will therefore apply, along with any applicable section 7 additional terms, to the whole of the work, and all its parts, regardless of how they are packaged. This License gives no permission to license the work in any other way, but it does not invalidate such permission if you have separately received it.

<a id="b-p0046"></a>**B:p0046** (5. Conveying Modified Source Versions.)

> d) If the work has interactive user interfaces, each must display Appropriate Legal Notices; however, if the Program has interactive interfaces that do not display Appropriate Legal Notices, your work need not make them do so.

<a id="b-p0047"></a>**B:p0047** (5. Conveying Modified Source Versions.)

> A compilation of a covered work with other separate and independent works, which are not by their nature extensions of the covered work, and which are not combined with it such as to form a larger program, in or on a volume of a storage or distribution medium, is called an "aggregate" if the compilation and its resulting copyright are not used to limit the access or legal rights of the compilation's users beyond what the individual works permit. Inclusion of a covered work in an aggregate does not cause this License to apply to the other parts of the aggregate.

<a id="b-p0048"></a>**B:p0048** (6. Conveying Non-Source Forms.)

> 6. Conveying Non-Source Forms.

<a id="b-p0049"></a>**B:p0049** (6. Conveying Non-Source Forms.)

> You may convey a covered work in object code form under the terms of sections 4 and 5, provided that you also convey the machine-readable Corresponding Source under the terms of this License, in one of these ways:

<a id="b-p0050"></a>**B:p0050** (6. Conveying Non-Source Forms.)

> a) Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by the Corresponding Source fixed on a durable physical medium customarily used for software interchange.

<a id="b-p0051"></a>**B:p0051** (6. Conveying Non-Source Forms.)

> b) Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by a written offer, valid for at least three years and valid for as long as you offer spare parts or customer support for that product model, to give anyone who possesses the object code either (1) a copy of the Corresponding Source for all the software in the product that is covered by this License, on a durable physical medium customarily used for software interchange, for a price no more than your reasonable cost of physically performing this conveying of source, or (2) access to copy the Corresponding Source from a network server at no charge.

<a id="b-p0052"></a>**B:p0052** (6. Conveying Non-Source Forms.)

> c) Convey individual copies of the object code with a copy of the written offer to provide the Corresponding Source. This alternative is allowed only occasionally and noncommercially, and only if you received the object code with such an offer, in accord with subsection 6b.

<a id="b-p0053"></a>**B:p0053** (6. Conveying Non-Source Forms.)

> d) Convey the object code by offering access from a designated place (gratis or for a charge), and offer equivalent access to the Corresponding Source in the same way through the same place at no further charge. You need not require recipients to copy the Corresponding Source along with the object code. If the place to copy the object code is a network server, the Corresponding Source may be on a different server (operated by you or a third party) that supports equivalent copying facilities, provided you maintain clear directions next to the object code saying where to find the Corresponding Source. Regardless of what server hosts the Corresponding Source, you remain obligated to ensure that it is available for as long as needed to satisfy these requirements.

<a id="b-p0054"></a>**B:p0054** (6. Conveying Non-Source Forms.)

> e) Convey the object code using peer-to-peer transmission, provided you inform other peers where the object code and Corresponding Source of the work are being offered to the general public at no charge under subsection 6d.

<a id="b-p0055"></a>**B:p0055** (6. Conveying Non-Source Forms.)

> A separable portion of the object code, whose source code is excluded from the Corresponding Source as a System Library, need not be included in conveying the object code work.

<a id="b-p0056"></a>**B:p0056** (6. Conveying Non-Source Forms.)

> A "User Product" is either (1) a "consumer product", which means any tangible personal property which is normally used for personal, family, or household purposes, or (2) anything designed or sold for incorporation into a dwelling. In determining whether a product is a consumer product, doubtful cases shall be resolved in favor of coverage. For a particular product received by a particular user, "normally used" refers to a typical or common use of that class of product, regardless of the status of the particular user or of the way in which the particular user actually uses, or expects or is expected to use, the product. A product is a consumer product regardless of whether the product has substantial commercial, industrial or non-consumer uses, unless such uses represent the only significant mode of use of the product.

<a id="b-p0057"></a>**B:p0057** (6. Conveying Non-Source Forms.)

> "Installation Information" for a User Product means any methods, procedures, authorization keys, or other information required to install and execute modified versions of a covered work in that User Product from a modified version of its Corresponding Source. The information must suffice to ensure that the continued functioning of the modified object code is in no case prevented or interfered with solely because modification has been made.

<a id="b-p0058"></a>**B:p0058** (6. Conveying Non-Source Forms.)

> If you convey an object code work under this section in, or with, or specifically for use in, a User Product, and the conveying occurs as part of a transaction in which the right of possession and use of the User Product is transferred to the recipient in perpetuity or for a fixed term (regardless of how the transaction is characterized), the Corresponding Source conveyed under this section must be accompanied by the Installation Information. But this requirement does not apply if neither you nor any third party retains the ability to install modified object code on the User Product (for example, the work has been installed in ROM).

<a id="b-p0059"></a>**B:p0059** (6. Conveying Non-Source Forms.)

> The requirement to provide Installation Information does not include a requirement to continue to provide support service, warranty, or updates for a work that has been modified or installed by the recipient, or for the User Product in which it has been modified or installed. Access to a network may be denied when the modification itself materially and adversely affects the operation of the network or violates the rules and protocols for communication across the network.

<a id="b-p0060"></a>**B:p0060** (6. Conveying Non-Source Forms.)

> Corresponding Source conveyed, and Installation Information provided, in accord with this section must be in a format that is publicly documented (and with an implementation available to the public in source code form), and must require no special password or key for unpacking, reading or copying.

<a id="b-p0061"></a>**B:p0061** (7. Additional Terms.)

> 7. Additional Terms.

<a id="b-p0062"></a>**B:p0062** (7. Additional Terms.)

> "Additional permissions" are terms that supplement the terms of this License by making exceptions from one or more of its conditions. Additional permissions that are applicable to the entire Program shall be treated as though they were included in this License, to the extent that they are valid under applicable law. If additional permissions apply only to part of the Program, that part may be used separately under those permissions, but the entire Program remains governed by this License without regard to the additional permissions.

<a id="b-p0063"></a>**B:p0063** (7. Additional Terms.)

> When you convey a copy of a covered work, you may at your option remove any additional permissions from that copy, or from any part of it. (Additional permissions may be written to require their own removal in certain cases when you modify the work.) You may place additional permissions on material, added by you to a covered work, for which you have or can give appropriate copyright permission.

<a id="b-p0064"></a>**B:p0064** (7. Additional Terms.)

> Notwithstanding any other provision of this License, for material you add to a covered work, you may (if authorized by the copyright holders of that material) supplement the terms of this License with terms:

<a id="b-p0065"></a>**B:p0065** (7. Additional Terms.)

> a) Disclaiming warranty or limiting liability differently from the terms of sections 15 and 16 of this License; or

<a id="b-p0066"></a>**B:p0066** (7. Additional Terms.)

> b) Requiring preservation of specified reasonable legal notices or author attributions in that material or in the Appropriate Legal Notices displayed by works containing it; or

<a id="b-p0067"></a>**B:p0067** (7. Additional Terms.)

> c) Prohibiting misrepresentation of the origin of that material, or requiring that modified versions of such material be marked in reasonable ways as different from the original version; or

<a id="b-p0068"></a>**B:p0068** (7. Additional Terms.)

> d) Limiting the use for publicity purposes of names of licensors or authors of the material; or

<a id="b-p0069"></a>**B:p0069** (7. Additional Terms.)

> e) Declining to grant rights under trademark law for use of some trade names, trademarks, or service marks; or

<a id="b-p0070"></a>**B:p0070** (7. Additional Terms.)

> f) Requiring indemnification of licensors and authors of that material by anyone who conveys the material (or modified versions of it) with contractual assumptions of liability to the recipient, for any liability that these contractual assumptions directly impose on those licensors and authors.

<a id="b-p0071"></a>**B:p0071** (7. Additional Terms.)

> All other non-permissive additional terms are considered "further restrictions" within the meaning of section 10. If the Program as you received it, or any part of it, contains a notice stating that it is governed by this License along with a term that is a further restriction, you may remove that term. If a license document contains a further restriction but permits relicensing or conveying under this License, you may add to a covered work material governed by the terms of that license document, provided that the further restriction does not survive such relicensing or conveying.

<a id="b-p0072"></a>**B:p0072** (7. Additional Terms.)

> If you add terms to a covered work in accord with this section, you must place, in the relevant source files, a statement of the additional terms that apply to those files, or a notice indicating where to find the applicable terms.

<a id="b-p0073"></a>**B:p0073** (7. Additional Terms.)

> Additional terms, permissive or non-permissive, may be stated in the form of a separately written license, or stated as exceptions; the above requirements apply either way.

<a id="b-p0074"></a>**B:p0074** (8. Termination.)

> 8. Termination.

<a id="b-p0075"></a>**B:p0075** (8. Termination.)

> You may not propagate or modify a covered work except as expressly provided under this License. Any attempt otherwise to propagate or modify it is void, and will automatically terminate your rights under this License (including any patent licenses granted under the third paragraph of section 11).

<a id="b-p0076"></a>**B:p0076** (8. Termination.)

> However, if you cease all violation of this License, then your license from a particular copyright holder is reinstated (a) provisionally, unless and until the copyright holder explicitly and finally terminates your license, and (b) permanently, if the copyright holder fails to notify you of the violation by some reasonable means prior to 60 days after the cessation.

<a id="b-p0077"></a>**B:p0077** (8. Termination.)

> Moreover, your license from a particular copyright holder is reinstated permanently if the copyright holder notifies you of the violation by some reasonable means, this is the first time you have received notice of violation of this License (for any work) from that copyright holder, and you cure the violation prior to 30 days after your receipt of the notice.

<a id="b-p0078"></a>**B:p0078** (8. Termination.)

> Termination of your rights under this section does not terminate the licenses of parties who have received copies or rights from you under this License. If your rights have been terminated and not permanently reinstated, you do not qualify to receive new licenses for the same material under section 10.

<a id="b-p0079"></a>**B:p0079** (9. Acceptance Not Required for Having Copies.)

> 9. Acceptance Not Required for Having Copies.

<a id="b-p0080"></a>**B:p0080** (9. Acceptance Not Required for Having Copies.)

> You are not required to accept this License in order to receive or run a copy of the Program. Ancillary propagation of a covered work occurring solely as a consequence of using peer-to-peer transmission to receive a copy likewise does not require acceptance. However, nothing other than this License grants you permission to propagate or modify any covered work. These actions infringe copyright if you do not accept this License. Therefore, by modifying or propagating a covered work, you indicate your acceptance of this License to do so.

<a id="b-p0081"></a>**B:p0081** (10. Automatic Licensing of Downstream Recipients.)

> 10. Automatic Licensing of Downstream Recipients.

<a id="b-p0082"></a>**B:p0082** (10. Automatic Licensing of Downstream Recipients.)

> Each time you convey a covered work, the recipient automatically receives a license from the original licensors, to run, modify and propagate that work, subject to this License. You are not responsible for enforcing compliance by third parties with this License.

<a id="b-p0083"></a>**B:p0083** (10. Automatic Licensing of Downstream Recipients.)

> An "entity transaction" is a transaction transferring control of an organization, or substantially all assets of one, or subdividing an organization, or merging organizations. If propagation of a covered work results from an entity transaction, each party to that transaction who receives a copy of the work also receives whatever licenses to the work the party's predecessor in interest had or could give under the previous paragraph, plus a right to possession of the Corresponding Source of the work from the predecessor in interest, if the predecessor has it or can get it with reasonable efforts.

<a id="b-p0084"></a>**B:p0084** (10. Automatic Licensing of Downstream Recipients.)

> You may not impose any further restrictions on the exercise of the rights granted or affirmed under this License. For example, you may not impose a license fee, royalty, or other charge for exercise of rights granted under this License, and you may not initiate litigation (including a cross-claim or counterclaim in a lawsuit) alleging that any patent claim is infringed by making, using, selling, offering for sale, or importing the Program or any portion of it.

<a id="b-p0085"></a>**B:p0085** (11. Patents.)

> 11. Patents.

<a id="b-p0086"></a>**B:p0086** (11. Patents.)

> A "contributor" is a copyright holder who authorizes use under this License of the Program or a work on which the Program is based. The work thus licensed is called the contributor's "contributor version".

<a id="b-p0087"></a>**B:p0087** (11. Patents.)

> A contributor's "essential patent claims" are all patent claims owned or controlled by the contributor, whether already acquired or hereafter acquired, that would be infringed by some manner, permitted by this License, of making, using, or selling its contributor version, but do not include claims that would be infringed only as a consequence of further modification of the contributor version. For purposes of this definition, "control" includes the right to grant patent sublicenses in a manner consistent with the requirements of this License.

<a id="b-p0088"></a>**B:p0088** (11. Patents.)

> Each contributor grants you a non-exclusive, worldwide, royalty-free patent license under the contributor's essential patent claims, to make, use, sell, offer for sale, import and otherwise run, modify and propagate the contents of its contributor version.

<a id="b-p0089"></a>**B:p0089** (11. Patents.)

> In the following three paragraphs, a "patent license" is any express agreement or commitment, however denominated, not to enforce a patent (such as an express permission to practice a patent or covenant not to sue for patent infringement). To "grant" such a patent license to a party means to make such an agreement or commitment not to enforce a patent against the party.

<a id="b-p0090"></a>**B:p0090** (11. Patents.)

> If you convey a covered work, knowingly relying on a patent license, and the Corresponding Source of the work is not available for anyone to copy, free of charge and under the terms of this License, through a publicly available network server or other readily accessible means, then you must either (1) cause the Corresponding Source to be so available, or (2) arrange to deprive yourself of the benefit of the patent license for this particular work, or (3) arrange, in a manner consistent with the requirements of this License, to extend the patent license to downstream recipients. "Knowingly relying" means you have actual knowledge that, but for the patent license, your conveying the covered work in a country, or your recipient's use of the covered work in a country, would infringe one or more identifiable patents in that country that you have reason to believe are valid.

<a id="b-p0091"></a>**B:p0091** (11. Patents.)

> If, pursuant to or in connection with a single transaction or arrangement, you convey, or propagate by procuring conveyance of, a covered work, and grant a patent license to some of the parties receiving the covered work authorizing them to use, propagate, modify or convey a specific copy of the covered work, then the patent license you grant is automatically extended to all recipients of the covered work and works based on it.

<a id="b-p0092"></a>**B:p0092** (11. Patents.)

> A patent license is "discriminatory" if it does not include within the scope of its coverage, prohibits the exercise of, or is conditioned on the non-exercise of one or more of the rights that are specifically granted under this License. You may not convey a covered work if you are a party to an arrangement with a third party that is in the business of distributing software, under which you make payment to the third party based on the extent of your activity of conveying the work, and under which the third party grants, to any of the parties who would receive the covered work from you, a discriminatory patent license (a) in connection with copies of the covered work conveyed by you (or copies made from those copies), or (b) primarily for and in connection with specific products or compilations that contain the covered work, unless you entered into that arrangement, or that patent license was granted, prior to 28 March 2007.

<a id="b-p0093"></a>**B:p0093** (11. Patents.)

> Nothing in this License shall be construed as excluding or limiting any implied license or other defenses to infringement that may otherwise be available to you under applicable patent law.

<a id="b-p0094"></a>**B:p0094** (12. No Surrender of Others' Freedom.)

> 12. No Surrender of Others' Freedom.

<a id="b-p0095"></a>**B:p0095** (12. No Surrender of Others' Freedom.)

> If conditions are imposed on you (whether by court order, agreement or otherwise) that contradict the conditions of this License, they do not excuse you from the conditions of this License. If you cannot convey a covered work so as to satisfy simultaneously your obligations under this License and any other pertinent obligations, then as a consequence you may not convey it at all. For example, if you agree to terms that obligate you to collect a royalty for further conveying from those to whom you convey the Program, the only way you could satisfy both those terms and this License would be to refrain entirely from conveying the Program.

<a id="b-p0096"></a>**B:p0096** (13. Use with the GNU Affero General Public License.)

> 13. Use with the GNU Affero General Public License.

<a id="b-p0097"></a>**B:p0097** (13. Use with the GNU Affero General Public License.)

> Notwithstanding any other provision of this License, you have permission to link or combine any covered work with a work licensed under version 3 of the GNU Affero General Public License into a single combined work, and to convey the resulting work. The terms of this License will continue to apply to the part which is the covered work, but the special requirements of the GNU Affero General Public License, section 13, concerning interaction through a network will apply to the combination as such.

<a id="b-p0098"></a>**B:p0098** (14. Revised Versions of this License.)

> 14. Revised Versions of this License.

<a id="b-p0099"></a>**B:p0099** (14. Revised Versions of this License.)

> The Free Software Foundation may publish revised and/or new versions of the GNU General Public License from time to time. Such new versions will be similar in spirit to the present version, but may differ in detail to address new problems or concerns.

<a id="b-p0100"></a>**B:p0100** (14. Revised Versions of this License.)

> Each version is given a distinguishing version number. If the Program specifies that a certain numbered version of the GNU General Public License "or any later version" applies to it, you have the option of following the terms and conditions either of that numbered version or of any later version published by the Free Software Foundation. If the Program does not specify a version number of the GNU General Public License, you may choose any version ever published by the Free Software Foundation.

<a id="b-p0101"></a>**B:p0101** (14. Revised Versions of this License.)

> If the Program specifies that a proxy can decide which future versions of the GNU General Public License can be used, that proxy's public statement of acceptance of a version permanently authorizes you to choose that version for the Program.

<a id="b-p0102"></a>**B:p0102** (14. Revised Versions of this License.)

> Later license versions may give you additional or different permissions. However, no additional obligations are imposed on any author or copyright holder as a result of your choosing to follow a later version.

<a id="b-p0103"></a>**B:p0103** (15. Disclaimer of Warranty.)

> 15. Disclaimer of Warranty.

<a id="b-p0104"></a>**B:p0104** (15. Disclaimer of Warranty.)

> THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

<a id="b-p0105"></a>**B:p0105** (16. Limitation of Liability.)

> 16. Limitation of Liability.

<a id="b-p0106"></a>**B:p0106** (16. Limitation of Liability.)

> IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

<a id="b-p0107"></a>**B:p0107** (17. Interpretation of Sections 15 and 16.)

> 17. Interpretation of Sections 15 and 16.

<a id="b-p0108"></a>**B:p0108** (17. Interpretation of Sections 15 and 16.)

> If the disclaimer of warranty and limitation of liability provided above cannot be given local legal effect according to their terms, reviewing courts shall apply local law that most closely approximates an absolute waiver of all civil liability in connection with the Program, unless a warranty or assumption of liability accompanies a copy of the Program in return for a fee.

<a id="b-p0112"></a>**B:p0112** (How to Apply These Terms to Your New Programs)

> To do so, attach the following notices to the program. It is safest to attach them to the start of each source file to most effectively state the exclusion of warranty; and each file should have at least the "copyright" line and a pointer to where the full notice is found.

<a id="b-p0114"></a>**B:p0114** (How to Apply These Terms to Your New Programs)

> This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

<a id="b-p0116"></a>**B:p0116** (How to Apply These Terms to Your New Programs)

> You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

<a id="b-p0118"></a>**B:p0118** (How to Apply These Terms to Your New Programs)

> If the program does terminal interaction, make it output a short notice like this when it starts in an interactive mode:

<a id="b-p0119"></a>**B:p0119** (How to Apply These Terms to Your New Programs)

> <program> Copyright (C) <year> <name of author> This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'. This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.

<a id="b-p0120"></a>**B:p0120** (How to Apply These Terms to Your New Programs)

> The hypothetical commands `show w' and `show c' should show the appropriate parts of the General Public License. Of course, your program's commands might be different; for a GUI interface, you would use an "about box".

<a id="b-p0121"></a>**B:p0121** (How to Apply These Terms to Your New Programs)

> You should also get your employer (if you work as a programmer) or school, if any, to sign a "copyright disclaimer" for the program, if necessary. For more information on this, and how to apply and follow the GNU GPL, see <https://www.gnu.org/licenses/>.

<a id="b-p0122"></a>**B:p0122** (How to Apply These Terms to Your New Programs)

> The GNU General Public License does not permit incorporating your program into proprietary programs. If your program is a subroutine library, you may consider it more useful to permit linking proprietary applications with the library. If this is what you want to do, use the GNU Lesser General Public License instead of this License. But first, please read <https://www.gnu.org/licenses/why-not-lgpl.html>.
