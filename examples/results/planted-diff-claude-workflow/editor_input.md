# Editor input

Findings below survived quote verification and the skeptic stage. Severity and confidence are final.

## F003 [critical] changed (confidence 0.96, upheld)

**Section 2(a)(1): license grant changed from irrevocable to revocable**

Version A grants a worldwide, royalty-free, non-sublicensable, non-exclusive, irrevocable license; version B makes the same grant revocable. This removes the licensee's core assurance that the Licensor cannot withdraw the permissions once granted. It also sits uneasily with Section 6(c), which still says the Licensor stopping distribution will not terminate this Public License.

- [A:p0023] "non-exclusive, irrevocable license to exercise the Licensed Rights"
- [B:p0024] "non-exclusive, revocable license to exercise the Licensed Rights"
- skeptic (upheld): A p0023 grants an 'irrevocable' license and B p0024 grants a 'revocable' one, with the rest of the sentence unchanged. No other paragraph of B restores irrevocability in the operative text; the only remaining 'irrevocable' is in the non-binding preface. This changes whether the Licensor can withdraw the grant, so it is critical. I could not refute it.

## F008 [critical] changed (confidence 0.96, upheld)

**Section 2(a)(5)(b): prohibition on downstream restrictions turned into a permission**

Version A says You may not offer or impose additional terms or apply Effective Technological Measures if doing so restricts recipients' exercise of the Licensed Rights; version B says You may do so. This reverses a prohibition into a permission, letting licensees restrict downstream recipients. The heading "No downstream restrictions" is unchanged and now contradicts the operative text.

- [A:p0031] "No downstream restrictions. You may not offer or impose any additional or different terms or conditions on"
- [B:p0032] "No downstream restrictions. You may offer or impose any additional or different terms or conditions on"
- skeptic (upheld): Compared A:p0031 with B:p0032 word by word. The only difference is the deletion of 'not', which turns a prohibition into a permission. The heading 'No downstream restrictions' is unchanged and now contradicts the operative text. No other provision in B restores the prohibition for the Licensed Material (Section 3(a)(4) covers only Adapted Material). Could not refute.

## F014 [major] broken_reference (confidence 0.99, upheld)

**Section 6(b): reinstatement cross-reference changed to non-existent Section 9(a)**

Version A ties reinstatement to termination under Section 6(a); version B refers to Section 9(a). Version B has only Sections 1 through 8, so the reference points to nothing. The reinstatement mechanism therefore no longer clearly applies to the automatic termination in Section 6(a).

- [A:p0064] "has terminated under Section 6(a), it reinstates:"
- [A:p0069] "d. Sections 1, 5, 6, 7, and 8 survive termination of this Public License."
- [B:p0065] "has terminated under Section 9(a), it reinstates:"
- [B:p0065] "Section 9(a)"
- [B:p0065] "Where Your right to use the Licensed Material has terminated under Section 9(a), it reinstates:"
- [B:p0068] "this Section 6(b) does not affect any right the Licensor may have to seek remedies for Your violations of this Public License."
- [B:p0070] "d. Sections 1, 5, 7, and 8 survive termination of this Public License."
- skeptic (upheld): B's headings run Section 1 (p0010) through Section 8 (p0075), with no Section 9, so 'Section 9(a)' in B p0065 resolves to nothing. B contains no remaining reference to Section 6(a) at all; even the Section 2(a)(3) term provision that pointed to 6(a) in A has been rewritten. So the link between automatic termination and reinstatement is broken. One weakness: the finding's evidence also cites the change to the survival list in p0070, which its description does not analyse. That is a separate change (reported below as missed), but it does not undercut the broken-reference claim.

## F005 [major] contradiction (confidence 0.97, upheld)

**Section 2(a)(3) term of five years in B conflicts with Section 6(a) term of the underlying rights**

In A, Section 2(a)(3) only pointed to Section 6(a) for the term. B replaces the pointer with a fixed term of five years from acceptance, but Section 6(a) was left unchanged and still says the license applies for the term of the Copyright and Similar Rights. B therefore states two different durations for the same license, and the cross-reference that kept them aligned is gone.

- [A:p0027] "3. Term. The term of this Public License is specified in Section 6(a)."
- [B:p0028] "3. Term. The term of this Public License is five years from the date You accept it."
- [B:p0028] "The term of this Public License is five years from the date You accept it."
- [B:p0064] "This Public License applies for the term of the Copyright and Similar Rights licensed here."
- skeptic (upheld): B p0028 fixes the term at five years from acceptance, while B p0064 (identical to A p0063) still says the license applies for the term of the Copyright and Similar Rights. One could read 2(a)(3) as a specific rule that overrides 6(a), but the text gives no priority rule, and the A cross-reference that tied the two together is gone. B states two incompatible durations. I could not refute it.

## F015 [major] changed (confidence 0.96, upheld)

**Section 6(b)(1): cure period for automatic reinstatement extended from 30 to 60 days**

In version A, rights reinstate automatically if the violation is cured within 30 days of discovery; in version B the window is 60 days. This doubles the time a licensee has to cure a violation and still get automatic reinstatement.

- [A:p0065] "provided it is cured within 30 days of Your discovery of the violation"
- [B:p0066] "provided it is cured within 60 days of Your discovery of the violation"
- skeptic (upheld): A p0065 says 'within 30 days' and B p0066 says 'within 60 days'; the rest of the sentence is identical. No other cure period appears in either version. This is a substantive change to a duration that governs automatic reinstatement, so major is appropriate.

## F012 [major] added (confidence 0.94, upheld)

**Section 3(a)(5): new 10-day advance written notice requirement for commercial Sharing**

Version B adds a new license condition: if You Share the Licensed Material for commercial purposes, You must notify the Licensor in writing at least 10 days in advance. Version A has no notice obligation and imposes no commercial/non-commercial distinction. The new condition burdens commercial reuse, and failing to meet it would be non-compliance that can trigger termination under Section 6(a). "Commercial purposes" is not defined anywhere in the license.

- [B:p0052] "If You Share the Licensed Material for commercial purposes, You must notify the Licensor in writing at least 10 days in advance."
- skeptic (upheld): B p0052 is a new Section 3(a)(5) with no counterpart in A. A case-insensitive search for 'commercial', 'notify' and 'in writing' finds nothing in A's license text. 'Commercial purposes' is not defined in B's Section 1, so the claim that it is undefined holds. Section 3 makes the exercise of the Licensed Rights 'expressly made subject to the following conditions', and B p0064 (6(a)) terminates rights automatically on any failure to comply, so the claim about termination exposure is correct. I found no basis to refute or weaken it.

## F011 [major] removed (confidence 0.93, upheld)

**Section 3(a)(3): Licensor's right to request removal of attribution information deleted**

Version A requires You, if requested by the Licensor, to remove information required by Section 3(a)(1)(A) to the extent reasonably practicable. Version B drops this provision entirely, so the Licensor can no longer require removal of its attribution, and licensees lose the corresponding obligation. The content does not appear elsewhere in B.

- [A:p0050] "If requested by the Licensor, You must remove any of the information required by Section 3(a)(1)(A) to the extent reasonably practicable."
- skeptic (upheld): A p0050 grants the Licensor a right to request removal of the Section 3(a)(1)(A) attribution information. I searched B for 'If requested by the Licensor', 'remove any of the information' and any other removal-on-request wording: none exists. B's Section 3(a) jumps from item 2 (p0050) to item 4 (p0051), confirming that item 3 was deleted, not moved or reworded. The Licensor's right and the licensee's matching obligation are both gone. Major is appropriate.

## F013 [major] changed (confidence 0.93, upheld)

**Section 4(c): database attribution obligation weakened from "must" to "should"**

Version A says You must comply with the Section 3(a) conditions when Sharing all or a substantial portion of the database contents; version B says You should comply. This turns a mandatory attribution condition for sui generis database contents into a recommendation, so a reader could share database contents without attribution.

- [A:p0056] "c. You must comply with the conditions in Section 3(a)"
- [B:p0057] "c. You should comply with the conditions in Section 3(a)"
- skeptic (upheld): A p0056 says 'must comply' and B p0057 says 'should comply'; otherwise the two sentences are identical. One partial counter-argument is that Section 3(a)(1) still applies by its own terms whenever You Share the Licensed Material, and B p0058 says Section 4 'does not replace Your obligations'. That makes the practical effect ambiguous rather than a clean removal of attribution for database contents. Still, the specific Section 4(c) condition is demoted from mandatory to advisory and the text is now internally inconsistent, so the finding stands as stated at major.

## F002 [major] changed (confidence 0.91, upheld)

**Section 1(a): definition of Adapted Material narrowed to translated or altered material**

Version A defines Adapted Material as material in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified. Version B keeps only translated or altered. Arrangements, transformations and other modifications may therefore fall outside the definition, which changes the scope of Section 2(a)(1)(b) and the Adapter's License rules in Section 3(a)(4).

- [A:p0010] "translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission"
- [B:p0011] "Licensed Material is translated or altered in a manner requiring permission"
- skeptic (upheld): A p0010 lists 'translated, altered, arranged, transformed, or otherwise modified' and B p0011 keeps only 'translated or altered'. I searched B for 'arranged', 'transformed' and 'otherwise modified' and none of them appears elsewhere as a definition of Adapted Material. One could argue that 'altered' is broad enough to cover arrangements, but the catch-all 'otherwise modified' is gone, so the definition is narrower. The change affects Section 2(a)(1)(b) and Section 3(a)(4), which both depend on the defined term. I could not refute it.

## F006 [major] changed (confidence 0.89, upheld)

**Section 2(a)(4): grant now refers to undefined "Granted Rights" instead of the defined "Licensed Rights"**

In A, Section 2(a)(4) authorizes You to exercise the Licensed Rights, a term defined in Section 1, in all media and formats. In B the same sentence says Granted Rights, a term that B defines nowhere, while the next sentence of the same paragraph still says Licensed Rights. The scope of the media-and-formats authorization is therefore unclear in B, and the paragraph is internally inconsistent.

- [A:p0028] "The Licensor authorizes You to exercise the Licensed Rights in all media and formats"
- [B:p0029] "The Licensor authorizes You to exercise the Granted Rights in all media and formats"
- skeptic (upheld): Searched all of B: 'Granted Rights' occurs only in B:p0029; Section 1 of B defines 'Licensed Rights' (B:p0017) but not 'Granted Rights'. A:p0028 uses the defined term. The second sentence of the same B paragraph still says 'Licensed Rights', so the paragraph is internally inconsistent. One could argue a reader would equate 'Granted Rights' with the definition 'the rights granted to You', but the term is still undefined in an operative grant clause. Could not refute.

## F017 [major] changed (confidence 0.57, downgraded)

**Section 7(a): parties swapped, so the protection against unagreed additional terms now runs to You instead of the Licensor**

In A, Section 7(a) says the Licensor is not bound by additional or different terms that You communicate unless it expressly agrees. In B the roles are reversed: You are not bound by additional or different terms that the Licensor communicates. The protection the clause gives the Licensor is gone, and B gives a new protection to the licensee. This changes who is bound by what between the parties, and a reader would act on it.

- [A:p0071] "The Licensor shall not be bound by any additional or different terms or conditions communicated by You unless expressly agreed."
- [B:p0072] "You shall not be bound by any additional or different terms or conditions communicated by the Licensor unless expressly agreed."
- skeptic (weakened): The party swap is real and is not editorial: A protects the Licensor against terms communicated by You, and B instead protects You against terms communicated by the Licensor. But 'critical' overstates it. The rubric lists a change of 'party' under major, and critical is for grants, prohibitions, termination or liability. In practice the Licensor is still largely protected elsewhere in B: Section 7(b) keeps any arrangement not stated in the license separate from and independent of it, and Section 8(c) still says no term is waived unless the Licensor expressly agrees. Both versions also keep the 'unless expressly agreed' qualifier, which matches the general rule that unilateral terms do not bind without agreement. So the Licensor's practical exposure is limited. Real change; major, not critical.

## F004 [major] changed (confidence 0.55, downgraded)

**Section 2(a)(3): license term changed from Section 6(a) term to five years from acceptance**

Version A defines the term by reference to Section 6(a), which ties it to the term of the Copyright and Similar Rights licensed. Version B instead fixes the term at five years from the date You accept it. This shortens the duration of the license grant and introduces an acceptance date that is not otherwise defined.

- [A:p0027] "The term of this Public License is specified in Section 6(a)."
- [B:p0028] "The term of this Public License is five years from the date You accept it."
- skeptic (weakened): The core change is real: A p0027 points to Section 6(a), and B p0028 fixes the term at five years from acceptance. One supporting claim is partly wrong, though. The finding says the acceptance date 'is not otherwise defined', but B p0009 says that You accept the license by exercising the Licensed Rights. So acceptance has a defined trigger (first exercise), even though no explicit date is given. Severity stays major. Only the secondary claim is overstated.

## F016 [major] changed (confidence 0.54, downgraded)

**Section 6(d): Section 6 removed from the provisions that survive termination**

Version A lists Sections 1, 5, 6, 7, and 8 as surviving termination; version B drops Section 6. As a result, the reinstatement terms in Section 6(b) and the Licensor's reserved remedies arguably no longer survive termination, which undercuts the reinstatement mechanism.

- [A:p0069] "Sections 1, 5, 6, 7, and 8 survive termination"
- [B:p0070] "Sections 1, 5, 7, and 8 survive termination"
- skeptic (weakened): The core change is real: A lists Sections 1, 5, 6, 7 and 8 as surviving termination, B lists only 1, 5, 7 and 8, and no other paragraph of B restores survival of Section 6 (grep for 'surviv' finds only B:p0070). Losing survival of Section 6(b) does undercut post-termination reinstatement, so major severity is fair. However, the description is partly wrong when it says the Licensor's reserved remedies 'no longer survive termination': Section 6(b)'s closing sentence does not create or reserve any remedy, it only clarifies that 6(b) 'does not affect any right the Licensor may have' to seek remedies. Those remedies exist independently of the license text, so dropping Section 6 from the survival list does not remove them. Issue real, explanation overstated; severity kept at major.

## F001 [major] contradiction (confidence 0.51, downgraded)

**Section 2(a)(1) grant made 'revocable' in B, contradicting the irrevocability statement and Section 6(c)**

A granted an 'irrevocable' license; B's Section 2(a)(1) grants a 'revocable' one. The change was not carried through: the licensor considerations still state 'Our licenses are irrevocable', and Section 6(c) still says the Licensor stopping distribution 'will not terminate this Public License'. B gives no mechanism or grounds for revocation, so a reader cannot tell whether, or how, the Licensor may withdraw the grant.

- [A:p0023] "non-sublicensable, non-exclusive, irrevocable license to exercise the Licensed Rights"
- [B:p0006] "Our licenses are irrevocable."
- [B:p0024] "non-sublicensable, non-exclusive, revocable license to exercise the Licensed Rights"
- [B:p0069] "stop distributing the Licensed Material at any time; however, doing so will not terminate this Public License."
- skeptic (weakened): The grant in B p0024 is indeed revocable while B p0006 still says the licenses are irrevocable, so an inconsistency exists. It is overstated, though. The 'Our licenses are irrevocable' sentence sits in the introductory considerations, which B p0005 says are informational only and do not form part of the license, so it does not bind against the operative grant. Section 6(c) does not conflict with revocability either: it covers the Licensor offering separate terms or stopping distribution, which is a different act from revoking the grant. The substantive change (irrevocable to revocable) is already reported as critical in F003. What is left is an inconsistency between the operative text and the non-binding preface, which is major, not critical.

## F007 [major] contradiction (confidence 0.42, downgraded)

**Section 2(a)(5)(b) now permits downstream restrictions, conflicting with Sections 2(a)(5)(a) and 3(a)(4)**

A prohibited You from imposing additional terms or Effective Technological Measures that restrict recipients; B turns this into a permission ('You may offer or impose') under the unchanged heading 'No downstream restrictions'. This conflicts with Section 2(a)(5)(a), under which every recipient automatically receives the Licensor's offer on this license's terms, and with Section 3(a)(4), which still forbids an Adapter's License from preventing recipients of Adapted Material from complying. B therefore restricts restrictions on recipients of Adapted Material but allows them on recipients of the Licensed Material itself.

- [A:p0031] "b. No downstream restrictions. You may not offer or impose any additional or different terms"
- [B:p0031] "Every recipient of the Licensed Material automatically receives an offer from the Licensor to exercise the Licensed Rights under the terms and conditions of this Public License."
- [B:p0032] "You may offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient"
- [B:p0051] "the Adapter's License You apply must not prevent recipients of the Adapted Material from complying with this Public License."
- skeptic (weakened): The underlying change (may not -> may) and the clash with the unchanged heading are already reported by F008. The extra cross-section conflicts are overstated. Section 2(a)(5)(a) concerns the Licensor's own offer to every recipient, which terms You add do not withdraw, so there is tension but no logical contradiction. Section 3(a)(4) governs only the Adapter's License for Adapted Material, while 2(a)(5)(b) concerns the Licensed Material itself, so the two provisions cover different subjects. The finding admits this asymmetry. The Licensor also still waives any right to forbid circumvention of Effective Technological Measures. What remains is a policy anomaly and an inconsistency, not a contradiction that changes who may do what beyond F008.

## F009 [major] contradiction (confidence 0.36, downgraded)

**Section 4(c) softened to 'should comply', inconsistent with Section 3 preamble and Section 4 closing sentence**

A required You to comply with the Section 3(a) conditions when Sharing all or a substantial portion of a database ('must'); B says You 'should' comply, which reads as advisory. Section 3 still states that all exercise of the Licensed Rights, which include Sui Generis Database Rights, is 'expressly made subject to' those conditions. The closing sentence of Section 4 still speaks of Your obligations. B is therefore unclear on whether attribution is mandatory for database sharing.

- [A:p0056] "c. You must comply with the conditions in Section 3(a) if You Share"
- [B:p0039] "Your exercise of the Licensed Rights is expressly made subject to the following conditions."
- [B:p0057] "c. You should comply with the conditions in Section 3(a) if You Share all or a substantial portion of the contents of the database."
- [B:p0058] "this Section 4 supplements and does not replace Your obligations under this Public License"
- skeptic (weakened): The must -> should change in Section 4(c) is real, and it sits uneasily with the Section 3 preamble. But the claim that B leaves attribution for database sharing unclear is overstated. Section 3(a)(1) still says 'You must' for any Sharing of the Licensed Material, and the Licensed Material is defined to include a database, so the mandatory attribution duty still applies through Section 3. The closing sentence of Section 4 does not support the finding: it concerns 'other Copyright and Similar Rights', not the database obligation. What remains is a confusing internal inconsistency with limited practical effect, which still fits major under the rubric.

## F010 [minor] omission (confidence 0.95, upheld)

**Numbering gap: item 3 is missing**

Item 4 follows the item before it, but 3 was expected; an item may have been deleted or the list renumbered incompletely.

- [B:p0050] "2. You may satisfy the conditions in Section"
- [B:p0050] "2. You may satisfy the conditions in Section 3(a)(1)"
- [B:p0051] "4. If You Share Adapted Material You produce,"
- [B:p0051] "4. If You Share Adapted Material You produce"
- skeptic (upheld): In B, Section 3(a) goes from item 2 (p0050) straight to item 4 (p0051) and then item 5 (p0052). Item 3 exists in A (A:p0050) and is absent from B. The numbering gap is real. Minor is the right severity for the numbering defect itself. The substantive loss of item 3 is not covered here and is listed under missed.

## F018 [info] moved (confidence 0.58, downgraded)

**Privileges-and-immunities clause moved from Section 8(d) (Interpretation) to Section 7(c) (Other Terms)**

The clause stating that nothing in the license limits or waives privileges and immunities was Section 8(d) in A. In B it is Section 7(c). Its wording is the same, so this is a move, not a deletion plus an insertion. Both sections remain in the survival list, so its effect is unchanged. Only citations to 'Section 8(d)' would break.

- [A:p0077] "d. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities"
- [B:p0074] "c. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities"
- skeptic (weakened): The move is correctly identified: the privileges-and-immunities sentence is word-for-word identical in A Section 8(d) and B Section 7(c), and A Section 8 is otherwise unchanged as B Section 8(a)-(c), so there is no numbering gap. However, the finding itself says the effect is unchanged, and that is right: both Sections 7 and 8 are still in B's survival list, and moving the clause from 'Interpretation' to 'Other Terms and Conditions' does not change what it means. The only consequence it names is that citations to 'Section 8(d)' would break, but neither A nor B cites Section 8(d) anywhere (a search for internal Section cross-references finds none), so nothing inside the document breaks. This is relocation or renumbering with no change in meaning, which is info at most, not minor.
