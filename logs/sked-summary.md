# SKED Dialogue Log

**Document ID:** SKED-LOG-001
**Version:** 1.0
**Date:** 2026-10-04
**Status:** Final
**Related artifacts:** spec/srs.md v1.0, spec/traceability.md v1.0

---

## 1. Purpose

This document is a retrospective record of the requirements-engineering dialogue conducted for the Personal Media Library System using the SKED (Structured Knowledge Elicitation Dialogue) methodology. It records the major ambiguities identified during elicitation, the human decisions that resolved them, and the corrections made during validation. It does not itself create, modify, or extend any requirement. All normative content resides in `spec/srs.md`.

---

## 2. Initial System Concept

The original project idea (recorded in `spec/idea.md`) describes an information system for organising and storing consumed media content. The intended user is a single person who wants to keep track of the books, movies, TV series, articles, podcasts, videos, and other content they have consumed or plan to consume.

The system was conceived around two primary concerns. First, each piece of media can be recorded with basic information. Second, and more distinctively, media items can be grouped under user-defined topics so that related content from different media types can be collected together. A topic such as "Space Exploration" might contain a book, a documentary, and a podcast — all related to the same theme. The relationship between media items and topics was stated as working in both directions: from a topic to its items, and from an item to its topics.

A secondary feature of the original concept was personal notes attached to individual media items, allowing the user to record their thoughts, conclusions, or observations alongside the item.

The system was described as "a personal space," implying a single-user application with no sharing, collaboration, or external access. No platform, technology, or specific field list was specified in the original concept.

---

## 3. Major Uncertainties Identified

The following table records the important ambiguities that required clarification before a formal specification could be written. Only uncertainties that materially affected one or more approved decisions are included.

| Topic | Initial uncertainty | Why clarification was needed | Resolution |
|---|---|---|---|
| Delivery platform | Not specified | Platform determines the interaction model and feasibility of offline operation | HD-001 (desktop application, later generalised to platform-unresolved); HD-009, HD-047 |
| Single-user vs multi-user | Implied single-user but not stated | Determines whether authentication, profiles, or sharing must be in scope | HD-002, HD-003, HD-005, HD-007, HD-008 |
| Authentication | Not mentioned | Single-user local tool may or may not need a password | HD-004, HD-046 |
| Internet dependency | Not stated | Affects architecture and whether any online features are in scope | HD-006, HD-066, HD-067, HD-068 |
| "Basic information" on a media item | Explicitly vague in the original concept | Fields must be precisely defined before a schema can be specified | HD-011 |
| Media type list | "Other types" was open-ended | Whether the list is fixed or user-extensible determines the data model | HD-010 |
| Status field | Not mentioned in the original concept | Consumption lifecycle is central to a tracking application; values must be defined | HD-012, HD-021 |
| MediaItem–Topic relationship cardinality | Stated in the original concept but then contradicted by a human edit during a Git merge | A merge conflict arose between a one-to-many (human) and many-to-many (agent) version | HD-000 (resolved by conflict resolution log) |
| Type-specific fields | Not addressed | Different media types often have different metadata; uniform vs polymorphic schema is a fork | HD-014 |
| Note model | Described as free text but cardinality unspecified | Single text field vs multiple timestamped notes requires a different data model | HD-011, HD-019 |
| Topic attributes | Only name was implied | Whether topics have descriptions, colours, or other attributes affects the model | HD-015 |
| CRUD operations | Implied but not listed | Delete semantics and cascade behaviour must be explicitly decided | HD-016, HD-017, HD-018, HD-022 |
| Deletion cascade | Not addressed | When a MediaItem or Topic is deleted, what happens to the other side's data | HD-016, HD-022 |
| Search scope | Not addressed | Whether search covers only names, or also notes, types, and other fields | HD-025 |
| Search behavior | Not addressed | Exact match vs substring; case-sensitive vs insensitive | HD-026, HD-054 |
| Search result for Topic matches | Unspecified | Whether a matched Topic returns the Topic or its associated items or both | HD-055, Q-IR-01 |
| Filter types | Not addressed | Which dimensions (type, status, rating, topic) support filtering | HD-029 |
| Multi-filter logic | Not addressed | Whether simultaneous filters use AND or OR logic | HD-030 |
| Rating filter semantics | Not addressed | Whether rating filter is a minimum, maximum, exact value, or range | HD-035, HD-056, HD-057, HD-058 |
| Unrated items in rating filter | Not addressed | Whether an absent rating means the item is excluded or always shown | HD-036, HD-059 |
| Sort fields | Not addressed | Which fields support sorting | HD-031, HD-032 |
| Unrated items in rating sort | Not addressed | Where unrated items appear in a rating-sorted list | HD-060 |
| Tie-breaking in sort | Not addressed | Whether a secondary sort is required when values are equal | HD-061 |
| Name validation | "Basic information" implied a name; empty names were not considered | Systems must reject invalid input; exact rule must be specified | HD-048, HD-049 |
| Topic name uniqueness | Implied but not stated; case sensitivity not addressed | Uniqueness without case rules is ambiguous | HD-015, HD-050, HD-051 |
| Rating domain | Mentioned 1–10 range; boundary and absence semantics unspecified | Out-of-range rejection must be explicit; absence must be distinguished from a low value | HD-052 |
| Save model | Not addressed | Whether the user must explicitly save or changes are auto-saved | HD-042, HD-062 |
| Save failure behavior | Not addressed | If auto-save fails, what the user sees and whether data is lost | HD-063, HD-064, HD-065 |
| Persistence across sessions | Implied but not stated | Must be an explicit requirement for acceptance testing | Q-NFR-01 |
| Performance | Not addressed | Whether a qualitative or quantitative target is required | HD-041, Q-NFR-02 |
| Accessibility | Not addressed | Must be decided to know whether special requirements exist | HD-044 |
| Language | Not stated | Must be decided before specifying all user-facing text | HD-045 |
| Security and local data protection | Not addressed | Single-user offline tool may or may not need encryption | HD-046 |
| Deletion confirmation | Not addressed | Permanent deletion without confirmation is a usability risk | HD-040 |
| Empty Topic allowance | Not addressed | Whether a topic with no items is a valid state | HD-023 |
| Rating filter: one vs two bounds | Not addressed after range was chosen | Whether both bounds are always required or either can be omitted | HD-056 |
| Search results when query is empty | Not addressed | Must define whether empty query returns all or no results | HD-053 |

---

## 4. Human Decisions

The following table summarises the substantive decisions recorded during the SKED process as HD-000 through HD-068. Related decisions are grouped for readability. Every HD identifier is preserved for traceability.

| Decision IDs | Topic | Decision summary |
|---|---|---|
| HD-000 | MediaItem–Topic relationship | Many-to-many. One item may belong to zero or more Topics; one Topic may contain zero or more MediaItems. Confirmed by conflict resolution between human (one-to-many) and agent (many-to-many) versions. Many-to-many was retained. |
| HD-001 | Platform (initial) | System is a desktop application. (Later superseded by HD-009 and HD-047 when the platform was intentionally left unresolved.) |
| HD-002 | User model | Single local user. |
| HD-003, HD-005 | Profiles | Multiple local profiles and profile switching are not required. |
| HD-004, HD-046 | Authentication and security | No password required for any user or profile (HD-004). No authentication mechanism, no encryption at rest. Local data protection is the responsibility of the OS (HD-046). Note: HD-004 is subsumed by HD-046 in the SRS; both represent the same security non-requirement. |
| HD-006, HD-066, HD-067, HD-068 | Offline operation | Core functionality must work without Internet access. No network request is required for any in-scope operation. No connection-related UI. |
| HD-007, HD-008 | Multi-user and sharing | Authentication, account management, multi-user access, collaboration, and sharing are out of scope. |
| HD-009, HD-047 | Platform and technology stack | Intentionally unresolved. The specification is platform-independent. No OS, language, framework, database, or file format is assumed or required. |
| HD-010 | Media type set | Fixed predefined set for the current version: book, movie, TV series, article, podcast, video, other. Users cannot create custom types. The set may be extended by future development. |
| HD-011 | MediaItem fields | id, name (required), type, status, notes (optional free text), rating (optional 1–10), topics (zero or more). All types share the same fields. |
| HD-012, HD-021 | Status values and semantics | Five values: planned (not started), in progress (currently consuming), postponed (paused, intends to return), abandoned (stopped, no intent to return), completed (finished). No workflow enforcement. |
| HD-013 | Duplicate names | Duplicate MediaItem names are allowed. |
| HD-014 | Uniform field structure | All media types use the same fields. No type-specific fields in the current version. |
| HD-015, HD-023 | Topic model | A Topic has a unique name. Empty Topics (zero MediaItems) are allowed. |
| HD-016 | Topic deletion | Deleting a Topic removes the Topic and its associations only. Associated MediaItems are not deleted. |
| HD-017, HD-018 | CRUD operations | MediaItems support create, view, edit, delete. Topics support create, view, rename, delete. |
| HD-019 | Notes model | One optional free-text notes field per MediaItem. Notes are edited with the MediaItem. No separate notes subsystem. |
| HD-022 | MediaItem deletion | Permanent. Removes all Topic associations. Topics unaffected. No restore. |
| HD-024 | Topic rename | Renaming preserves all existing MediaItem associations. Uniqueness constraint applies to the new name. |
| HD-025, HD-026, HD-053, HD-054, HD-055 | Search | Covers MediaItem name and Topic name. Does not cover notes. Substring matching, case-insensitive. Empty query = search inactive. A matched Topic is returned as a Topic result and can be opened to view its MediaItems. Note: HD-028 (an intermediate decision during elicitation confirming this exact Topic-search behavior) is captured here and in HD-055. |
| HD-027, HD-034 | Out-of-scope features | External metadata retrieval, import/export, backup/restore, statistics, analytics, cloud sync, recommendations, notifications (other than save failure), undo/recycle bin, authentication, and account management are all out of scope. |
| HD-028 | Search result for Topic | A Topic matching the search query is returned as a Topic result; the user can open it to see its associated MediaItems. |
| HD-029, HD-030 | Filters | Required filters: type, status, rating, topic. Multiple simultaneous filters use AND logic. |
| HD-031, HD-032 | Sorting | Sort by name and rating. Ascending and descending. No date-added field. |
| HD-033 | Combined operations | Search, filters, and sorting can be active simultaneously. |
| HD-035, HD-036, HD-056, HD-057, HD-058, HD-059 | Rating filter | Arbitrary range (lower bound, upper bound, or both). Lower ≤ upper when both specified; invalid range rejected. Unrated items excluded when any rating filter is active. |
| HD-037 | MediaItem creation defaults | At creation: name required, type required, status defaults to planned, notes and rating optional, Topics may be assigned. |
| HD-038 | Association management | MediaItem–Topic associations can be managed from both sides. |
| HD-039 | Navigation | Both directions supported: Topic → MediaItems → individual MediaItem; MediaItem → Topics → individual Topic. |
| HD-040 | Deletion confirmation | Both MediaItem and Topic deletion require user confirmation before execution. |
| HD-041 | Performance | No hard quantitative target. Common operations must execute without perceptible delay at typical personal library scale. |
| HD-042, HD-062 | Auto-save | Application auto-saves every successful data change. No explicit Save action required. |
| HD-043 | Usability | The application must be usable for all main operations without requiring the user to read external documentation. |
| HD-044 | Accessibility | No special accessibility requirements for the current version. |
| HD-045 | Language | User-facing language is English. No multilingual support. |
| HD-048, HD-049 | MediaItem name validation | Name invalid if empty or whitespace-only after trimming. Leading/trailing whitespace removed before saving. |
| HD-050, HD-051 | Topic name uniqueness | Uniqueness is case-insensitive. Leading/trailing whitespace removed before saving and before uniqueness check. |
| HD-052 | Rating domain | Rating, when present, must be an integer 1–10. Values outside this range are rejected. Absence of rating is a distinct valid state. |
| HD-060 | Unrated items in sort | When sorting by rating, unrated MediaItems appear after all rated MediaItems in both ascending and descending directions. |
| HD-061 | Tie-breaking | No secondary sort order. Relative order within ties is unspecified. |
| HD-063, HD-064, HD-065 | Save failure | If auto-save fails, the user must be notified. The unsaved change remains available for the current session. The specification does not prescribe the retry or recovery mechanism. |

---

## 5. Model Assumptions That Were Corrected or Rejected

The following cases are supported by the project history and approved decisions. Only confirmed cases are included.

| Assumption or proposal | Human correction or rejection | Resulting decision |
|---|---|---|
| During a Git merge, the coding-agent version of `spec/idea.md` stated the many-to-many relationship explicitly. A separate human edit changed the description to say each media item should belong to one primary topic (one-to-many). | The conflict resolution log (`logs/conflict-resolution.md`) records that the many-to-many version was retained because the original project idea had already described the relationship working in both directions. The human's one-to-many edit was not accepted as the intended model. | HD-000: many-to-many relationship confirmed. |
| The specification initially included HD-001 (desktop application) as a confirmed platform decision. In a subsequent iteration, the human clarified that the exact platform was not yet finalized and should remain implementation-independent. | The human explicitly withdrew the desktop-specific constraint and requested that all requirements remain platform-independent. | HD-009, HD-047: platform and technology stack intentionally unresolved. |
| The NFR draft (initial version) contained 36 items, several of which restated already-approved functional requirements (e.g., auto-save, local persistence), included meta-notes about the specification process, and introduced an unconfirmed timing constraint ("before the user's next interaction with the affected data") for save-failure notification. | The human directed a strict NFR review, identifying that functional duplicates, scope restatements, and unconfirmed timing assumptions do not belong in non-functional requirements. | Revised NFR baseline reduced to 11 items; timing constraint removed; save-failure notification requirement preserved without timing prescription (REQ-NF-006, HD-065). |
| The initial BDD baseline included BDD-017 as a single scenario combining two sequential `When` actions (planned → abandoned, then abandoned → completed), which reduced independent executability. | The independent BDD consistency review identified this as a structural issue (ISSUE-003). | BDD-017 was split into BDD-017a and BDD-017b, each with one `When` action. |
| The initial BDD scenario BDD-058 used the Given clause "the next save operation will fail," which describes an internal implementation mechanism rather than an observable system state. | The independent BDD review identified this as an unsupported assumption (ISSUE-009). | The precondition was reworded to "a save failure condition is simulated at the test-environment level," making clear this is a test setup condition, not a system requirement. |

---

## 6. Scope Decisions

### In Scope (current version)

- MediaItem create, view, edit, delete
- Topic create, view, rename, delete
- MediaItem–Topic many-to-many association management from both sides
- Bidirectional navigation between MediaItems and Topics
- Status management (five values, free transitions)
- Search (name and Topic name, substring, case-insensitive)
- Filtering (type, status, rating range, topic) with AND logic
- Sorting (name, rating; ascending/descending)
- Combined search + filter + sort
- Automatic persistence of all successful changes
- Save-failure notification and in-session retention of unsaved change
- English-only user interface
- Single local user, no authentication

### Out of Scope (current version)

External metadata retrieval, data import, data export, built-in backup or restore, statistics, analytics, cloud synchronisation, recommendations, notifications other than save-failure notification, undo/redo/recycle bin, authentication, account management, multi-user access, collaboration, sharing, type-specific MediaItem fields, date-added field, multiple notes per MediaItem, notes search, secondary sort order, user-defined media types, multilingual support, special accessibility features, connection-related UI, application-level encryption or access control.

### Open Human Decisions

| Decision | Status |
|---|---|
| Target operating system and deployment platform | Unresolved (HD-009, HD-047). Requires an explicit human decision before implementation begins. |
| Technology stack (language, framework, database, file format) | Unresolved (HD-009, HD-047). Same blocker. |

These are recorded as open items in SRS Section 12.5 and in the RTM. They must not be resolved by assumption during implementation planning.

---

## 7. Terminology Decisions

The following canonical terminology was established during the SKED process and is defined in the approved Domain Glossary (SRS Section 4).

| Canonical term | Decision | Source |
|---|---|---|
| **MediaItem** | The single canonical term for an individual stored media object. Not "item," "entry," "record," or "content object." | HD-011 |
| **Topic** | The canonical term for a user-defined named category. Not "tag," "label," "collection," or "playlist." | HD-015 |
| **Notes** | The single optional free-text field per MediaItem. Not "note" (singular item) or "comments." | HD-011, HD-019 |
| **Rating** | The optional 1–10 evaluation field. Absence is described as "unrated," not as "null" or "zero." | HD-011, HD-052 |
| **Normalisation** | The process of trimming leading and trailing whitespace from a name before saving or comparison. | HD-049, HD-051 |
| **Auto-save** | The persistence behavior. Not "autosave," "auto save," or "background save." | HD-042 |
| **Save failure** | The error condition when auto-save does not succeed. | HD-063 |
| **Session** | The period from application launch to close. Relevant to save-failure retention scope. | HD-064 |
| **AND logic** | The multi-filter combination rule. Not "strict," "intersection," or "conjunction." | HD-030 |
| **Substring match** | The search matching strategy. Not "contains," "fuzzy," or "partial." | HD-026 |
| **Personal library** | The informal collective term for the user's complete data set. | spec/idea.md, HD-002 |

---

## 8. Requirements Evolution Summary

The specification was produced in the following ordered stages:

1. **Initial concept** (`spec/idea.md`) — an informal description of a personal media tracking system with user-defined topics and personal notes. No fields, rules, or constraints were specified.

2. **SKED elicitation (Iterations 1–7)** — a structured dialogue produced 69 confirmed human decisions (HD-000 through HD-068), resolving all requirement-level ambiguities. The process identified more than 30 distinct areas of uncertainty, each of which was raised as a question, answered by the human, and recorded as a decision.

3. **Domain Glossary** — 43 canonical terms defined from the confirmed decision record. No synonyms or undecided terms introduced.

4. **System Scope** — formal in-scope and out-of-scope boundary derived entirely from human decisions. Checked for consistency against all HD identifiers.

5. **Functional Requirements (REQ-F-001–066)** — 66 atomic, independently testable requirements derived from the decision record, organised into 10 subsections. Business rules (BR-001–010) and validation rules (VR-001–011) produced as sub-requirements.

6. **Non-Functional Requirements (REQ-NF-001–011)** — initial 36-item draft reduced to 11 after a strict review removed functional duplicates, scope restatements, and meta-notes. Six items were left pending human confirmation; four were resolved (Q-NFR-01 through Q-NFR-04); two capacity/reliability metrics were confirmed as not required.

7. **Interface Requirements (IR-001–043)** — 43 platform-independent interface requirements. One item (IR-024) was initially pending resolution of Q-IR-01 (search results presentation); resolved by selecting MP-IR-A (unified list with each result identified by type).

8. **Constraints (CON-001–013)** — 13 fixed solution-space constraints derived from human decisions. Distinguished from functional requirements and NFRs. No implementation prescriptions introduced.

9. **Acceptance Criteria (AC-001–069)** — 69 independently verifiable conditions derived from approved requirements. Two qualitative criteria (AC-052, AC-053) noted as requiring evaluator judgment.

10. **BDD Scenarios (BDD-001–070)** — initial 65-scenario baseline produced, then subjected to an independent consistency review that identified 14 issues. All 14 were corrected. Six new scenarios added (BDD-066–070); BDD-017 split into BDD-017a and BDD-017b. Final count: 70 scenarios.

11. **SRS** (`spec/srs.md`) — formal consolidation of all approved artifacts into a single 1,883-line IEEE 830-inspired document. No new requirements or behavior introduced during construction.

12. **Requirements Traceability Matrix** (`spec/traceability.md`) — full forward and reverse traceability across all 133 requirements, 69 ACs, and 70 BDD scenarios. Two traceability omissions from SRS Section 11 identified and corrected.

---

## 9. Review and Correction History

| Stage | Event | Outcome |
|---|---|---|
| NFR strict review | Initial 36-item NFR draft reviewed against approved baselines | 14 items removed as duplicates, scope restatements, or meta-notes; 4 human decision questions raised (Q-NFR-01–04); all 4 resolved; final NFR baseline: 11 items |
| Interface requirements | Q-IR-01 raised regarding unified vs separate search results | Resolved: MP-IR-A selected (unified list, each result identified by type); IR-024 finalised |
| Independent BDD consistency review | 65-scenario BDD baseline reviewed against all approved artifacts | 14 issues identified (6 MISSING COVERAGE, 5 AMBIGUOUS EXPECTED RESULT, 1 UNSUPPORTED ASSUMPTION, 1 TRACEABILITY ERROR, 1 structural issue) |
| BDD corrections | All 14 issues corrected per review | BDD-017 split into BDD-017a/b; 6 new scenarios added (BDD-066–070); 8 scenarios revised in-place; 1 traceability correction; final count: 70 scenarios |
| BDD status | Second independent consistency review confirmed all 14 issues resolved | BDD baseline marked READY FOR HUMAN APPROVAL |
| SRS construction | All approved artifacts consolidated into spec/srs.md | No new requirements introduced; 1,883 lines; all identifiers preserved |
| RTM audit | spec/traceability.md produced; all 133 requirements, 69 ACs, 70 BDD scenarios checked | Two traceability omissions found in SRS Section 11 and corrected in the RTM: VR-002 → AC-043 → BDD-006; VR-004 → AC-047 → BDD-022 |

---

## 10. Open Decisions

The following decisions were explicitly identified as unresolved during the SKED process and remain open. They must not be resolved by assumption or default during any subsequent phase.

| Decision | HD reference | What is needed to resolve it |
|---|---|---|
| Target operating system and deployment platform | HD-009, HD-047 | An explicit human decision naming the target platform before implementation planning begins |
| Technology stack (programming language, framework, database engine, file format, UI toolkit) | HD-009, HD-047 | An explicit human decision, which may be informed by the platform decision above |

These items are also recorded in SRS Section 12.5.

---

## 11. Traceability Reference

The complete forward and reverse traceability mapping is maintained in `spec/traceability.md`. The high-level chain is:

```
Human Decisions (HD-000 to HD-068)
    → Functional Requirements (REQ-F-001 to REQ-F-066)
    → Business Rules (BR-001 to BR-010)
    → Validation Rules (VR-001 to VR-011)
    → Non-Functional Requirements (REQ-NF-001 to REQ-NF-011)
    → Interface Requirements (IR-001 to IR-043)
    → Constraints (CON-001 to CON-013)
    → Acceptance Criteria (AC-001 to AC-069)
    → BDD Scenarios (BDD-001 to BDD-070)
    → SRS: spec/srs.md
    → RTM: spec/traceability.md
```

This document does not reproduce the full matrix. For full traceability, consult `spec/traceability.md`.

---

## 12. Log Integrity Statement

This document is a retrospective record of the requirements-engineering process. It does not create, modify, extend, or supersede any requirement, acceptance criterion, BDD scenario, constraint, or decision recorded in `spec/srs.md` or `spec/traceability.md`. All normative content resides exclusively in those two documents. Any future change to a requirement must be made through a formal revision of `spec/srs.md` and must be reflected in `spec/traceability.md`. This log should be updated to reflect such changes but is not itself the authoritative source of any requirement.

---

*End of SKED Dialogue Log — Version 1.0*
