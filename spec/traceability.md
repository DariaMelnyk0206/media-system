# Requirements Traceability Matrix

**Project:** Personal Media Library System
**Document ID:** RTM-001
**Version:** 1.0
**Date:** 2026-10-04
**Status:** Implementation Verified
**Source SRS:** spec/srs.md v1.0

---

## Notes on This Document

- This matrix covers the approved baseline requirements REQ-F-001–066, REQ-NF-001–011, IR-001–043, CON-001–013, plus Addendum 001 requirements REQ-F-070–074.
- Baseline links are retained as approved. Addendum 001 links and final verification statuses are recorded in Parts 8 and 9.
- A relationship is recorded only where it is supported by the approved specification. No relationship is inferred from proximity alone.
- Intentional gaps (requirements with no BDD scenario by design) are marked with a note rather than left blank.
- Two known gaps from the SRS Section 11 traceability table (AC-043, AC-047, BDD-006, BDD-022) are correctly mapped here and reported in the audit section.

---

## Table Legend

| Symbol | Meaning |
|---|---|
| `—` | Not applicable or not yet populated |
| `[intentional]` | No BDD scenario exists by deliberate specification decision |
| `[future]` | To be populated during implementation |

---

## Part 1 — Functional Requirements

### REQ-F-001 through REQ-F-066

| Req ID | Requirement (abbreviated) | Acceptance Criteria | BDD Scenarios | Tickets | Tests | Code | Documentation |
|---|---|---|---|---|---|---|---|
| REQ-F-001 | Allow user to create a new MediaItem | AC-001 | BDD-001, BDD-002, BDD-066 | — | — | — | — |
| REQ-F-002 | Name required at creation | AC-001, AC-042 | BDD-001, BDD-004, BDD-005 | — | — | — | — |
| REQ-F-003 | Type required at creation | AC-001 | BDD-001, BDD-002, BDD-066 | — | — | — | — |
| REQ-F-004 | Default status is *planned* at creation | AC-002, AC-060 | BDD-002, BDD-063, BDD-066 | — | — | — | — |
| REQ-F-005 | Notes may be left empty at creation | AC-003 | BDD-001, BDD-003 | — | — | — | — |
| REQ-F-006 | Rating may be left unset at creation | AC-003 | BDD-001, BDD-003 | — | — | — | — |
| REQ-F-007 | Topics may be assigned at creation | AC-004 | BDD-002 | — | — | — | — |
| REQ-F-008 | Auto-save on successful creation | AC-005 | BDD-003, BDD-057 | — | — | — | — |
| REQ-F-009 | View a MediaItem and all its fields | AC-006 | BDD-009, BDD-010 | — | — | — | — |
| REQ-F-010 | Edit any field of a MediaItem | AC-007 | BDD-011, BDD-012 | — | — | — | — |
| REQ-F-011 | Auto-save on successful edit | AC-007 | BDD-011, BDD-012 | — | — | — | — |
| REQ-F-012 | Allow user to delete a MediaItem | AC-008 | BDD-013 | — | — | — | — |
| REQ-F-013 | Require confirmation before deletion | AC-008, AC-009 | BDD-013, BDD-014 | — | — | — | — |
| REQ-F-014 | Permanently remove on confirmed delete | AC-008 | BDD-013 | — | — | — | — |
| REQ-F-015 | Remove all Topic associations on item delete | AC-010 | BDD-015 | — | — | — | — |
| REQ-F-016 | Topics unaffected by MediaItem delete | AC-010 | BDD-015 | — | — | — | — |
| REQ-F-017 | Deleted MediaItem is not restorable | AC-011 | BDD-016 | — | — | — | — |
| REQ-F-018 | Allow setting status to any of five values | AC-012 | BDD-017a, BDD-017b | — | — | — | — |
| REQ-F-019 | Free status change, no workflow | AC-012 | BDD-017a, BDD-017b | — | — | — | — |
| REQ-F-020 | Allow user to create a new Topic | AC-013 | BDD-018 | — | — | — | — |
| REQ-F-021 | Auto-save on successful Topic creation | AC-013 | BDD-018 | — | — | — | — |
| REQ-F-022 | View a Topic and its associated MediaItems | AC-014 | BDD-023, BDD-024 | — | — | — | — |
| REQ-F-023 | Allow user to rename a Topic | AC-015 | BDD-025 | — | — | — | — |
| REQ-F-024 | Rename preserves all MediaItem associations | AC-015 | BDD-025 | — | — | — | — |
| REQ-F-025 | Auto-save on successful Topic rename | AC-015 | BDD-025 | — | — | — | — |
| REQ-F-026 | Allow user to delete a Topic | AC-016 | BDD-027 | — | — | — | — |
| REQ-F-027 | Require confirmation before Topic deletion | AC-016, AC-017 | BDD-027, BDD-028 | — | — | — | — |
| REQ-F-028 | Remove Topic and its associations on confirmed delete | AC-016 | BDD-027, BDD-029 | — | — | — | — |
| REQ-F-029 | MediaItems unaffected by Topic delete | AC-016 | BDD-029 | — | — | — | — |
| REQ-F-030 | Add Topic association from MediaItem side | AC-018 | BDD-030, BDD-070 | — | — | — | — |
| REQ-F-031 | Remove Topic association from MediaItem side | AC-018 | BDD-031 | — | — | — | — |
| REQ-F-032 | Add MediaItem association from Topic side | AC-019 | BDD-032 | — | — | — | — |
| REQ-F-033 | Remove MediaItem association from Topic side | AC-019 | BDD-033 | — | — | — | — |
| REQ-F-034 | Auto-save on successful association change | AC-020 | BDD-030, BDD-032, BDD-034 | — | — | — | — |
| REQ-F-035 | Navigate from Topic to associated MediaItem | AC-021 | BDD-035, BDD-070 | — | — | — | — |
| REQ-F-036 | Display all Topics a MediaItem belongs to | AC-022 | BDD-036, BDD-070 | — | — | — | — |
| REQ-F-037 | Navigate from MediaItem to associated Topic | AC-022 | BDD-036 | — | — | — | — |
| REQ-F-038 | Allow user to enter a search query | AC-023 | BDD-037 | — | — | — | — |
| REQ-F-039 | Return MediaItems matching query by substring | AC-023, AC-026 | BDD-037, BDD-039, BDD-067 | — | — | — | — |
| REQ-F-040 | Return Topics matching query by substring | AC-024, AC-026 | BDD-038, BDD-039, BDD-067 | — | — | — | — |
| REQ-F-041 | Allow opening a Topic search result | AC-025 | BDD-040 | — | — | — | — |
| REQ-F-042 | Empty search query = search inactive | AC-027 | BDD-041 | — | — | — | — |
| REQ-F-043 | Notes field not searched | AC-028 | BDD-042 | — | — | — | — |
| REQ-F-044 | Filter by media type | AC-029 | BDD-043 | — | — | — | — |
| REQ-F-045 | Filter by status | AC-030 | BDD-044 | — | — | — | — |
| REQ-F-046 | Filter by rating range | AC-031, AC-032, AC-033 | BDD-045, BDD-046, BDD-047 | — | — | — | — |
| REQ-F-047 | Allow lower bound only, upper only, or both | AC-031, AC-032, AC-033 | BDD-045, BDD-046, BDD-047 | — | — | — | — |
| REQ-F-048 | Exclude unrated items when rating filter active | AC-034 | BDD-045, BDD-046, BDD-047 | — | — | — | — |
| REQ-F-049 | Filter by Topic | AC-035 | BDD-049, BDD-050 | — | — | — | — |
| REQ-F-050 | Multiple simultaneous filters use AND logic | AC-036 | BDD-051, BDD-068 | — | — | — | — |
| REQ-F-051 | Sort by name ascending | AC-037 | BDD-052 | — | — | — | — |
| REQ-F-052 | Sort by name descending | AC-038 | BDD-053 | — | — | — | — |
| REQ-F-053 | Sort by rating ascending | AC-039 | BDD-054 | — | — | — | — |
| REQ-F-054 | Sort by rating descending | AC-040 | BDD-055 | — | — | — | — |
| REQ-F-055 | Unrated items appear last in rating sort | AC-039, AC-040 | BDD-054, BDD-055 | — | — | — | — |
| REQ-F-056 | Tie order is unspecified | — | — [intentional: unspecified by design] | — | — | — | — |
| REQ-F-057 | Search, filter, and sort combinable | AC-041 | BDD-056, BDD-069 | — | — | — | — |
| REQ-F-058 | Combined: filter first, then sort | AC-041 | BDD-056, BDD-069 | — | — | — | — |
| REQ-F-059 | Auto-save every successful data change | AC-049, AC-061 | BDD-012, BDD-064 | — | — | — | — |
| REQ-F-060 | Notify user when auto-save fails | AC-050, AC-062 | BDD-058 | — | — | — | — |
| REQ-F-061 | Retain unsaved change in current session | AC-051, AC-062 | BDD-059 | — | — | — | — |
| REQ-F-062 | Reject empty or whitespace-only MediaItem name | AC-042 | BDD-004, BDD-005 | — | — | — | — |
| REQ-F-063 | Reject invalid or non-unique Topic name | AC-045, AC-046 | BDD-019, BDD-020, BDD-021, BDD-026 | — | — | — | — |
| REQ-F-064 | Reject MediaItem rating outside 1–10 | AC-044 | BDD-007, BDD-008 | — | — | — | — |
| REQ-F-065 | Reject rating filter where lower > upper | AC-048 | BDD-048 | — | — | — | — |
| REQ-F-066 | Notify user of save failure (mechanism unspecified) | AC-050 | BDD-058 | — | — | — | — |

### Validation Rules (under Section 5 of SRS)

Validation rules VR-001–011 are sub-requirements of the Functional Requirements. They are included here for completeness.

| Rule ID | Rule (abbreviated) | Parent REQ-F | Acceptance Criteria | BDD Scenarios |
|---|---|---|---|---|
| VR-001 | MediaItem name must not be empty after trimming | REQ-F-062 | AC-042 | BDD-004, BDD-005 |
| VR-002 | Leading/trailing whitespace trimmed from MediaItem name | REQ-F-062 | AC-043 | BDD-006 |
| VR-003 | Topic name must not be empty after trimming | REQ-F-063 | AC-045 | BDD-019 |
| VR-004 | Leading/trailing whitespace trimmed from Topic name | REQ-F-063 | AC-047 | BDD-022 |
| VR-005 | Topic name must be case-insensitively unique | REQ-F-063 | AC-046 | BDD-020, BDD-021, BDD-026 |
| VR-006 | Uniqueness check applies at creation and rename | REQ-F-063 | AC-046 | BDD-020, BDD-021, BDD-026 |
| VR-007 | Rating must be integer 1–10 when provided | REQ-F-064 | AC-044 | BDD-007, BDD-008 |
| VR-008 | Type must be one of seven predefined values | REQ-F-003 | AC-064 | BDD-001, BDD-002 |
| VR-009 | Status must be one of five predefined values | REQ-F-018 | AC-065 | BDD-017a, BDD-017b |
| VR-010 | Rating filter: lower bound must not exceed upper bound | REQ-F-065 | AC-048 | BDD-048 |
| VR-011 | Each rating bound must be integer 1–10 | REQ-F-046, REQ-F-047 | AC-031, AC-032, AC-033 | BDD-045, BDD-046, BDD-047 |

---

## Part 2 — Non-Functional Requirements

| Req ID | Requirement (abbreviated) | Acceptance Criteria | BDD Scenarios | Tickets | Tests | Code | Documentation |
|---|---|---|---|---|---|---|---|
| REQ-NF-001 | Common ops without perceptible delay | AC-052 | — [intentional: qualitative; evaluator judgment] | — | — | — | — |
| REQ-NF-002 | Operable without external documentation | AC-053 | — [intentional: qualitative; evaluator judgment] | — | — | — | — |
| REQ-NF-003 | Informative validation violation messages | AC-042, AC-043, AC-044, AC-045, AC-046, AC-047, AC-048 | BDD-004, BDD-005, BDD-006, BDD-007, BDD-008, BDD-019, BDD-020, BDD-021, BDD-022, BDD-026, BDD-048 | — | — | — | — |
| REQ-NF-004 | Confirmation prompt before permanent deletion | AC-008, AC-009, AC-016, AC-017 | BDD-013, BDD-014, BDD-027, BDD-028 | — | — | — | — |
| REQ-NF-005 | Successfully saved data available on next launch | AC-005, AC-013, AC-015, AC-020, AC-049, AC-063 | BDD-003, BDD-018, BDD-025, BDD-034, BDD-057 | — | — | — | — |
| REQ-NF-006 | Save failure must not corrupt prior data | AC-050 | BDD-058 | — | — | — | — |
| REQ-NF-007 | No association may reference a non-existent entity | AC-054 | BDD-015, BDD-029 | — | — | — | — |
| REQ-NF-008 | No network request required for any operation | AC-055, AC-068 | BDD-060 | — | — | — | — |
| REQ-NF-009 | User data not transmitted outside local machine | AC-056 | BDD-060 | — | — | — | — |
| REQ-NF-010 | All user-facing text in English | AC-057 | BDD-065 | — | — | — | — |
| REQ-NF-011 | Platform and technology stack not prescribed | — | — [intentional: specification meta-constraint; not testable at runtime] | — | — | — | — |

---

## Part 3 — Interface Requirements

| Req ID | Requirement (abbreviated) | Acceptance Criteria | BDD Scenarios | Tickets | Tests | Code | Documentation |
|---|---|---|---|---|---|---|---|
| IR-001 | All user-facing text in English | AC-057 | BDD-065 | — | — | — | — |
| IR-002 | No authentication UI elements | AC-058 | BDD-061 | — | — | — | — |
| IR-003 | No connection-related UI elements | AC-059 | BDD-062 | — | — | — | — |
| IR-004 | Entry point to create a MediaItem | AC-001 | BDD-001 | — | — | — | — |
| IR-005 | All MediaItem fields accessible at creation | AC-001, AC-002, AC-003, AC-004 | BDD-001, BDD-002 | — | — | — | — |
| IR-006 | Status pre-selected as *planned* on creation form | AC-060 | BDD-063 | — | — | — | — |
| IR-007 | View MediaItem showing all fields without extra navigation | AC-006 | BDD-009, BDD-010 | — | — | — | — |
| IR-008 | All MediaItem fields accessible for editing | AC-007 | BDD-011, BDD-012 | — | — | — | — |
| IR-009 | Entry point to delete a MediaItem | AC-008 | BDD-013 | — | — | — | — |
| IR-010 | Confirmation prompt before MediaItem deletion | AC-008, AC-009 | BDD-013, BDD-014 | — | — | — | — |
| IR-011 | Entry point to create a Topic | AC-013 | BDD-018 | — | — | — | — |
| IR-012 | View Topic displaying name and associated MediaItems | AC-014 | BDD-023, BDD-024 | — | — | — | — |
| IR-013 | Entry point to rename a Topic | AC-015 | BDD-025 | — | — | — | — |
| IR-014 | Entry point to delete a Topic | AC-016 | BDD-027 | — | — | — | — |
| IR-015 | Confirmation prompt before Topic deletion | AC-016, AC-017 | BDD-027, BDD-028 | — | — | — | — |
| IR-016 | Add/remove Topic from MediaItem side | AC-018 | BDD-030, BDD-031 | — | — | — | — |
| IR-017 | Add/remove MediaItem from Topic side | AC-019 | BDD-032, BDD-033 | — | — | — | — |
| IR-018 | Navigate from Topic to associated MediaItem | AC-021 | BDD-035 | — | — | — | — |
| IR-019 | Display all Topics for a MediaItem; navigate to any | AC-022 | BDD-036 | — | — | — | — |
| IR-020 | Search query entry | AC-023 | BDD-037 | — | — | — | — |
| IR-021 | Display matching MediaItems as search results | AC-023 | BDD-037 | — | — | — | — |
| IR-022 | Display matching Topics as distinct search results | AC-024 | BDD-038 | — | — | — | — |
| IR-023 | Allow opening a Topic search result | AC-025 | BDD-040 | — | — | — | — |
| IR-024 | Unified search list; each result identified by type | AC-026 | BDD-039, BDD-067 | — | — | — | — |
| IR-025 | Empty search does not restrict results | AC-027 | BDD-041 | — | — | — | — |
| IR-026 | Type filter | AC-029 | BDD-043 | — | — | — | — |
| IR-027 | Status filter | AC-030 | BDD-044 | — | — | — | — |
| IR-028 | Rating filter bound(s) entry | AC-031, AC-032, AC-033 | BDD-045, BDD-046, BDD-047 | — | — | — | — |
| IR-029 | Topic filter | AC-035 | BDD-049, BDD-050 | — | — | — | — |
| IR-030 | AND logic reflected in multi-filter results | AC-036 | BDD-051, BDD-068 | — | — | — | — |
| IR-031 | Sort by name (ascending/descending) | AC-037, AC-038 | BDD-052, BDD-053 | — | — | — | — |
| IR-032 | Sort by rating (ascending/descending) | AC-039, AC-040 | BDD-054, BDD-055 | — | — | — | — |
| IR-033 | Unrated items visibly last in rating sort | AC-039, AC-040 | BDD-054, BDD-055 | — | — | — | — |
| IR-034 | Combined search + filter + sort active simultaneously | AC-041 | BDD-056, BDD-069 | — | — | — | — |
| IR-035 | Informative message: MediaItem name violation | AC-042 | BDD-004, BDD-005 | — | — | — | — |
| IR-036 | Informative message: rating value violation | AC-044 | BDD-007, BDD-008 | — | — | — | — |
| IR-037 | Informative message: Topic name empty | AC-045 | BDD-019 | — | — | — | — |
| IR-038 | Informative message: Topic name not unique | AC-046 | BDD-020, BDD-021, BDD-026 | — | — | — | — |
| IR-039 | Informative message: rating range invalid | AC-048 | BDD-048 | — | — | — | — |
| IR-040 | No explicit Save action required or presented | AC-061 | BDD-012, BDD-064 | — | — | — | — |
| IR-041 | Notification presented on save failure | AC-050, AC-062 | BDD-058 | — | — | — | — |
| IR-042 | Unsaved change remains visible after save failure | AC-051, AC-062 | BDD-059 | — | — | — | — |
| IR-043 | Library fully present on application launch | AC-063 | BDD-057 | — | — | — | — |

---

## Part 4 — Constraints

| Req ID | Constraint (abbreviated) | Acceptance Criteria | BDD Scenarios | Tickets | Tests | Code | Documentation |
|---|---|---|---|---|---|---|---|
| CON-001 | Fixed media type set (7 values) | AC-064 | BDD-001, BDD-002 | — | — | — | — |
| CON-002 | Fixed status value set (5 values) | AC-065 | BDD-017a, BDD-017b | — | — | — | — |
| CON-003 | Rating domain: integer 1–10 or absent | AC-044 | BDD-007, BDD-008 | — | — | — | — |
| CON-004 | Uniform MediaItem field structure; no type-specific fields | AC-066 | — [intentional: model structure; verified by inspection] | — | — | — | — |
| CON-005 | No date-added field | AC-067 | — [intentional: absence; verified by inspection] | — | — | — | — |
| CON-006 | Single notes field per MediaItem | — | — [intentional: enforced by model; no dedicated AC] | — | — | — | — |
| CON-007 | Topic name uniqueness: case-insensitive, post-normalisation | AC-046, AC-047 | BDD-020, BDD-021, BDD-022, BDD-026 | — | — | — | — |
| CON-008 | Single local user; no multi-user architecture | AC-058 | BDD-061 | — | — | — | — |
| CON-009 | No network component | AC-068 | BDD-060 | — | — | — | — |
| CON-010 | All data stored locally; no external transmission | AC-056 | BDD-060 | — | — | — | — |
| CON-011 | English user-facing text only | AC-057 | BDD-065 | — | — | — | — |
| CON-012 | Platform and technology stack not prescribed | — | — [intentional: specification meta-constraint] | — | — | — | — |
| CON-013 | Excluded features scope ceiling | AC-069 | — [intentional: absence; verified by scope audit] | — | — | — | — |

---

## Part 5 — Reverse Traceability: Acceptance Criteria → Requirements

| AC ID | Acceptance Criterion (abbreviated) | Source Requirements |
|---|---|---|
| AC-001 | MediaItem created with name and type | REQ-F-001, REQ-F-002, REQ-F-003, IR-004, IR-005 |
| AC-002 | Default status is *planned* | REQ-F-004, IR-006 |
| AC-003 | Creation succeeds with empty notes and unset rating | REQ-F-005, REQ-F-006 |
| AC-004 | Topics assigned at creation are associated | REQ-F-007 |
| AC-005 | Created item present after relaunch | REQ-F-008, REQ-NF-005 |
| AC-006 | All fields visible when viewing MediaItem | REQ-F-009, IR-007 |
| AC-007 | Edited value reflected without explicit save | REQ-F-010, REQ-F-011, IR-008 |
| AC-008 | Item permanently removed after confirmed delete | REQ-F-012, REQ-F-013, REQ-F-014, IR-009, IR-010, REQ-NF-004 |
| AC-009 | Item unchanged when delete is cancelled | REQ-F-013, IR-010, REQ-NF-004 |
| AC-010 | Associations removed; Topics intact after item delete | REQ-F-015, REQ-F-016 |
| AC-011 | No restore available for deleted item | REQ-F-017 |
| AC-012 | Status changeable to any value from any other | REQ-F-018, REQ-F-019 |
| AC-013 | Topic created and present after relaunch | REQ-F-020, REQ-F-021, IR-011, REQ-NF-005 |
| AC-014 | Topic shows name and associated items | REQ-F-022, IR-012 |
| AC-015 | Rename updates name, preserves associations, persists | REQ-F-023, REQ-F-024, REQ-F-025, IR-013, REQ-NF-005 |
| AC-016 | Topic deleted; associations removed; items intact | REQ-F-026, REQ-F-027, REQ-F-028, REQ-F-029, IR-014, IR-015, REQ-NF-004 |
| AC-017 | Topic unchanged when delete is cancelled | REQ-F-027, IR-015, REQ-NF-004 |
| AC-018 | Association add/remove from MediaItem side | REQ-F-030, REQ-F-031, IR-016 |
| AC-019 | Association add/remove from Topic side | REQ-F-032, REQ-F-033, IR-017 |
| AC-020 | Association change persists after relaunch | REQ-F-034, REQ-NF-005 |
| AC-021 | Navigate from Topic to MediaItem | REQ-F-035, IR-018 |
| AC-022 | Navigate from MediaItem to Topic | REQ-F-036, REQ-F-037, IR-019 |
| AC-023 | MediaItem name matched by substring | REQ-F-038, REQ-F-039, IR-020, IR-021 |
| AC-024 | Topic name matched; result identified as Topic | REQ-F-040, IR-022 |
| AC-025 | Topic search result openable | REQ-F-041, IR-023 |
| AC-026 | Unified results list; each item identified by type | REQ-F-039, REQ-F-040, IR-024 |
| AC-027 | Empty query returns all non-search-restricted results | REQ-F-042, IR-025 |
| AC-028 | Notes content not returned in search | REQ-F-043 |
| AC-029 | Type filter restricts by type | REQ-F-044, IR-026 |
| AC-030 | Status filter restricts by status | REQ-F-045, IR-027 |
| AC-031 | Rating filter lower-bound only | REQ-F-046, REQ-F-047, IR-028 |
| AC-032 | Rating filter upper-bound only | REQ-F-046, REQ-F-047, IR-028 |
| AC-033 | Rating filter both bounds | REQ-F-046, REQ-F-047, IR-028 |
| AC-034 | Unrated items excluded by any rating filter | REQ-F-048 |
| AC-035 | Topic filter restricts to associated items | REQ-F-049, IR-029 |
| AC-036 | AND logic; empty result when no item satisfies all | REQ-F-050, IR-030 |
| AC-037 | Sort name ascending | REQ-F-051, IR-031 |
| AC-038 | Sort name descending | REQ-F-052, IR-031 |
| AC-039 | Sort rating ascending; unrated last | REQ-F-053, REQ-F-055, IR-032, IR-033 |
| AC-040 | Sort rating descending; unrated last | REQ-F-054, REQ-F-055, IR-032, IR-033 |
| AC-041 | Combined search + filter + sort | REQ-F-057, REQ-F-058, IR-034 |
| AC-042 | Reject empty/whitespace-only MediaItem name | REQ-F-062, VR-001, IR-035, REQ-NF-003 |
| AC-043 | MediaItem name trimmed before saving | VR-002 |
| AC-044 | Reject rating outside 1–10 | REQ-F-064, VR-007, IR-036, REQ-NF-003, CON-003 |
| AC-045 | Reject empty/whitespace-only Topic name | REQ-F-063, VR-003, IR-037, REQ-NF-003 |
| AC-046 | Reject non-unique Topic name | REQ-F-063, VR-005, VR-006, IR-038, REQ-NF-003, CON-007 |
| AC-047 | Topic name trimmed before saving | VR-004, CON-007 |
| AC-048 | Reject inverted rating filter range | REQ-F-065, VR-010, IR-039, REQ-NF-003 |
| AC-049 | All change types persist after relaunch | REQ-F-059, REQ-NF-005 |
| AC-050 | Save failure notified; prior data intact | REQ-F-060, REQ-F-066, IR-041, REQ-NF-006 |
| AC-051 | Unsaved change accessible in current session | REQ-F-061, IR-042 |
| AC-052 | Common ops without perceptible delay (qualitative) | REQ-NF-001 |
| AC-053 | Operable without docs (qualitative) | REQ-NF-002 |
| AC-054 | No orphaned associations after deletion | REQ-NF-007 |
| AC-055 | All ops succeed offline | REQ-NF-008 |
| AC-056 | No outbound network traffic | REQ-NF-009 |
| AC-057 | All user-facing text is English | REQ-NF-010, IR-001, CON-011 |
| AC-058 | No auth UI present | IR-002, CON-008 |
| AC-059 | No connection UI present | IR-003 |
| AC-060 | Status pre-selected as *planned* on creation form | IR-006 |
| AC-061 | No explicit Save action required | IR-040 |
| AC-062 | Failure notification and unsaved change visible | IR-041, IR-042 |
| AC-063 | Library fully present on launch | IR-043, REQ-NF-005 |
| AC-064 | Type field contains only seven predefined values | CON-001, VR-008 |
| AC-065 | Status field contains only five predefined values | CON-002, VR-009 |
| AC-066 | No fields beyond the approved set | CON-004 |
| AC-067 | No date-added field present | CON-005 |
| AC-068 | No outbound network calls | CON-009, REQ-NF-008 |
| AC-069 | No excluded feature present | CON-013 |

---

## Part 6 — Reverse Traceability: BDD Scenarios → Requirements and Acceptance Criteria

| BDD ID | Scenario (abbreviated) | Source Requirements | Acceptance Criteria |
|---|---|---|---|
| BDD-001 | Create MediaItem, required fields only | REQ-F-001–007 | AC-001, AC-002, AC-003 |
| BDD-002 | Create MediaItem, all optional fields | REQ-F-001–007 | AC-001, AC-003, AC-004 |
| BDD-003 | Created item persists after relaunch | REQ-F-008, REQ-NF-005 | AC-005 |
| BDD-004 | Reject empty MediaItem name | REQ-F-062, VR-001 | AC-042 |
| BDD-005 | Reject whitespace-only MediaItem name | REQ-F-062, VR-001 | AC-042 |
| BDD-006 | MediaItem name trimmed | VR-002 | AC-043 |
| BDD-007 | Reject rating above 10 | REQ-F-064, VR-007 | AC-044 |
| BDD-008 | Reject rating of zero | REQ-F-064, VR-007 | AC-044 |
| BDD-009 | View fully populated MediaItem | REQ-F-009, IR-007 | AC-006 |
| BDD-010 | View MediaItem with optional fields unset | REQ-F-009 | AC-006 |
| BDD-011 | Edit MediaItem and confirm persistence | REQ-F-010–011, REQ-NF-005 | AC-007, AC-049 |
| BDD-012 | Edit requires no explicit save | REQ-F-011, REQ-F-059 | AC-007, AC-061 |
| BDD-013 | Delete MediaItem after confirmation | REQ-F-012–014 | AC-008 |
| BDD-014 | Cancel MediaItem deletion | REQ-F-013 | AC-009 |
| BDD-015 | Delete item removes associations; Topics intact | REQ-F-014–016 | AC-010 |
| BDD-016 | Deleted item cannot be restored | REQ-F-017 | AC-011 |
| BDD-017a | Change status planned → abandoned | REQ-F-018–019 | AC-012 |
| BDD-017b | Change status abandoned → completed | REQ-F-018–019 | AC-012 |
| BDD-018 | Create Topic and confirm persistence | REQ-F-020–021 | AC-013 |
| BDD-019 | Reject empty Topic name | REQ-F-063, VR-003 | AC-045 |
| BDD-020 | Reject duplicate Topic name (case-insensitive) | REQ-F-063, VR-005 | AC-046 |
| BDD-021 | Reject duplicate Topic name with whitespace | REQ-F-063, VR-005–006 | AC-046 |
| BDD-022 | Topic name trimmed | VR-004 | AC-047 |
| BDD-023 | View Topic with associated items | REQ-F-022 | AC-014 |
| BDD-024 | View empty Topic | REQ-F-022 | AC-014 |
| BDD-025 | Rename Topic; associations preserved; persists | REQ-F-023–025, REQ-NF-005 | AC-015 |
| BDD-026 | Reject Topic rename to existing name | REQ-F-063, VR-006 | AC-046 |
| BDD-027 | Delete Topic after confirmation | REQ-F-026–028 | AC-016 |
| BDD-028 | Cancel Topic deletion | REQ-F-027 | AC-017 |
| BDD-029 | Delete Topic; MediaItems intact | REQ-F-028–029 | AC-016 |
| BDD-030 | Add association from MediaItem side | REQ-F-030, REQ-F-034 | AC-018, AC-020 |
| BDD-031 | Remove association from MediaItem side | REQ-F-031 | AC-018 |
| BDD-032 | Add association from Topic side | REQ-F-032, REQ-F-034 | AC-019, AC-020 |
| BDD-033 | Remove association from Topic side | REQ-F-033 | AC-019 |
| BDD-034 | Association persists after relaunch | REQ-F-034, REQ-NF-005 | AC-020, AC-049 |
| BDD-035 | Navigate Topic → MediaItem | REQ-F-035 | AC-021 |
| BDD-036 | Navigate MediaItem → Topic | REQ-F-036–037 | AC-022 |
| BDD-037 | Search returns MediaItems by substring | REQ-F-038–039 | AC-023 |
| BDD-038 | Search returns Topics as Topic results | REQ-F-040 | AC-024 |
| BDD-039 | Unified search list with identical names | REQ-F-039–040 | AC-026 |
| BDD-040 | Open Topic from search results | REQ-F-041 | AC-025 |
| BDD-041 | Empty search does not restrict MediaItem results | REQ-F-042 | AC-027 |
| BDD-042 | Notes content not searchable | REQ-F-043 | AC-028 |
| BDD-043 | Filter by type | REQ-F-044 | AC-029 |
| BDD-044 | Filter by status | REQ-F-045 | AC-030 |
| BDD-045 | Rating filter, lower bound only | REQ-F-046–048 | AC-031, AC-034 |
| BDD-046 | Rating filter, upper bound only | REQ-F-046–048 | AC-032, AC-034 |
| BDD-047 | Rating filter, both bounds | REQ-F-046–048 | AC-033, AC-034 |
| BDD-048 | Reject inverted rating range | REQ-F-065, VR-010 | AC-048 |
| BDD-049 | Topic filter returns only associated items | REQ-F-049 | AC-035 |
| BDD-050 | Topic filter on empty Topic returns empty results | REQ-F-049 | AC-035 |
| BDD-051 | Multiple filters with AND logic | REQ-F-050 | AC-036 |
| BDD-052 | Sort by name ascending | REQ-F-051 | AC-037 |
| BDD-053 | Sort by name descending | REQ-F-052 | AC-038 |
| BDD-054 | Sort by rating ascending; unrated last | REQ-F-053, REQ-F-055 | AC-039 |
| BDD-055 | Sort by rating descending; unrated last | REQ-F-054–055 | AC-040 |
| BDD-056 | Combined: search + type filter + rating sort | REQ-F-057–058 | AC-041 |
| BDD-057 | All data types persist across relaunch | REQ-F-008, REQ-NF-005 | AC-049, AC-063 |
| BDD-058 | Save failure notification; prior data intact | REQ-F-060, REQ-F-066, REQ-NF-006 | AC-050 |
| BDD-059 | Unsaved change visible in session after failure | REQ-F-061 | AC-051, AC-062 |
| BDD-060 | All ops succeed offline | REQ-NF-008 | AC-055 |
| BDD-061 | No authentication UI | IR-002 | AC-058 |
| BDD-062 | No connection UI | IR-003 | AC-059 |
| BDD-063 | Status defaults to *planned* on creation form | IR-006 | AC-060 |
| BDD-064 | No explicit Save action required | IR-040, REQ-F-059 | AC-061 |
| BDD-065 | All user-facing text is English | REQ-NF-010, IR-001 | AC-057 |
| BDD-066 | Explicit non-default status preserved at creation | REQ-F-001, REQ-F-003, REQ-F-004 | AC-001, AC-002 |
| BDD-067 | Unified search: heterogeneous substring match | REQ-F-039–040, IR-024 | AC-023, AC-024, AC-026 |
| BDD-068 | AND logic produces empty result | REQ-F-050 | AC-036 |
| BDD-069 | Combined: search + type filter + name sort | REQ-F-057–058 | AC-041 |
| BDD-070 | Many-to-many: one item, multiple Topics | REQ-F-030, REQ-F-035–036 | AC-018, AC-021, AC-022 |

---

## Part 7 — Traceability Audit

### A. Coverage Totals

| Category | Total | With AC | With BDD | Without AC | Without BDD |
|---|---|---|---|---|---|
| REQ-F | 66 | 65 | 65 | 1 (REQ-F-056) | 1 (REQ-F-056) |
| REQ-NF | 11 | 10 | 8 | 1 (REQ-NF-011) | 3 (REQ-NF-001, NF-002, NF-011) |
| IR | 43 | 43 | 43 | 0 | 0 |
| CON | 13 | 11 | 9 | 2 (CON-006, CON-012) | 4 (CON-004, CON-005, CON-006, CON-012) |
| **Total requirements** | **133** | **129** | **125** | **4** | **8** |
| AC | 69 | n/a | 67 | — | 2 (AC-052, AC-053) |
| BDD | 70 | 70 | n/a | 0 | — |

### B. Requirements With No AC (4 items)

| ID | Reason | Classification |
|---|---|---|
| REQ-F-056 | Tie order is explicitly unspecified by approved specification; no criterion is possible | **Intentional** |
| REQ-NF-011 | Specification meta-constraint; not testable at runtime | **Intentional** |
| CON-006 | Enforced by model structure; no dedicated AC; absence of multi-note mechanism is verification | **Intentional** |
| CON-012 | Same as REQ-NF-011 | **Intentional** |

### C. Requirements With No BDD Scenario (8 items)

| ID | Reason | Classification |
|---|---|---|
| REQ-F-056 | Unspecified by design | **Intentional** |
| REQ-NF-001 | Qualitative only; evaluator judgment | **Intentional** |
| REQ-NF-002 | Qualitative only; evaluator judgment | **Intentional** |
| REQ-NF-011 | Specification meta-constraint | **Intentional** |
| CON-004 | Verified by model inspection, not user behavior | **Intentional** |
| CON-005 | Verified by absence inspection | **Intentional** |
| CON-006 | Verified by model structure | **Intentional** |
| CON-012 | Specification meta-constraint | **Intentional** |

### D. AC Without BDD Scenario (2 items)

| ID | Reason | Classification |
|---|---|---|
| AC-052 | Qualitative performance; no quantitative threshold | **Intentional** |
| AC-053 | Qualitative usability; requires human evaluator | **Intentional** |

### E. Orphan ACs (ACs not traceable to any requirement)

**None.** All 69 ACs trace to at least one approved requirement.

### F. Orphan BDD Scenarios (BDDs not traceable to any requirement or AC)

**None.** All 70 BDD scenarios trace to at least one approved requirement and at least one AC.

### G. Inconsistencies Found

**One inconsistency corrected in this matrix relative to SRS Section 11:**

| Issue | Description | Action |
|---|---|---|
| AC-043 missing from SRS Section 11 traceability table | AC-043 (MediaItem name trimmed) traces to VR-002. VR-002 is defined in Section 5.12 but was not assigned a row in the SRS Section 11 matrix. BDD-006 also had no row. | Correctly mapped in this RTM: VR-002 → AC-043 → BDD-006. This does not constitute a new requirement; it is a traceability gap correction in the matrix only. The AC and BDD scenario are approved and present in spec/srs.md. |
| AC-047 missing from SRS Section 11 traceability table | AC-047 (Topic name trimmed) traces to VR-004. Same omission as above. BDD-022 also had no row. | Correctly mapped in this RTM: VR-004 → AC-047 → BDD-022. Same classification: traceability gap correction only. |

**No contradictions, duplicate relationships, or incorrect identifiers were found in the approved baseline.**

### H. Summary

| Check | Result |
|---|---|
| All REQ-F present | ✓ 66 of 66 |
| All REQ-NF present | ✓ 11 of 11 |
| All IR present | ✓ 43 of 43 |
| All CON present | ✓ 13 of 13 |
| All AC traced to at least one requirement | ✓ 69 of 69 |
| All BDD traced to at least one requirement and one AC | ✓ 70 of 70 |
| Requirements without AC | 4 — all intentional |
| Requirements without BDD | 8 — all intentional |
| AC without BDD | 2 — all intentional |
| Orphan ACs | 0 |
| Orphan BDD scenarios | 0 |
| Contradictions | 0 |
| Gaps requiring human decision | 0 |
| Traceability gaps in SRS Section 11 (corrected here) | 2 (AC-043/BDD-006, AC-047/BDD-022) |

---

*End of baseline Requirements Traceability Matrix — Version 1.0*

---

## Part 8 — Addendum 001: Collection Statistics

This section extends the initial SRS-001 v1.0 baseline. The addendum uses
AC-070..075 because AC-047..052 are already defined in the baseline. BDD-071..075
continue after the baseline's BDD-070.

### Functional Requirements → Acceptance Criteria → BDD → Tickets

| Req ID | Requirement (abbreviated) | Acceptance Criteria | BDD Scenarios | Tickets |
|---|---|---|---|---|
| REQ-F-070 | Return total MediaItem and Topic counts | AC-070, AC-074 | BDD-071 | TEST-016, FEAT-013 |
| REQ-F-071 | Return complete status and type distributions | AC-071, AC-074 | BDD-071, BDD-072 | TEST-016, FEAT-013 |
| REQ-F-072 | Return average rating and rated count | AC-072, AC-074 | BDD-071, BDD-072 | TEST-016, FEAT-013 |
| REQ-F-073 | Return ordered Topic association counts | AC-073 | BDD-073 | TEST-016, FEAT-013 |
| REQ-F-074 | Log request outcome without user-authored content | AC-075 | BDD-074, BDD-075 | TEST-016, FEAT-013 |

### Addendum Acceptance Criteria → Requirements

| AC ID | Acceptance Criterion (abbreviated) | Source Requirements |
|---|---|---|
| AC-070 | Collection totals match current records | REQ-F-070 |
| AC-071 | Complete status/type counts sum to MediaItem total | REQ-F-071 |
| AC-072 | Rated-only mean and count; null with no ratings | REQ-F-072 |
| AC-073 | Every Topic has a distinct associated-item count and deterministic order | REQ-F-073 |
| AC-074 | Empty collection returns zero/empty aggregates and null average | REQ-F-070..072 |
| AC-075 | Query is logged; failures use HTTP 500 ErrorResponse | REQ-F-074 |

### Addendum BDD Scenarios → Requirements and Acceptance Criteria

| BDD ID | Scenario (abbreviated) | Source Requirements | Acceptance Criteria |
|---|---|---|---|
| BDD-071 | Statistics for an empty collection | REQ-F-070..072 | AC-070, AC-071, AC-072, AC-074 |
| BDD-072 | Rating aggregates exclude unrated items | REQ-F-071..072 | AC-071, AC-072 |
| BDD-073 | Many-to-many Topic counts and ordering | REQ-F-073 | AC-073 |
| BDD-074 | Successful statistics request is logged | REQ-F-074 | AC-075 |
| BDD-075 | Processing failure returns 500 and is logged | REQ-F-074 | AC-075 |

### Scope Exception

Addendum 001 narrowly supersedes CON-013's exclusion of statistics and
qualifies AC-069 for the local, read-only `GET /api/stats` capability only.
AC-069 and CON-013 remain in force for all other exclusions. The addendum is
additive and does not change existing API contracts.

---

*End of Requirements Traceability Matrix — Version 1.0 with Addendum 001*

---

## Part 9 — Final Implementation Verification

Verification was recorded on 2026-11-15. Requirement identifiers follow the
approved SRS baseline and Addendum 001; REQ-F-067..069 are unallocated and are
not part of the current requirement set.

| Artifact category | Identifiers / scope | Status | Evidence |
|---|---|---|---|
| Functional requirements | REQ-F-001..066, REQ-F-070..074 | PASS | Unit and contract suite; addendum coverage in Part 8 |
| Acceptance criteria | AC-001..069, AC-070..075 | PASS | Mapped to requirements and verified behavior |
| BDD scenarios | BDD-001..070, BDD-071..075 | PASS | Mapped to requirements and acceptance criteria |
| Unit test modules | All 13 modules under `tests/unit/` | PASS | Full pytest run |
| OpenAPI contract module | `tests/contract/test_openapi_contract.py` | PASS | Full pytest run |
| OpenAPI operations | All 16 operations documented under `/api` | PASS | Runtime contract test and OpenAPI specification |
| Full test suite | `pytest tests/ --tb=short -q` | PASS — 297/297 | 2026-11-15 |
| Ruff | Implementation, contract tests, collection-statistics tests | PASS | `ruff check src/ tests/contract/ tests/unit/test_collection_stats.py` |

The module-by-module and operation-by-operation inventories, including their
individual PASS statuses, are maintained in
[`docs/TRACEABILITY.md`](../docs/TRACEABILITY.md). The full-suite result
includes the 13 unit modules and the OpenAPI contract module.
