# Document diff report: planted-diff-workflow

| | |
|---|---|
| Mode | diff |
| Document A | `examples/planted/cc-by-4.0.txt` (79 paragraphs, sha256 `fd3a263fe19e`) |
| Document B | `examples/planted/cc-by-4.0-planted.txt` (80 paragraphs, sha256 `c6e691013a77`) |
| Runner / backend | workflow / claude-code |
| Alignment | equal 65, modified 12, inserted 2, deleted 1, moved 1 |

## Pipeline

| Stage | Result |
|---|---|
| Section-reader chunks | 2 |
| Findings emitted by agents | 24 |
| Rejected by the quote verifier | 3 (12.5%) |
| Deterministic sweep findings | 2 |
| Evidence match levels (accepted) | exact 49; re-attributed 0 |
| Findings after merge | 18 |
| Changed operations cited by a finding | first pass 12/16 (75.0%); with gap reader 13/16 (81.2%) |
| Skeptic 'missed' findings | 12 reported, 1 rejected, 11 duplicates attached |
| Skeptic verdicts | 18 (upheld 11, weakened 7); ungrounded refutations 0 |
| Final status | downgraded 7, upheld 11 |

## Summary

Version B makes several substantive changes to the public license compared with version A, and two of them are critical. The license grant in Section 2(a)(1) changes from irrevocable to revocable (F003), and the downstream-restrictions clause in Section 2(a)(5)(b) loses the word "not", so licensees may now impose extra terms or technological measures on recipients under a heading that still says the opposite (F008). Related inconsistencies with the non-binding preface and with the Adapted Material rules are recorded as lower-confidence follow-ons (F001, F007). The term and termination machinery is also damaged: Section 2(a)(3) now fixes a five-year term that conflicts with the unchanged Section 6(a) (F005, F004), the reinstatement clause points to a Section 9(a) that does not exist (F014), the cure period doubles from 30 to 60 days (F015), and Section 6 drops out of the survival list (F016). On the conditions side, B adds an undefined commercial-use notice requirement of 10 days (F012), deletes the Licensor's right to request removal of attribution and leaves a numbering gap where that item stood (F011, F010), and softens the database attribution duty from must to should (F013, F009). Two drafting changes blur defined terms: Adapted Material is narrowed to translated or altered material (F002), and the media-and-formats grant now uses the undefined term Granted Rights (F006). Section 7(a) swaps the parties so the protection against unagreed terms now runs to the licensee rather than the Licensor (F017). The relocation of the privileges-and-immunities clause from Section 8(d) to Section 7(c) has no effect on meaning and is informational only (F018). Several major findings (F001, F004, F007, F009, F016, F017) were downgraded by the skeptic because parts of their reasoning were overstated, so a reviewer should rely mainly on the core changes they identify.

- **License grant revocability and downstream restrictions**: F003, F008, F001, F007
- **Term, termination, reinstatement and survival**: F014, F005, F015, F004, F016
- **Conditions on Sharing and attribution duties**: F012, F011, F013, F009, F010
- **Definitions and defined terms**: F002, F006
- **Party roles and clause placement in other terms**: F017, F018

## Findings (18)

critical: 2, major: 14, minor: 1, info: 1

### F003 [critical] changed: Section 2(a)(1): license grant changed from irrevocable to revocable

Confidence 0.96 (upheld). Reported by reader-c01, skeptic-b02-v1:missed.

Version A grants a worldwide, royalty-free, non-sublicensable, non-exclusive, irrevocable license; version B makes the same grant revocable. This removes the licensee's core assurance that the Licensor cannot withdraw the permissions once granted. It also sits uneasily with Section 6(c), which still says the Licensor stopping distribution will not terminate this Public License.

- [A:p0023](#a-p0023) (exact): "non-exclusive, irrevocable license to exercise the Licensed Rights"
- [B:p0024](#b-p0024) (exact): "non-exclusive, revocable license to exercise the Licensed Rights"
- Skeptic skeptic-b01-v1: **upheld**. A p0023 grants an 'irrevocable' license and B p0024 grants a 'revocable' one, with the rest of the sentence unchanged. No other paragraph of B restores irrevocability in the operative text; the only remaining 'irrevocable' is in the non-binding preface. This changes whether the Licensor can withdraw the grant, so it is critical. I could not refute it.

### F008 [critical] changed: Section 2(a)(5)(b): prohibition on downstream restrictions turned into a permission

Confidence 0.96 (upheld). Reported by reader-c01, skeptic-b01-v1:missed.

Version A says You may not offer or impose additional terms or apply Effective Technological Measures if doing so restricts recipients' exercise of the Licensed Rights; version B says You may do so. This reverses a prohibition into a permission, letting licensees restrict downstream recipients. The heading "No downstream restrictions" is unchanged and now contradicts the operative text.

- [A:p0031](#a-p0031) (exact): "No downstream restrictions. You may not offer or impose any additional or different terms or conditions on"
- [B:p0032](#b-p0032) (exact): "No downstream restrictions. You may offer or impose any additional or different terms or conditions on"
- Skeptic skeptic-b02-v1: **upheld**. Compared A:p0031 with B:p0032 word by word. The only difference is the deletion of 'not', which turns a prohibition into a permission. The heading 'No downstream restrictions' is unchanged and now contradicts the operative text. No other provision in B restores the prohibition for the Licensed Material (Section 3(a)(4) covers only Adapted Material). Could not refute.

### F014 [major] broken_reference: Section 6(b): reinstatement cross-reference changed to non-existent Section 9(a)

Confidence 0.99 (upheld). Reported by crossref, reader-c01, skeptic-b01-v1:missed, sweep.

Version A ties reinstatement to termination under Section 6(a); version B refers to Section 9(a). Version B has only Sections 1 through 8, so the reference points to nothing. The reinstatement mechanism therefore no longer clearly applies to the automatic termination in Section 6(a).

- [A:p0064](#a-p0064) (exact): "has terminated under Section 6(a), it reinstates:"
- [A:p0069](#a-p0069) (exact): "d. Sections 1, 5, 6, 7, and 8 survive termination of this Public License."
- [B:p0065](#b-p0065) (exact): "has terminated under Section 9(a), it reinstates:"
- [B:p0065](#b-p0065) (exact): "Section 9(a)"
- [B:p0065](#b-p0065) (exact): "Where Your right to use the Licensed Material has terminated under Section 9(a), it reinstates:"
- [B:p0068](#b-p0068) (exact): "this Section 6(b) does not affect any right the Licensor may have to seek remedies for Your violations of this Public License."
- [B:p0070](#b-p0070) (exact): "d. Sections 1, 5, 7, and 8 survive termination of this Public License."
- Skeptic skeptic-b03-v1: **upheld**. B's headings run Section 1 (p0010) through Section 8 (p0075), with no Section 9, so 'Section 9(a)' in B p0065 resolves to nothing. B contains no remaining reference to Section 6(a) at all; even the Section 2(a)(3) term provision that pointed to 6(a) in A has been rewritten. So the link between automatic termination and reinstatement is broken. One weakness: the finding's evidence also cites the change to the survival list in p0070, which its description does not analyse. That is a separate change (reported below as missed), but it does not undercut the broken-reference claim.

### F005 [major] contradiction: Section 2(a)(3) term of five years in B conflicts with Section 6(a) term of the underlying rights

Confidence 0.97 (upheld). Reported by crossref, reader-c01, skeptic-b03-v1:missed.

In A, Section 2(a)(3) only pointed to Section 6(a) for the term. B replaces the pointer with a fixed term of five years from acceptance, but Section 6(a) was left unchanged and still says the license applies for the term of the Copyright and Similar Rights. B therefore states two different durations for the same license, and the cross-reference that kept them aligned is gone.

- [A:p0027](#a-p0027) (exact): "3. Term. The term of this Public License is specified in Section 6(a)."
- [B:p0028](#b-p0028) (exact): "3. Term. The term of this Public License is five years from the date You accept it."
- [B:p0028](#b-p0028) (exact): "The term of this Public License is five years from the date You accept it."
- [B:p0064](#b-p0064) (exact): "This Public License applies for the term of the Copyright and Similar Rights licensed here."
- Skeptic skeptic-b01-v1: **upheld**. B p0028 fixes the term at five years from acceptance, while B p0064 (identical to A p0063) still says the license applies for the term of the Copyright and Similar Rights. One could read 2(a)(3) as a specific rule that overrides 6(a), but the text gives no priority rule, and the A cross-reference that tied the two together is gone. B states two incompatible durations. I could not refute it.

### F012 [major] added: Section 3(a)(5): new 10-day advance written notice requirement for commercial Sharing

Confidence 0.94 (upheld). Reported by reader-c01, skeptic-b02-v1:missed.

Version B adds a new license condition: if You Share the Licensed Material for commercial purposes, You must notify the Licensor in writing at least 10 days in advance. Version A has no notice obligation and imposes no commercial/non-commercial distinction. The new condition burdens commercial reuse, and failing to meet it would be non-compliance that can trigger termination under Section 6(a). "Commercial purposes" is not defined anywhere in the license.

- [B:p0052](#b-p0052) (exact): "If You Share the Licensed Material for commercial purposes, You must notify the Licensor in writing at least 10 days in advance."
- Skeptic skeptic-b03-v1: **upheld**. B p0052 is a new Section 3(a)(5) with no counterpart in A. A case-insensitive search for 'commercial', 'notify' and 'in writing' finds nothing in A's license text. 'Commercial purposes' is not defined in B's Section 1, so the claim that it is undefined holds. Section 3 makes the exercise of the Licensed Rights 'expressly made subject to the following conditions', and B p0064 (6(a)) terminates rights automatically on any failure to comply, so the claim about termination exposure is correct. I found no basis to refute or weaken it.

### F011 [major] removed: Section 3(a)(3): Licensor's right to request removal of attribution information deleted

Confidence 0.93 (upheld). Reported by reader-c01, skeptic-b02-v1:missed.

Version A requires You, if requested by the Licensor, to remove information required by Section 3(a)(1)(A) to the extent reasonably practicable. Version B drops this provision entirely, so the Licensor can no longer require removal of its attribution, and licensees lose the corresponding obligation. The content does not appear elsewhere in B.

- [A:p0050](#a-p0050) (exact): "If requested by the Licensor, You must remove any of the information required by Section 3(a)(1)(A) to the extent reasonably practicable."
- Skeptic skeptic-b03-v1: **upheld**. A p0050 grants the Licensor a right to request removal of the Section 3(a)(1)(A) attribution information. I searched B for 'If requested by the Licensor', 'remove any of the information' and any other removal-on-request wording: none exists. B's Section 3(a) jumps from item 2 (p0050) to item 4 (p0051), confirming that item 3 was deleted, not moved or reworded. The Licensor's right and the licensee's matching obligation are both gone. Major is appropriate.

### F015 [major] changed: Section 6(b)(1): cure period for automatic reinstatement extended from 30 to 60 days

Confidence 0.96 (upheld). Reported by reader-c01, skeptic-b01-v1:missed.

In version A, rights reinstate automatically if the violation is cured within 30 days of discovery; in version B the window is 60 days. This doubles the time a licensee has to cure a violation and still get automatic reinstatement.

- [A:p0065](#a-p0065) (exact): "provided it is cured within 30 days of Your discovery of the violation"
- [B:p0066](#b-p0066) (exact): "provided it is cured within 60 days of Your discovery of the violation"
- Skeptic skeptic-b03-v1: **upheld**. A p0065 says 'within 30 days' and B p0066 says 'within 60 days'; the rest of the sentence is identical. No other cure period appears in either version. This is a substantive change to a duration that governs automatic reinstatement, so major is appropriate.

### F002 [major] changed: Section 1(a): definition of Adapted Material narrowed to translated or altered material

Confidence 0.91 (upheld). Reported by reader-c01.

Version A defines Adapted Material as material in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified. Version B keeps only translated or altered. Arrangements, transformations and other modifications may therefore fall outside the definition, which changes the scope of Section 2(a)(1)(b) and the Adapter's License rules in Section 3(a)(4).

- [A:p0010](#a-p0010) (exact): "translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission"
- [B:p0011](#b-p0011) (exact): "Licensed Material is translated or altered in a manner requiring permission"
- Skeptic skeptic-b01-v1: **upheld**. A p0010 lists 'translated, altered, arranged, transformed, or otherwise modified' and B p0011 keeps only 'translated or altered'. I searched B for 'arranged', 'transformed' and 'otherwise modified' and none of them appears elsewhere as a definition of Adapted Material. One could argue that 'altered' is broad enough to cover arrangements, but the catch-all 'otherwise modified' is gone, so the definition is narrower. The change affects Section 2(a)(1)(b) and Section 3(a)(4), which both depend on the defined term. I could not refute it.

### F006 [major] changed: Section 2(a)(4): grant now refers to undefined "Granted Rights" instead of the defined "Licensed Rights"

Confidence 0.89 (upheld). Reported by gap.

In A, Section 2(a)(4) authorizes You to exercise the Licensed Rights, a term defined in Section 1, in all media and formats. In B the same sentence says Granted Rights, a term that B defines nowhere, while the next sentence of the same paragraph still says Licensed Rights. The scope of the media-and-formats authorization is therefore unclear in B, and the paragraph is internally inconsistent.

- [A:p0028](#a-p0028) (exact): "The Licensor authorizes You to exercise the Licensed Rights in all media and formats"
- [B:p0029](#b-p0029) (exact): "The Licensor authorizes You to exercise the Granted Rights in all media and formats"
- Skeptic skeptic-b02-v1: **upheld**. Searched all of B: 'Granted Rights' occurs only in B:p0029; Section 1 of B defines 'Licensed Rights' (B:p0017) but not 'Granted Rights'. A:p0028 uses the defined term. The second sentence of the same B paragraph still says 'Licensed Rights', so the paragraph is internally inconsistent. One could argue a reader would equate 'Granted Rights' with the definition 'the rights granted to You', but the term is still undefined in an operative grant clause. Could not refute.

### F013 [major] changed: Section 4(c): database attribution obligation weakened from "must" to "should"

Confidence 0.93 (upheld). Reported by reader-c01.

Version A says You must comply with the Section 3(a) conditions when Sharing all or a substantial portion of the database contents; version B says You should comply. This turns a mandatory attribution condition for sui generis database contents into a recommendation, so a reader could share database contents without attribution.

- [A:p0056](#a-p0056) (exact): "c. You must comply with the conditions in Section 3(a)"
- [B:p0057](#b-p0057) (exact): "c. You should comply with the conditions in Section 3(a)"
- Skeptic skeptic-b03-v1: **upheld**. A p0056 says 'must comply' and B p0057 says 'should comply'; otherwise the two sentences are identical. One partial counter-argument is that Section 3(a)(1) still applies by its own terms whenever You Share the Licensed Material, and B p0058 says Section 4 'does not replace Your obligations'. That makes the practical effect ambiguous rather than a clean removal of attribution for database contents. Still, the specific Section 4(c) condition is demoted from mandatory to advisory and the text is now internally inconsistent, so the finding stands as stated at major.

### F017 [major] changed: Section 7(a): parties swapped, so the protection against unagreed additional terms now runs to You instead of the Licensor

Confidence 0.57 (downgraded, severity lowered from critical). Reported by reader-c02.

In A, Section 7(a) says the Licensor is not bound by additional or different terms that You communicate unless it expressly agrees. In B the roles are reversed: You are not bound by additional or different terms that the Licensor communicates. The protection the clause gives the Licensor is gone, and B gives a new protection to the licensee. This changes who is bound by what between the parties, and a reader would act on it.

- [A:p0071](#a-p0071) (exact): "The Licensor shall not be bound by any additional or different terms or conditions communicated by You unless expressly agreed."
- [B:p0072](#b-p0072) (exact): "You shall not be bound by any additional or different terms or conditions communicated by the Licensor unless expressly agreed."
- Skeptic skeptic-b04-v1: **weakened**. The party swap is real and is not editorial: A protects the Licensor against terms communicated by You, and B instead protects You against terms communicated by the Licensor. But 'critical' overstates it. The rubric lists a change of 'party' under major, and critical is for grants, prohibitions, termination or liability. In practice the Licensor is still largely protected elsewhere in B: Section 7(b) keeps any arrangement not stated in the license separate from and independent of it, and Section 8(c) still says no term is waived unless the Licensor expressly agrees. Both versions also keep the 'unless expressly agreed' qualifier, which matches the general rule that unilateral terms do not bind without agreement. So the Licensor's practical exposure is limited. Real change; major, not critical.
  - counter-evidence [B:p0073](#b-p0073): "Any arrangements, understandings, or agreements regarding the Licensed Material not stated herein are separate from and independent of the terms and conditions of this Public License."
  - counter-evidence [B:p0078](#b-p0078): "No term or condition of this Public License will be waived and no failure to comply consented to unless expressly agreed to by the Licensor."

### F004 [major] changed: Section 2(a)(3): license term changed from Section 6(a) term to five years from acceptance

Confidence 0.55 (downgraded). Reported by reader-c01, skeptic-b02-v1:missed.

Version A defines the term by reference to Section 6(a), which ties it to the term of the Copyright and Similar Rights licensed. Version B instead fixes the term at five years from the date You accept it. This shortens the duration of the license grant and introduces an acceptance date that is not otherwise defined.

- [A:p0027](#a-p0027) (exact): "The term of this Public License is specified in Section 6(a)."
- [B:p0028](#b-p0028) (exact): "The term of this Public License is five years from the date You accept it."
- Skeptic skeptic-b01-v1: **weakened**. The core change is real: A p0027 points to Section 6(a), and B p0028 fixes the term at five years from acceptance. One supporting claim is partly wrong, though. The finding says the acceptance date 'is not otherwise defined', but B p0009 says that You accept the license by exercising the Licensed Rights. So acceptance has a defined trigger (first exercise), even though no explicit date is given. Severity stays major. Only the secondary claim is overstated.
  - counter-evidence [B:p0009](#b-p0009): "By exercising the Licensed Rights (defined below), You accept and agree to be bound by the terms and conditions of this Creative Commons Attribution 4.0 International Public License"

### F016 [major] changed: Section 6(d): Section 6 removed from the provisions that survive termination

Confidence 0.54 (downgraded). Reported by reader-c01, skeptic-b01-v1:missed, skeptic-b03-v1:missed.

Version A lists Sections 1, 5, 6, 7, and 8 as surviving termination; version B drops Section 6. As a result, the reinstatement terms in Section 6(b) and the Licensor's reserved remedies arguably no longer survive termination, which undercuts the reinstatement mechanism.

- [A:p0069](#a-p0069) (exact): "Sections 1, 5, 6, 7, and 8 survive termination"
- [B:p0070](#b-p0070) (exact): "Sections 1, 5, 7, and 8 survive termination"
- Skeptic skeptic-b04-v1: **weakened**. The core change is real: A lists Sections 1, 5, 6, 7 and 8 as surviving termination, B lists only 1, 5, 7 and 8, and no other paragraph of B restores survival of Section 6 (grep for 'surviv' finds only B:p0070). Losing survival of Section 6(b) does undercut post-termination reinstatement, so major severity is fair. However, the description is partly wrong when it says the Licensor's reserved remedies 'no longer survive termination': Section 6(b)'s closing sentence does not create or reserve any remedy, it only clarifies that 6(b) 'does not affect any right the Licensor may have' to seek remedies. Those remedies exist independently of the license text, so dropping Section 6 from the survival list does not remove them. Issue real, explanation overstated; severity kept at major.
  - counter-evidence [B:p0068](#b-p0068): "this Section 6(b) does not affect any right the Licensor may have to seek remedies for Your violations"
  - counter-evidence [B:p0070](#b-p0070): "Sections 1, 5, 7, and 8 survive termination of this Public License."

### F001 [major] contradiction: Section 2(a)(1) grant made 'revocable' in B, contradicting the irrevocability statement and Section 6(c)

Confidence 0.51 (downgraded, severity lowered from critical). Reported by crossref.

A granted an 'irrevocable' license; B's Section 2(a)(1) grants a 'revocable' one. The change was not carried through: the licensor considerations still state 'Our licenses are irrevocable', and Section 6(c) still says the Licensor stopping distribution 'will not terminate this Public License'. B gives no mechanism or grounds for revocation, so a reader cannot tell whether, or how, the Licensor may withdraw the grant.

- [A:p0023](#a-p0023) (exact): "non-sublicensable, non-exclusive, irrevocable license to exercise the Licensed Rights"
- [B:p0006](#b-p0006) (exact): "Our licenses are irrevocable."
- [B:p0024](#b-p0024) (exact): "non-sublicensable, non-exclusive, revocable license to exercise the Licensed Rights"
- [B:p0069](#b-p0069) (exact): "stop distributing the Licensed Material at any time; however, doing so will not terminate this Public License."
- Skeptic skeptic-b01-v1: **weakened**. The grant in B p0024 is indeed revocable while B p0006 still says the licenses are irrevocable, so an inconsistency exists. It is overstated, though. The 'Our licenses are irrevocable' sentence sits in the introductory considerations, which B p0005 says are informational only and do not form part of the license, so it does not bind against the operative grant. Section 6(c) does not conflict with revocability either: it covers the Licensor offering separate terms or stopping distribution, which is a different act from revoking the grant. The substantive change (irrevocable to revocable) is already reported as critical in F003. What is left is an inconsistency between the operative text and the non-binding preface, which is major, not critical.
  - counter-evidence [B:p0005](#b-p0005): "The following considerations are for informational purposes only, are not exhaustive, and do not form part of our licenses."
  - counter-evidence [B:p0069](#b-p0069): "offer the Licensed Material under separate terms or conditions or stop distributing the Licensed Material at any time; however, doing so will not terminate this Public License."

### F007 [major] contradiction: Section 2(a)(5)(b) now permits downstream restrictions, conflicting with Sections 2(a)(5)(a) and 3(a)(4)

Confidence 0.42 (downgraded, severity lowered from critical). Reported by crossref.

A prohibited You from imposing additional terms or Effective Technological Measures that restrict recipients; B turns this into a permission ('You may offer or impose') under the unchanged heading 'No downstream restrictions'. This conflicts with Section 2(a)(5)(a), under which every recipient automatically receives the Licensor's offer on this license's terms, and with Section 3(a)(4), which still forbids an Adapter's License from preventing recipients of Adapted Material from complying. B therefore restricts restrictions on recipients of Adapted Material but allows them on recipients of the Licensed Material itself.

- [A:p0031](#a-p0031) (exact): "b. No downstream restrictions. You may not offer or impose any additional or different terms"
- [B:p0031](#b-p0031) (exact): "Every recipient of the Licensed Material automatically receives an offer from the Licensor to exercise the Licensed Rights under the terms and conditions of this Public License."
- [B:p0032](#b-p0032) (exact): "You may offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient"
- [B:p0051](#b-p0051) (exact): "the Adapter's License You apply must not prevent recipients of the Adapted Material from complying with this Public License."
- Skeptic skeptic-b02-v1: **weakened**. The underlying change (may not -> may) and the clash with the unchanged heading are already reported by F008. The extra cross-section conflicts are overstated. Section 2(a)(5)(a) concerns the Licensor's own offer to every recipient, which terms You add do not withdraw, so there is tension but no logical contradiction. Section 3(a)(4) governs only the Adapter's License for Adapted Material, while 2(a)(5)(b) concerns the Licensed Material itself, so the two provisions cover different subjects. The finding admits this asymmetry. The Licensor also still waives any right to forbid circumvention of Effective Technological Measures. What remains is a policy anomaly and an inconsistency, not a contradiction that changes who may do what beyond F008.
  - counter-evidence [B:p0031](#b-p0031): "automatically receives an offer from the Licensor to exercise the Licensed Rights under the terms and conditions of this Public License"
  - counter-evidence [B:p0051](#b-p0051): "the Adapter's License You apply must not prevent recipients of the Adapted Material from complying with this Public License"
  - counter-evidence [B:p0032](#b-p0032): "apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights"
  - counter-evidence [B:p0029](#b-p0029): "including technical modifications necessary to circumvent Effective Technological Measures"

### F009 [major] contradiction: Section 4(c) softened to 'should comply', inconsistent with Section 3 preamble and Section 4 closing sentence

Confidence 0.36 (downgraded). Reported by crossref.

A required You to comply with the Section 3(a) conditions when Sharing all or a substantial portion of a database ('must'); B says You 'should' comply, which reads as advisory. Section 3 still states that all exercise of the Licensed Rights, which include Sui Generis Database Rights, is 'expressly made subject to' those conditions. The closing sentence of Section 4 still speaks of Your obligations. B is therefore unclear on whether attribution is mandatory for database sharing.

- [A:p0056](#a-p0056) (exact): "c. You must comply with the conditions in Section 3(a) if You Share"
- [B:p0039](#b-p0039) (exact): "Your exercise of the Licensed Rights is expressly made subject to the following conditions."
- [B:p0057](#b-p0057) (exact): "c. You should comply with the conditions in Section 3(a) if You Share all or a substantial portion of the contents of the database."
- [B:p0058](#b-p0058) (exact): "this Section 4 supplements and does not replace Your obligations under this Public License"
- Skeptic skeptic-b02-v1: **weakened**. The must -> should change in Section 4(c) is real, and it sits uneasily with the Section 3 preamble. But the claim that B leaves attribution for database sharing unclear is overstated. Section 3(a)(1) still says 'You must' for any Sharing of the Licensed Material, and the Licensed Material is defined to include a database, so the mandatory attribution duty still applies through Section 3. The closing sentence of Section 4 does not support the finding: it concerns 'other Copyright and Similar Rights', not the database obligation. What remains is a confusing internal inconsistency with limited practical effect, which still fits major under the rubric.
  - counter-evidence [B:p0041](#b-p0041): "1. If You Share the Licensed Material (including in modified form), You must:"
  - counter-evidence [B:p0016](#b-p0016): "Licensed Material means the artistic or literary work, database, or other material"
  - counter-evidence [B:p0058](#b-p0058): "where the Licensed Rights include other Copyright and Similar Rights"

### F010 [minor] omission: Numbering gap: item 3 is missing

Confidence 0.95 (upheld). Reported by reader-c01, skeptic-b03-v1:missed, sweep.

Item 4 follows the item before it, but 3 was expected; an item may have been deleted or the list renumbered incompletely.

- [B:p0050](#b-p0050) (exact): "2. You may satisfy the conditions in Section"
- [B:p0050](#b-p0050) (exact): "2. You may satisfy the conditions in Section 3(a)(1)"
- [B:p0051](#b-p0051) (exact): "4. If You Share Adapted Material You produce,"
- [B:p0051](#b-p0051) (exact): "4. If You Share Adapted Material You produce"
- Skeptic skeptic-b02-v1: **upheld**. In B, Section 3(a) goes from item 2 (p0050) straight to item 4 (p0051) and then item 5 (p0052). Item 3 exists in A (A:p0050) and is absent from B. The numbering gap is real. Minor is the right severity for the numbering defect itself. The substantive loss of item 3 is not covered here and is listed under missed.

### F018 [info] moved: Privileges-and-immunities clause moved from Section 8(d) (Interpretation) to Section 7(c) (Other Terms)

Confidence 0.58 (downgraded, severity lowered from minor). Reported by crossref, reader-c02.

The clause stating that nothing in the license limits or waives privileges and immunities was Section 8(d) in A. In B it is Section 7(c). Its wording is the same, so this is a move, not a deletion plus an insertion. Both sections remain in the survival list, so its effect is unchanged. Only citations to 'Section 8(d)' would break.

- [A:p0077](#a-p0077) (exact): "d. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities"
- [B:p0074](#b-p0074) (exact): "c. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities"
- Skeptic skeptic-b04-v1: **weakened**. The move is correctly identified: the privileges-and-immunities sentence is word-for-word identical in A Section 8(d) and B Section 7(c), and A Section 8 is otherwise unchanged as B Section 8(a)-(c), so there is no numbering gap. However, the finding itself says the effect is unchanged, and that is right: both Sections 7 and 8 are still in B's survival list, and moving the clause from 'Interpretation' to 'Other Terms and Conditions' does not change what it means. The only consequence it names is that citations to 'Section 8(d)' would break, but neither A nor B cites Section 8(d) anywhere (a search for internal Section cross-references finds none), so nothing inside the document breaks. This is relocation or renumbering with no change in meaning, which is info at most, not minor.
  - counter-evidence [A:p0077](#a-p0077): "d. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities that apply to the Licensor or You"
  - counter-evidence [B:p0074](#b-p0074): "c. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities that apply to the Licensor or You"
  - counter-evidence [B:p0070](#b-p0070): "Sections 1, 5, 7, and 8 survive termination of this Public License."

## Rejected by the quote verifier (4)

| Agent | Kind | Title | Reason |
|---|---|---|---|
| reader-c01 | undefined_term | Section 2(a)(4): "Licensed Rights" replaced by undefined term "Granted Rights" | kind_not_allowed_in_diff_mode: undefined_term |
| crossref | undefined_term | Section 2(a)(4) uses undefined term 'Granted Rights' instead of the defined term 'Licensed | kind_not_allowed_in_diff_mode: undefined_term |
| crossref | undefined_term | New Section 3(a)(5) notice duty relies on undefined 'commercial purposes' and reaches data | kind_not_allowed_in_diff_mode: undefined_term |
| skeptic-b01-v1:missed | undefined_term | Section 2(a)(4): 'Licensed Rights' replaced by undefined term 'Granted Rights' | kind_not_allowed_in_diff_mode: undefined_term |

## Cited paragraphs

<a id="a-p0010"></a>**A:p0010** (Section 1 -- Definitions.)

> a. Adapted Material means material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material and in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission under the Copyright and Similar Rights held by the Licensor. For purposes of this Public License, where the Licensed Material is a musical work, performance, or sound recording, Adapted Material is always produced where the Licensed Material is synched in timed relation with a moving image.

<a id="a-p0023"></a>**A:p0023** (Section 2 -- Scope.)

> 1. Subject to the terms and conditions of this Public License, the Licensor hereby grants You a worldwide, royalty-free, non-sublicensable, non-exclusive, irrevocable license to exercise the Licensed Rights in the Licensed Material to:

<a id="a-p0027"></a>**A:p0027** (Section 2 -- Scope.)

> 3. Term. The term of this Public License is specified in Section 6(a).

<a id="a-p0028"></a>**A:p0028** (Section 2 -- Scope.)

> 4. Media and formats; technical modifications allowed. The Licensor authorizes You to exercise the Licensed Rights in all media and formats whether now known or hereafter created, and to make technical modifications necessary to do so. The Licensor waives and/or agrees not to assert any right or authority to forbid You from making technical modifications necessary to exercise the Licensed Rights, including technical modifications necessary to circumvent Effective Technological Measures. For purposes of this Public License, simply making modifications authorized by this Section 2(a) (4) never produces Adapted Material.

<a id="a-p0031"></a>**A:p0031** (Section 2 -- Scope.)

> b. No downstream restrictions. You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient of the Licensed Material.

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

<a id="b-p0005"></a>**B:p0005** (Using Creative Commons Public Licenses)

> Creative Commons public licenses provide a standard set of terms and conditions that creators and other rights holders may use to share original works of authorship and other material subject to copyright and certain other rights specified in the public license below. The following considerations are for informational purposes only, are not exhaustive, and do not form part of our licenses.

<a id="b-p0006"></a>**B:p0006** (Using Creative Commons Public Licenses)

> Considerations for licensors: Our public licenses are intended for use by those authorized to give the public permission to use material in ways otherwise restricted by copyright and certain other rights. Our licenses are irrevocable. Licensors should read and understand the terms and conditions of the license they choose before applying it. Licensors should also secure all rights necessary before applying our licenses so that the public can reuse the material as expected. Licensors should clearly mark any material not subject to the license. This includes other CC-licensed material, or material used under an exception or limitation to copyright. More considerations for licensors: wiki.creativecommons.org/Considerations_for_licensors

<a id="b-p0009"></a>**B:p0009** (Creative Commons Attribution 4.0 International Public License)

> By exercising the Licensed Rights (defined below), You accept and agree to be bound by the terms and conditions of this Creative Commons Attribution 4.0 International Public License (“Public License”). To the extent this Public License may be interpreted as a contract, You are granted the Licensed Rights in consideration of Your acceptance of these terms and conditions, and the Licensor grants You such rights in consideration of benefits the Licensor receives from making the Licensed Material available under these terms and conditions.

<a id="b-p0011"></a>**B:p0011** (Section 1 -- Definitions.)

> a. Adapted Material means material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material and in which the Licensed Material is translated or altered in a manner requiring permission under the Copyright and Similar Rights held by the Licensor. For purposes of this Public License, where the Licensed Material is a musical work, performance, or sound recording, Adapted Material is always produced where the Licensed Material is synched in timed relation with a moving image.

<a id="b-p0016"></a>**B:p0016** (Section 1 -- Definitions.)

> f. Licensed Material means the artistic or literary work, database, or other material to which the Licensor applied this Public License.

<a id="b-p0024"></a>**B:p0024** (Section 2 -- Scope.)

> 1. Subject to the terms and conditions of this Public License, the Licensor hereby grants You a worldwide, royalty-free, non-sublicensable, non-exclusive, revocable license to exercise the Licensed Rights in the Licensed Material to:

<a id="b-p0028"></a>**B:p0028** (Section 2 -- Scope.)

> 3. Term. The term of this Public License is five years from the date You accept it.

<a id="b-p0029"></a>**B:p0029** (Section 2 -- Scope.)

> 4. Media and formats; technical modifications allowed. The Licensor authorizes You to exercise the Granted Rights in all media and formats whether now known or hereafter created, and to make technical modifications necessary to do so. The Licensor waives and/or agrees not to assert any right or authority to forbid You from making technical modifications necessary to exercise the Licensed Rights, including technical modifications necessary to circumvent Effective Technological Measures. For purposes of this Public License, simply making modifications authorized by this Section 2(a) (4) never produces Adapted Material.

<a id="b-p0031"></a>**B:p0031** (Section 2 -- Scope.)

> a. Offer from the Licensor -- Licensed Material. Every recipient of the Licensed Material automatically receives an offer from the Licensor to exercise the Licensed Rights under the terms and conditions of this Public License.

<a id="b-p0032"></a>**B:p0032** (Section 2 -- Scope.)

> b. No downstream restrictions. You may offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient of the Licensed Material.

<a id="b-p0039"></a>**B:p0039** (Section 3 -- License Conditions.)

> Your exercise of the Licensed Rights is expressly made subject to the following conditions.

<a id="b-p0041"></a>**B:p0041** (Section 3 -- License Conditions.)

> 1. If You Share the Licensed Material (including in modified form), You must:

<a id="b-p0050"></a>**B:p0050** (Section 3 -- License Conditions.)

> 2. You may satisfy the conditions in Section 3(a)(1) in any reasonable manner based on the medium, means, and context in which You Share the Licensed Material. For example, it may be reasonable to satisfy the conditions by providing a URI or hyperlink to a resource that includes the required information.

<a id="b-p0051"></a>**B:p0051** (Section 3 -- License Conditions.)

> 4. If You Share Adapted Material You produce, the Adapter's License You apply must not prevent recipients of the Adapted Material from complying with this Public License.

<a id="b-p0052"></a>**B:p0052** (Section 3 -- License Conditions.)

> 5. If You Share the Licensed Material for commercial purposes, You must notify the Licensor in writing at least 10 days in advance.

<a id="b-p0057"></a>**B:p0057** (Section 4 -- Sui Generis Database Rights.)

> c. You should comply with the conditions in Section 3(a) if You Share all or a substantial portion of the contents of the database.

<a id="b-p0058"></a>**B:p0058** (Section 4 -- Sui Generis Database Rights.)

> For the avoidance of doubt, this Section 4 supplements and does not replace Your obligations under this Public License where the Licensed Rights include other Copyright and Similar Rights.

<a id="b-p0064"></a>**B:p0064** (Section 6 -- Term and Termination.)

> a. This Public License applies for the term of the Copyright and Similar Rights licensed here. However, if You fail to comply with this Public License, then Your rights under this Public License terminate automatically.

<a id="b-p0065"></a>**B:p0065** (Section 6 -- Term and Termination.)

> b. Where Your right to use the Licensed Material has terminated under Section 9(a), it reinstates:

<a id="b-p0066"></a>**B:p0066** (Section 6 -- Term and Termination.)

> 1. automatically as of the date the violation is cured, provided it is cured within 60 days of Your discovery of the violation; or

<a id="b-p0068"></a>**B:p0068** (Section 6 -- Term and Termination.)

> For the avoidance of doubt, this Section 6(b) does not affect any right the Licensor may have to seek remedies for Your violations of this Public License.

<a id="b-p0069"></a>**B:p0069** (Section 6 -- Term and Termination.)

> c. For the avoidance of doubt, the Licensor may also offer the Licensed Material under separate terms or conditions or stop distributing the Licensed Material at any time; however, doing so will not terminate this Public License.

<a id="b-p0070"></a>**B:p0070** (Section 6 -- Term and Termination.)

> d. Sections 1, 5, 7, and 8 survive termination of this Public License.

<a id="b-p0072"></a>**B:p0072** (Section 7 -- Other Terms and Conditions.)

> a. You shall not be bound by any additional or different terms or conditions communicated by the Licensor unless expressly agreed.

<a id="b-p0073"></a>**B:p0073** (Section 7 -- Other Terms and Conditions.)

> b. Any arrangements, understandings, or agreements regarding the Licensed Material not stated herein are separate from and independent of the terms and conditions of this Public License.

<a id="b-p0074"></a>**B:p0074** (Section 7 -- Other Terms and Conditions.)

> c. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities that apply to the Licensor or You, including from the legal processes of any jurisdiction or authority.

<a id="b-p0078"></a>**B:p0078** (Section 8 -- Interpretation.)

> c. No term or condition of this Public License will be waived and no failure to comply consented to unless expressly agreed to by the Licensor.
