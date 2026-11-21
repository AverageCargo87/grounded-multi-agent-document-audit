export const meta = {
  name: 'grounded-document-audit',
  description: 'Quote-verified multi-agent document audit or diff: section readers, a cross-reference checker, a gap reader, skeptics and an editor, with every deterministic step run by the docaudit CLI',
  whenToUse: 'After `python -m docaudit prepare ... --skeptic-batches 4` has written <run>/workflow_args.json; pass that JSON object as args',
  phases: [
    { title: 'Read', detail: 'section readers fan out over the prepared chunks' },
    { title: 'Cross-check', detail: 'one agent checks references, terms and values across the whole text' },
    { title: 'Verify', detail: 'docaudit verify: quote verification, merge, coverage, skeptic batches' },
    { title: 'Gaps', detail: 'diff mode: a second reader covers changes that no accepted finding cites' },
    { title: 'Skeptics', detail: 'one skeptic per batch tries to refute every finding' },
    { title: 'Recheck', detail: 'findings the skeptics reported as missed get their own skeptic pass' },
    { title: 'Edit', detail: 'docaudit aggregate, then the editor writes the synthesis' },
    { title: 'Report', detail: 'docaudit report: Markdown and JSON with paragraph links' },
  ],
}

// <generated:workflow-assets>
// Generated from docaudit/schemas.py and docaudit/prompts.py by
// `python -m docaudit export-workflow-assets`. Do not edit by hand.
const SCHEMAS = {
  "roles": {
    "section_reader": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "findings",
        "coverage_note"
      ],
      "properties": {
        "findings": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "kind",
              "title",
              "description",
              "severity",
              "confidence",
              "evidence"
            ],
            "properties": {
              "kind": {
                "type": "string",
                "enum": [
                  "added",
                  "removed",
                  "changed",
                  "moved",
                  "contradiction",
                  "inconsistent_value",
                  "broken_reference",
                  "undefined_term",
                  "ambiguity",
                  "omission",
                  "other"
                ]
              },
              "title": {
                "type": "string",
                "description": "One line, specific: what changed or what is wrong, and where."
              },
              "description": {
                "type": "string",
                "description": "Two to five sentences: the problem, why it matters, and for diff findings the before and after."
              },
              "severity": {
                "type": "string",
                "enum": [
                  "critical",
                  "major",
                  "minor",
                  "info"
                ]
              },
              "confidence": {
                "type": "number",
                "description": "0.0 to 1.0: probability that a careful reviewer accepts the finding as stated."
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "doc",
                    "para_id",
                    "quote"
                  ],
                  "properties": {
                    "doc": {
                      "type": "string",
                      "enum": [
                        "A",
                        "B"
                      ],
                      "description": "Document key: A (audit target or old version) or B (new version)."
                    },
                    "para_id": {
                      "type": "string",
                      "description": "Paragraph id exactly as shown, for example p0042."
                    },
                    "quote": {
                      "type": "string",
                      "description": "Verbatim text copied from that paragraph. '...' may join verbatim segments of two or more words."
                    }
                  }
                }
              }
            }
          }
        },
        "coverage_note": {
          "type": "string",
          "description": "What you checked, what you could not judge, and which changes you judged editorial (by op number or paragraph id)."
        }
      }
    },
    "cross_reference_checker": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "findings",
        "coverage_note"
      ],
      "properties": {
        "findings": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "kind",
              "title",
              "description",
              "severity",
              "confidence",
              "evidence"
            ],
            "properties": {
              "kind": {
                "type": "string",
                "enum": [
                  "added",
                  "removed",
                  "changed",
                  "moved",
                  "contradiction",
                  "inconsistent_value",
                  "broken_reference",
                  "undefined_term",
                  "ambiguity",
                  "omission",
                  "other"
                ]
              },
              "title": {
                "type": "string",
                "description": "One line, specific: what changed or what is wrong, and where."
              },
              "description": {
                "type": "string",
                "description": "Two to five sentences: the problem, why it matters, and for diff findings the before and after."
              },
              "severity": {
                "type": "string",
                "enum": [
                  "critical",
                  "major",
                  "minor",
                  "info"
                ]
              },
              "confidence": {
                "type": "number",
                "description": "0.0 to 1.0: probability that a careful reviewer accepts the finding as stated."
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "doc",
                    "para_id",
                    "quote"
                  ],
                  "properties": {
                    "doc": {
                      "type": "string",
                      "enum": [
                        "A",
                        "B"
                      ],
                      "description": "Document key: A (audit target or old version) or B (new version)."
                    },
                    "para_id": {
                      "type": "string",
                      "description": "Paragraph id exactly as shown, for example p0042."
                    },
                    "quote": {
                      "type": "string",
                      "description": "Verbatim text copied from that paragraph. '...' may join verbatim segments of two or more words."
                    }
                  }
                }
              }
            }
          }
        },
        "coverage_note": {
          "type": "string",
          "description": "What you checked, what you could not judge, and which changes you judged editorial (by op number or paragraph id)."
        }
      }
    },
    "gap_reader": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "findings",
        "coverage_note"
      ],
      "properties": {
        "findings": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "kind",
              "title",
              "description",
              "severity",
              "confidence",
              "evidence"
            ],
            "properties": {
              "kind": {
                "type": "string",
                "enum": [
                  "added",
                  "removed",
                  "changed",
                  "moved",
                  "contradiction",
                  "inconsistent_value",
                  "broken_reference",
                  "undefined_term",
                  "ambiguity",
                  "omission",
                  "other"
                ]
              },
              "title": {
                "type": "string",
                "description": "One line, specific: what changed or what is wrong, and where."
              },
              "description": {
                "type": "string",
                "description": "Two to five sentences: the problem, why it matters, and for diff findings the before and after."
              },
              "severity": {
                "type": "string",
                "enum": [
                  "critical",
                  "major",
                  "minor",
                  "info"
                ]
              },
              "confidence": {
                "type": "number",
                "description": "0.0 to 1.0: probability that a careful reviewer accepts the finding as stated."
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "doc",
                    "para_id",
                    "quote"
                  ],
                  "properties": {
                    "doc": {
                      "type": "string",
                      "enum": [
                        "A",
                        "B"
                      ],
                      "description": "Document key: A (audit target or old version) or B (new version)."
                    },
                    "para_id": {
                      "type": "string",
                      "description": "Paragraph id exactly as shown, for example p0042."
                    },
                    "quote": {
                      "type": "string",
                      "description": "Verbatim text copied from that paragraph. '...' may join verbatim segments of two or more words."
                    }
                  }
                }
              }
            }
          }
        },
        "coverage_note": {
          "type": "string",
          "description": "What you checked, what you could not judge, and which changes you judged editorial (by op number or paragraph id)."
        }
      }
    },
    "skeptic": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "verdicts",
        "missed"
      ],
      "properties": {
        "verdicts": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "finding_id",
              "verdict",
              "reason",
              "suggested_severity",
              "counter_evidence"
            ],
            "properties": {
              "finding_id": {
                "type": "string",
                "description": "Id of the finding under review, for example F007."
              },
              "verdict": {
                "type": "string",
                "enum": [
                  "upheld",
                  "weakened",
                  "refuted"
                ]
              },
              "reason": {
                "type": "string",
                "description": "What you checked and why the verdict follows."
              },
              "suggested_severity": {
                "type": "string",
                "enum": [
                  "critical",
                  "major",
                  "minor",
                  "info",
                  "keep"
                ]
              },
              "counter_evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "doc",
                    "para_id",
                    "quote"
                  ],
                  "properties": {
                    "doc": {
                      "type": "string",
                      "enum": [
                        "A",
                        "B"
                      ],
                      "description": "Document key: A (audit target or old version) or B (new version)."
                    },
                    "para_id": {
                      "type": "string",
                      "description": "Paragraph id exactly as shown, for example p0042."
                    },
                    "quote": {
                      "type": "string",
                      "description": "Verbatim text copied from that paragraph. '...' may join verbatim segments of two or more words."
                    }
                  }
                },
                "description": "Verbatim quotes that support a refuted or weakened verdict."
              }
            }
          }
        },
        "missed": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "kind",
              "title",
              "description",
              "severity",
              "confidence",
              "evidence"
            ],
            "properties": {
              "kind": {
                "type": "string",
                "enum": [
                  "added",
                  "removed",
                  "changed",
                  "moved",
                  "contradiction",
                  "inconsistent_value",
                  "broken_reference",
                  "undefined_term",
                  "ambiguity",
                  "omission",
                  "other"
                ]
              },
              "title": {
                "type": "string",
                "description": "One line, specific: what changed or what is wrong, and where."
              },
              "description": {
                "type": "string",
                "description": "Two to five sentences: the problem, why it matters, and for diff findings the before and after."
              },
              "severity": {
                "type": "string",
                "enum": [
                  "critical",
                  "major",
                  "minor",
                  "info"
                ]
              },
              "confidence": {
                "type": "number",
                "description": "0.0 to 1.0: probability that a careful reviewer accepts the finding as stated."
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "additionalProperties": false,
                  "required": [
                    "doc",
                    "para_id",
                    "quote"
                  ],
                  "properties": {
                    "doc": {
                      "type": "string",
                      "enum": [
                        "A",
                        "B"
                      ],
                      "description": "Document key: A (audit target or old version) or B (new version)."
                    },
                    "para_id": {
                      "type": "string",
                      "description": "Paragraph id exactly as shown, for example p0042."
                    },
                    "quote": {
                      "type": "string",
                      "description": "Verbatim text copied from that paragraph. '...' may join verbatim segments of two or more words."
                    }
                  }
                }
              }
            }
          },
          "description": "Substantive issues in the cited sections that no listed finding covers."
        }
      }
    },
    "editor": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "executive_summary",
        "themes",
        "ordered_finding_ids"
      ],
      "properties": {
        "executive_summary": {
          "type": "string"
        },
        "themes": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "title",
              "finding_ids"
            ],
            "properties": {
              "title": {
                "type": "string"
              },
              "finding_ids": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            }
          }
        },
        "ordered_finding_ids": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    }
  },
  "receipt": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "output_path",
      "valid",
      "n_items"
    ],
    "properties": {
      "output_path": {
        "type": "string"
      },
      "valid": {
        "type": "boolean",
        "description": "True only if the docaudit validate command printed OK for the file."
      },
      "n_items": {
        "type": "integer",
        "description": "Number of findings (or verdicts) written."
      }
    }
  },
  "shell": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "exit_code",
      "summary_json"
    ],
    "properties": {
      "exit_code": {
        "type": "integer"
      },
      "summary_json": {
        "type": "string",
        "description": "The last stdout line, copied exactly (it is a JSON object)."
      }
    }
  }
}
const ROLE_SYSTEM = {
  "section_reader": {
    "audit": "You are a section reader, one of several agents that each receive one chunk of the material. Work through the chunk item by item: every alignment operation (diff mode) or every paragraph (audit mode) in it must be considered, not sampled. Report each issue once, with the most specific evidence available. Other agents handle cross-section consistency, so focus on what is visible in your chunk, but do flag a cross-reference inside your chunk that looks wrong. In coverage_note, list anything you could not judge and every change you judged editorial (by op number), so a later check can tell skipped from dismissed.\n\nKinds in audit mode (one document, key A):\n- contradiction: two passages cannot both hold. Quote both.\n- inconsistent_value: the same quantity, date, list or name is given differently in different places. Quote each occurrence.\n- broken_reference: a cross-reference points to a section, clause or item that does not exist, or to one that says something else.\n- undefined_term: a capitalised or quoted term is used as a defined term but never defined, or is defined twice in different ways.\n- ambiguity: a sentence with two materially different readings. Quote it and state both readings.\n- omission: a list, numbering sequence or procedure that is visibly incomplete.\n- other: anything else a careful reviewer would flag. Use sparingly.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it.",
    "diff": "You are a section reader, one of several agents that each receive one chunk of the material. Work through the chunk item by item: every alignment operation (diff mode) or every paragraph (audit mode) in it must be considered, not sampled. Report each issue once, with the most specific evidence available. Other agents handle cross-section consistency, so focus on what is visible in your chunk, but do flag a cross-reference inside your chunk that looks wrong. In coverage_note, list anything you could not judge and every change you judged editorial (by op number), so a later check can tell skipped from dismissed.\n\nKinds in diff mode (A is the old version, B the new one):\n- added: content in B that A does not have. Quote B. The quoted B text must not occur anywhere in A (code checks this).\n- removed: content in A that B does not have. Quote A. The quoted A text must not occur anywhere in B (code checks this).\n- changed: the same provision exists in both versions with a different meaning. Quote both sides; the quotes themselves must show the difference.\n- moved: the same provision sits in a different place. Quote both sides.\n- broken_reference, contradiction, inconsistent_value, omission: the edit left version B internally inconsistent (for example a reference to a section that no longer exists, or a numbering gap).\nReport substantive changes: obligations, permissions, conditions, parties, scope, durations, amounts, definitions, references, remedies. Do not report purely editorial changes (spelling variants, punctuation, line wrapping, renumbering with no change in meaning). If you are unsure whether a change is editorial, report it with severity info.\nBefore you call something added or removed, check that the content does not appear elsewhere in the other version under different wording or in another section.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it."
  },
  "cross_reference_checker": {
    "audit": "You are the cross-reference checker. Section readers each saw one chunk; you see the whole text plus a deterministic index (outline, defined terms, cross-references with their resolution status, numeric expressions, and in diff mode the list of inserted and deleted paragraphs). Look for what chunk readers cannot see: contradictions between distant passages, values or lists that disagree across sections, references whose target exists but says something else, defined terms used inconsistently, and in diff mode content reported as added or removed that actually moved, plus edits in one place that were not carried through to the places that depend on them. Do not repeat local findings a chunk reader would obviously make.\n\nKinds in audit mode (one document, key A):\n- contradiction: two passages cannot both hold. Quote both.\n- inconsistent_value: the same quantity, date, list or name is given differently in different places. Quote each occurrence.\n- broken_reference: a cross-reference points to a section, clause or item that does not exist, or to one that says something else.\n- undefined_term: a capitalised or quoted term is used as a defined term but never defined, or is defined twice in different ways.\n- ambiguity: a sentence with two materially different readings. Quote it and state both readings.\n- omission: a list, numbering sequence or procedure that is visibly incomplete.\n- other: anything else a careful reviewer would flag. Use sparingly.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it.",
    "diff": "You are the cross-reference checker. Section readers each saw one chunk; you see the whole text plus a deterministic index (outline, defined terms, cross-references with their resolution status, numeric expressions, and in diff mode the list of inserted and deleted paragraphs). Look for what chunk readers cannot see: contradictions between distant passages, values or lists that disagree across sections, references whose target exists but says something else, defined terms used inconsistently, and in diff mode content reported as added or removed that actually moved, plus edits in one place that were not carried through to the places that depend on them. Do not repeat local findings a chunk reader would obviously make.\n\nKinds in diff mode (A is the old version, B the new one):\n- added: content in B that A does not have. Quote B. The quoted B text must not occur anywhere in A (code checks this).\n- removed: content in A that B does not have. Quote A. The quoted A text must not occur anywhere in B (code checks this).\n- changed: the same provision exists in both versions with a different meaning. Quote both sides; the quotes themselves must show the difference.\n- moved: the same provision sits in a different place. Quote both sides.\n- broken_reference, contradiction, inconsistent_value, omission: the edit left version B internally inconsistent (for example a reference to a section that no longer exists, or a numbering gap).\nReport substantive changes: obligations, permissions, conditions, parties, scope, durations, amounts, definitions, references, remedies. Do not report purely editorial changes (spelling variants, punctuation, line wrapping, renumbering with no change in meaning). If you are unsure whether a change is editorial, report it with severity info.\nBefore you call something added or removed, check that the content does not appear elsewhere in the other version under different wording or in another section.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it."
  },
  "gap_reader": {
    "audit": "You are the gap reader. A deterministic coverage check found changes that no accepted finding cites. These are exactly the places where a first pass is most likely to have skipped something. For every listed operation decide: substantive (report it as a finding) or editorial (name it in coverage_note with its op number and the reason). Do not skip any operation silently.\n\nKinds in audit mode (one document, key A):\n- contradiction: two passages cannot both hold. Quote both.\n- inconsistent_value: the same quantity, date, list or name is given differently in different places. Quote each occurrence.\n- broken_reference: a cross-reference points to a section, clause or item that does not exist, or to one that says something else.\n- undefined_term: a capitalised or quoted term is used as a defined term but never defined, or is defined twice in different ways.\n- ambiguity: a sentence with two materially different readings. Quote it and state both readings.\n- omission: a list, numbering sequence or procedure that is visibly incomplete.\n- other: anything else a careful reviewer would flag. Use sparingly.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it.",
    "diff": "You are the gap reader. A deterministic coverage check found changes that no accepted finding cites. These are exactly the places where a first pass is most likely to have skipped something. For every listed operation decide: substantive (report it as a finding) or editorial (name it in coverage_note with its op number and the reason). Do not skip any operation silently.\n\nKinds in diff mode (A is the old version, B the new one):\n- added: content in B that A does not have. Quote B. The quoted B text must not occur anywhere in A (code checks this).\n- removed: content in A that B does not have. Quote A. The quoted A text must not occur anywhere in B (code checks this).\n- changed: the same provision exists in both versions with a different meaning. Quote both sides; the quotes themselves must show the difference.\n- moved: the same provision sits in a different place. Quote both sides.\n- broken_reference, contradiction, inconsistent_value, omission: the edit left version B internally inconsistent (for example a reference to a section that no longer exists, or a numbering gap).\nReport substantive changes: obligations, permissions, conditions, parties, scope, durations, amounts, definitions, references, remedies. Do not report purely editorial changes (spelling variants, punctuation, line wrapping, renumbering with no change in meaning). If you are unsure whether a change is editorial, report it with severity info.\nBefore you call something added or removed, check that the content does not appear elsewhere in the other version under different wording or in another section.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it."
  },
  "skeptic": {
    "audit": "You are a skeptic. Your job is to refute findings, not to agree with them. For each finding in your batch, re-read the cited paragraphs and search the rest of the text, then give a verdict:\n- refuted: the finding is wrong. Typical reasons: the quote is misread, the change is editorial, the content exists elsewhere (so it was not added or removed), the reference resolves, the passages do not actually conflict.\n- weakened: the issue is real but overstated (lower severity, narrower scope, partly wrong). Use suggested_severity for the severity you would accept, or keep.\n- upheld: you tried to refute it and could not.\nA refuted or weakened verdict must carry counter_evidence: verbatim quotes that show why (the cited text itself counts when the finding misreads it). Code verifies these quotes too, and a refutation without verified counter-evidence is downgraded to weakened. When in doubt, do not uphold.\nThen list in missed any substantive issue in the cited sections that no finding in the batch covers, using the normal finding format. Missed findings get their own skeptic pass.\n\nKinds in audit mode (one document, key A):\n- contradiction: two passages cannot both hold. Quote both.\n- inconsistent_value: the same quantity, date, list or name is given differently in different places. Quote each occurrence.\n- broken_reference: a cross-reference points to a section, clause or item that does not exist, or to one that says something else.\n- undefined_term: a capitalised or quoted term is used as a defined term but never defined, or is defined twice in different ways.\n- ambiguity: a sentence with two materially different readings. Quote it and state both readings.\n- omission: a list, numbering sequence or procedure that is visibly incomplete.\n- other: anything else a careful reviewer would flag. Use sparingly.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it.",
    "diff": "You are a skeptic. Your job is to refute findings, not to agree with them. For each finding in your batch, re-read the cited paragraphs and search the rest of the text, then give a verdict:\n- refuted: the finding is wrong. Typical reasons: the quote is misread, the change is editorial, the content exists elsewhere (so it was not added or removed), the reference resolves, the passages do not actually conflict.\n- weakened: the issue is real but overstated (lower severity, narrower scope, partly wrong). Use suggested_severity for the severity you would accept, or keep.\n- upheld: you tried to refute it and could not.\nA refuted or weakened verdict must carry counter_evidence: verbatim quotes that show why (the cited text itself counts when the finding misreads it). Code verifies these quotes too, and a refutation without verified counter-evidence is downgraded to weakened. When in doubt, do not uphold.\nThen list in missed any substantive issue in the cited sections that no finding in the batch covers, using the normal finding format. Missed findings get their own skeptic pass.\n\nKinds in diff mode (A is the old version, B the new one):\n- added: content in B that A does not have. Quote B. The quoted B text must not occur anywhere in A (code checks this).\n- removed: content in A that B does not have. Quote A. The quoted A text must not occur anywhere in B (code checks this).\n- changed: the same provision exists in both versions with a different meaning. Quote both sides; the quotes themselves must show the difference.\n- moved: the same provision sits in a different place. Quote both sides.\n- broken_reference, contradiction, inconsistent_value, omission: the edit left version B internally inconsistent (for example a reference to a section that no longer exists, or a numbering gap).\nReport substantive changes: obligations, permissions, conditions, parties, scope, durations, amounts, definitions, references, remedies. Do not report purely editorial changes (spelling variants, punctuation, line wrapping, renumbering with no change in meaning). If you are unsure whether a change is editorial, report it with severity info.\nBefore you call something added or removed, check that the content does not appear elsewhere in the other version under different wording or in another section.\n\nSeverity:\n- critical: changes or breaks who may do what (grants, prohibitions, termination, liability) in a way a reader would act on.\n- major: changes a condition, duration, amount, scope, party or definition, or makes the text internally inconsistent.\n- minor: a narrow change or defect with limited practical effect.\n- info: editorial, or noted for completeness.\nconfidence is your probability (0.0 to 1.0) that a careful human reviewer would accept the finding exactly as stated.\n\nEvidence rules (code enforces them after you answer):\n1. Every finding needs at least one evidence item {doc, para_id, quote}.\n2. Copy the quote character for character from the paragraph text that follows its [doc:para_id] tag. Do not paraphrase, translate, correct typos or join text from two paragraphs. To shorten, join verbatim segments of two or more words with \"...\".\n3. Quote the words that show the problem, usually 5 to 40 words, not a whole page.\n4. A finding whose quote is not found in the cited paragraph is rejected automatically and counted as a failure of your stage. A quote found in a different paragraph is re-attributed and flagged.\n5. If you cannot quote it, do not report it."
  },
  "editor": {
    "audit": "You are the editor. You receive only findings that survived quote verification and the skeptic stage, with final severity and confidence already set by code. You may not add findings, change severities, or bring back refuted findings; code ignores any id that is not in your input. Write:\n- executive_summary: 5 to 10 plain sentences for a reviewer who has not read the documents. Refer to findings by id (for example F012). Quote the documents only verbatim, in double quotes, or not at all; code checks every quote of four or more words.\n- themes: groups of related finding ids with a short title.\n- ordered_finding_ids: every input id in the order a reviewer should read them (most consequential first).",
    "diff": "You are the editor. You receive only findings that survived quote verification and the skeptic stage, with final severity and confidence already set by code. You may not add findings, change severities, or bring back refuted findings; code ignores any id that is not in your input. Write:\n- executive_summary: 5 to 10 plain sentences for a reviewer who has not read the documents. Refer to findings by id (for example F012). Quote the documents only verbatim, in double quotes, or not at all; code checks every quote of four or more words.\n- themes: groups of related finding ids with a short title.\n- ordered_finding_ids: every input id in the order a reviewer should read them (most consequential first)."
  }
}
// </generated:workflow-assets>

// ---------------------------------------------------------------- arguments
// args is the object in <run>/workflow_args.json, written by `docaudit prepare`.
const A = args || {}
for (const key of ['runDir', 'repoDir', 'mode', 'chunks']) {
  if (A[key] === undefined || A[key] === null) {
    throw new Error(`args.${key} is required: pass the contents of <run>/workflow_args.json`)
  }
}
const RUN = String(A.runDir).replace(/\\/g, '/')
const REPO = String(A.repoDir).replace(/\\/g, '/')
const PY = A.python || 'python'
const MODE = A.mode
const VOTES = A.skepticVotes || 1
// 2 by default; args.maxConcurrent can lower it to 1 (it is never raised above 2)
const MAX_CONCURRENT = Math.max(1, Math.min(2, Number(A.maxConcurrent || 2)))
const DOCS = MODE === 'diff' ? `${RUN}/docs/A.md and ${RUN}/docs/B.md` : `${RUN}/docs/A.md`

// ---------------------------------------------------------------- concurrency
// At most MAX_CONCURRENT agents run at any moment, whatever the harness allows.
// A finishing task hands its slot directly to the next waiter, so the cap
// holds even when new tasks are queued in the same tick.
let active = 0
const waiting = []
async function limited(fn) {
  if (active < MAX_CONCURRENT) {
    active++
  } else {
    await new Promise(resolve => waiting.push(resolve))
  }
  try {
    return await fn()
  } finally {
    const next = waiting.shift()
    if (next) next()
    else active--
  }
}

// ---------------------------------------------------------------- steps
function command(sub) {
  return `cd "${REPO}" && ${PY} -m docaudit ${sub}`
}

// Deterministic core steps run as a shell command through a low-effort agent.
async function shell(label, phaseName, sub) {
  const cmd = command(sub)
  const prompt = `You are a build step, not an analyst. Run exactly this one command with the Bash tool:

<<<CMD
${cmd}
CMD>>>

Do not create, edit or delete any file yourself and do not run any other command. Return exit_code (the exit status of the command) and summary_json (the last line of its standard output, copied exactly; it is a JSON object).`
  const r = await limited(() => agent(prompt, { label, phase: phaseName, schema: SCHEMAS.shell, effort: 'low' }))
  if (!r) throw new Error(`${label}: the step returned nothing`)
  if (r.exit_code !== 0) throw new Error(`${label}: exit code ${r.exit_code}: ${r.summary_json}`)
  try {
    return JSON.parse(r.summary_json)
  } catch (e) {
    log(`${label}: could not parse the summary line, continuing without it`)
    return null
  }
}

function rolePrompt(role, inputRel, outputRel, task) {
  const docsLine = role === 'cross_reference_checker' || role === 'skeptic'
    ? `- The full numbered documents are ${DOCS}. Read them as needed; every quote must come from them.\n`
    : ''
  return `${ROLE_SYSTEM[role][MODE]}

HOW TO WORK IN THIS RUN
- Run directory: ${RUN}
- Your input is ${RUN}/${inputRel}. Read it with the Read tool. Paragraph texts follow tags such as [A:p0042].
${docsLine}- Task: ${task}
- Write your answer as ONE JSON object to ${RUN}/${outputRel} with the Write tool. It must match this JSON schema exactly (no extra keys):
${JSON.stringify(SCHEMAS.roles[role])}
- Then validate the file with the Bash tool:

<<<CMD
${command(`validate --role ${role} "${RUN}/${outputRel}"`)}
CMD>>>

  If it prints INVALID, fix the file and validate again until it prints OK.
- Do not modify any other file. Your final answer is a receipt: output_path, valid (true only after OK), n_items (number of findings or verdicts written).

ROLE: ${role}
INPUT_FILE: ${inputRel}
OUTPUT_FILE: ${outputRel}`
}

async function roleAgent(role, label, inputRel, phaseName, task) {
  const outputRel = `agents/${label}.json`
  const r = await limited(() => agent(rolePrompt(role, inputRel, outputRel, task), { label, phase: phaseName, schema: SCHEMAS.receipt }))
  if (!r || !r.valid) log(`${label}: no valid output; the core records it as an agent failure`)
  return r
}

// ---------------------------------------------------------------- run
phase('Read')
log(`${MODE} run, ${A.chunks.length} chunks, at most ${MAX_CONCURRENT} agents at a time`)
await parallel([
  ...A.chunks.map(id => () => roleAgent('section_reader', `reader-${id}`, `chunks/${id}.md`, 'Read', `Review chunk ${id} and report findings.`)),
  () => roleAgent('cross_reference_checker', 'crossref', 'index.md', 'Cross-check',
    'Using the full documents and the deterministic index, report cross-section findings.'),
])

phase('Verify')
let v = await shell('verify', 'Verify', `verify --run "${RUN}"`)
if (v) log(`verify: ${v.agent_findings} agent findings, ${v.rejected} rejected by the quote verifier, ${v.merged} after merge`)

if (MODE === 'diff' && (!v || v.uncovered > 0)) {
  phase('Gaps')
  await roleAgent('gap_reader', 'gap', 'gaps.md', 'Gaps', 'Classify every listed operation; report the substantive ones as findings.')
  v = await shell('verify-2', 'Gaps', `verify --run "${RUN}"`)
  if (v) log(`after gap reader: coverage ${v.coverage}, ${v.merged} findings`)
}

phase('Skeptics')
let batches = v && Array.isArray(v.batches) && v.batches.every(b => /^b\d{2}$/.test(b)) ? v.batches : null
if (!batches) {
  if (!A.skepticBatches) throw new Error('could not read the batch list from verify; prepare with --skeptic-batches N')
  batches = Array.from({ length: A.skepticBatches }, (_, i) => `b${String(i + 1).padStart(2, '0')}`)
}
const skeptics = []
for (const b of batches) {
  for (let k = 1; k <= VOTES; k++) {
    skeptics.push(() => roleAgent('skeptic', `skeptic-${b}-v${k}`, `skeptic/${b}.md`, 'Skeptics',
      'Try to refute every finding in this batch, then list what it missed.'))
  }
}
await parallel(skeptics)

phase('Recheck')
const rc = await shell('recheck-prep', 'Recheck', `recheck-prep --run "${RUN}"`)
if (!rc || rc.recheck_findings > 0) {
  await parallel(Array.from({ length: VOTES }, (_, i) => () => roleAgent('skeptic', `recheck-r01-v${i + 1}`, 'skeptic/r01.md', 'Recheck',
    'These findings were reported as missed by other skeptics. Try to refute each one.')))
} else {
  log('recheck: nothing to recheck')
}

phase('Edit')
await shell('aggregate', 'Edit', `aggregate --run "${RUN}"`)
await roleAgent('editor', 'editor', 'editor_input.md', 'Edit', 'Write the synthesis.')

phase('Report')
const rep = await shell('report', 'Report', `report --run "${RUN}" --runner workflow --backend claude-code`)
return { runDir: RUN, report: `${RUN}/report.md`, reportJson: `${RUN}/report.json`, summary: rep }
