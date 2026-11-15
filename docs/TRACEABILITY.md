# Personal Media Library System (PMLS) — Requirement Traceability Matrix (RTM-001)

**Document ID:** RTM-001  
**Source SRS:** spec/srs.md v1.0 (SRS-001)  
**Source Decomposition:** docs/jira-decomposition.csv  
**Version:** 1.0  
**Date:** 2026-10-19  
**Status:** Baseline  

---

## Purpose

This Requirement Traceability Matrix (RTM) is an artefact of the Software Design Document (SDD) process for the Personal Media Library System. It establishes a bidirectional link between every approved requirement in SRS-001 and the corresponding Jira work items produced during initial decomposition.

The matrix serves four purposes within the SDD lifecycle:

1. **Completeness assurance** — confirms that every functional requirement (REQ-F-001..066) and every constraint (CON-001..013) is covered by at least one Jira work item.
2. **Impact analysis** — when a requirement changes, the affected tickets are immediately identifiable.
3. **Verification accountability** — links each requirement to the Test and Verification ticket that will confirm its correct implementation.
4. **Scope enforcement** — supports ongoing compliance with the Scope Ceiling (CON-013) by making all covered items explicit.

The original 46 Jira work items were derived strictly from the approved SRS-001 v1.0 baseline. Addendum 001 adds TEST-016 and FEAT-013; it authorizes only the narrowly scoped local statistics exception to CON-013. All other exclusions remain binding.

---

## Traceability Table

| Requirement ID | Requirement Summary | Jira Issue ID | Jira Ticket Summary | Issue Type | Traceability (AC / BDD / VR) | Assignee Role | Status |
|---|---|---|---|---|---|---|---|
| REQ-F-001 | Allow user to create a new MediaItem | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-001; BDD-001, BDD-002, BDD-066 | Agent | To Do |
| REQ-F-001 | Allow user to create a new MediaItem | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-001; BDD-001, BDD-002, BDD-066 | Agent | To Do |
| REQ-F-002 | Name required at creation | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-001, AC-042; BDD-001, BDD-004, BDD-005; VR-001 | Agent | To Do |
| REQ-F-002 | Name required at creation | 8 | TEST-002: Тести — MediaItem Create (негативні сценарії / валідація) | Test | AC-042; BDD-004, BDD-005; VR-001 | Agent | To Do |
| REQ-F-002 | Name required at creation | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-001, AC-042; BDD-001, BDD-004, BDD-005; VR-001 | Agent | To Do |
| REQ-F-003 | Type required at creation | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-001; BDD-001, BDD-002, BDD-066; VR-008 | Agent | To Do |
| REQ-F-003 | Type required at creation | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-001; BDD-001, BDD-002, BDD-066; VR-008 | Agent | To Do |
| REQ-F-004 | Default status is *planned* at creation | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-002, AC-060; BDD-002, BDD-063, BDD-066 | Agent | To Do |
| REQ-F-004 | Default status is *planned* at creation | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-002, AC-060; BDD-002, BDD-063, BDD-066 | Agent | To Do |
| REQ-F-005 | Notes may be left empty at creation | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-003; BDD-001, BDD-003 | Agent | To Do |
| REQ-F-005 | Notes may be left empty at creation | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-003; BDD-001, BDD-003 | Agent | To Do |
| REQ-F-006 | Rating may be left unset at creation | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-003; BDD-001, BDD-003 | Agent | To Do |
| REQ-F-006 | Rating may be left unset at creation | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-003; BDD-001, BDD-003 | Agent | To Do |
| REQ-F-007 | Topics may be assigned at creation | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-004; BDD-002 | Agent | To Do |
| REQ-F-007 | Topics may be assigned at creation | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-004; BDD-002 | Agent | To Do |
| REQ-F-008 | Auto-save on successful creation | 7 | TEST-001: Тести — MediaItem Create (позитивні сценарії) | Test | AC-005; BDD-003, BDD-057 | Agent | To Do |
| REQ-F-008 | Auto-save on successful creation | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-005; BDD-003, BDD-057 | Agent | To Do |
| REQ-F-009 | View a MediaItem and all its fields | 9 | TEST-003: Тести — MediaItem View та Edit | Test | AC-006; BDD-009, BDD-010 | Agent | To Do |
| REQ-F-009 | View a MediaItem and all its fields | 23 | FEAT-002: Реалізація — MediaItem View та Edit | Feature | AC-006; BDD-009, BDD-010 | Agent | To Do |
| REQ-F-010 | Edit any field of a MediaItem | 9 | TEST-003: Тести — MediaItem View та Edit | Test | AC-007; BDD-011, BDD-012 | Agent | To Do |
| REQ-F-010 | Edit any field of a MediaItem | 23 | FEAT-002: Реалізація — MediaItem View та Edit | Feature | AC-007; BDD-011, BDD-012 | Agent | To Do |
| REQ-F-011 | Auto-save on successful edit | 9 | TEST-003: Тести — MediaItem View та Edit | Test | AC-007; BDD-011, BDD-012 | Agent | To Do |
| REQ-F-011 | Auto-save on successful edit | 23 | FEAT-002: Реалізація — MediaItem View та Edit | Feature | AC-007; BDD-011, BDD-012 | Agent | To Do |
| REQ-F-012 | Allow user to delete a MediaItem | 10 | TEST-004: Тести — MediaItem Delete | Test | AC-008; BDD-013 | Agent | To Do |
| REQ-F-012 | Allow user to delete a MediaItem | 24 | FEAT-003: Реалізація — MediaItem Delete | Feature | AC-008; BDD-013 | Agent | To Do |
| REQ-F-013 | Require confirmation before deletion | 10 | TEST-004: Тести — MediaItem Delete | Test | AC-008, AC-009; BDD-013, BDD-014 | Agent | To Do |
| REQ-F-013 | Require confirmation before deletion | 24 | FEAT-003: Реалізація — MediaItem Delete | Feature | AC-008, AC-009; BDD-013, BDD-014 | Agent | To Do |
| REQ-F-014 | Permanently remove on confirmed delete | 10 | TEST-004: Тести — MediaItem Delete | Test | AC-008; BDD-013 | Agent | To Do |
| REQ-F-014 | Permanently remove on confirmed delete | 24 | FEAT-003: Реалізація — MediaItem Delete | Feature | AC-008; BDD-013 | Agent | To Do |
| REQ-F-015 | Remove all Topic associations on item delete | 10 | TEST-004: Тести — MediaItem Delete | Test | AC-010; BDD-015 | Agent | To Do |
| REQ-F-015 | Remove all Topic associations on item delete | 24 | FEAT-003: Реалізація — MediaItem Delete | Feature | AC-010; BDD-015 | Agent | To Do |
| REQ-F-016 | Topics unaffected by MediaItem delete | 10 | TEST-004: Тести — MediaItem Delete | Test | AC-010; BDD-015 | Agent | To Do |
| REQ-F-016 | Topics unaffected by MediaItem delete | 24 | FEAT-003: Реалізація — MediaItem Delete | Feature | AC-010; BDD-015 | Agent | To Do |
| REQ-F-017 | Deleted MediaItem is not restorable | 10 | TEST-004: Тести — MediaItem Delete | Test | AC-011; BDD-016 | Agent | To Do |
| REQ-F-017 | Deleted MediaItem is not restorable | 24 | FEAT-003: Реалізація — MediaItem Delete | Feature | AC-011; BDD-016 | Agent | To Do |
| REQ-F-018 | Allow setting status to any of five values | 11 | TEST-005: Тести — MediaItem Status Management | Test | AC-012; BDD-017a, BDD-017b; VR-009 | Agent | To Do |
| REQ-F-018 | Allow setting status to any of five values | 25 | FEAT-004: Реалізація — MediaItem Status Management | Feature | AC-012; BDD-017a, BDD-017b; VR-009 | Agent | To Do |
| REQ-F-019 | Free status change, no workflow | 11 | TEST-005: Тести — MediaItem Status Management | Test | AC-012; BDD-017a, BDD-017b | Agent | To Do |
| REQ-F-019 | Free status change, no workflow | 25 | FEAT-004: Реалізація — MediaItem Status Management | Feature | AC-012; BDD-017a, BDD-017b | Agent | To Do |
| REQ-F-020 | Allow user to create a new Topic | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-013; BDD-018; VR-003, VR-004, VR-005 | Agent | To Do |
| REQ-F-020 | Allow user to create a new Topic | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-013; BDD-018 | Agent | To Do |
| REQ-F-021 | Auto-save on successful Topic creation | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-013; BDD-018 | Agent | To Do |
| REQ-F-021 | Auto-save on successful Topic creation | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-013; BDD-018 | Agent | To Do |
| REQ-F-022 | View a Topic and its associated MediaItems | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-014; BDD-023, BDD-024 | Agent | To Do |
| REQ-F-022 | View a Topic and its associated MediaItems | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-014; BDD-023, BDD-024 | Agent | To Do |
| REQ-F-023 | Allow user to rename a Topic | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-015; BDD-025 | Agent | To Do |
| REQ-F-023 | Allow user to rename a Topic | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-015; BDD-025 | Agent | To Do |
| REQ-F-024 | Rename preserves all MediaItem associations | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-015; BDD-025 | Agent | To Do |
| REQ-F-024 | Rename preserves all MediaItem associations | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-015; BDD-025 | Agent | To Do |
| REQ-F-025 | Auto-save on successful Topic rename | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-015; BDD-025 | Agent | To Do |
| REQ-F-025 | Auto-save on successful Topic rename | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-015; BDD-025 | Agent | To Do |
| REQ-F-026 | Allow user to delete a Topic | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-016; BDD-027 | Agent | To Do |
| REQ-F-026 | Allow user to delete a Topic | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-016; BDD-027 | Agent | To Do |
| REQ-F-027 | Require confirmation before Topic deletion | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-016, AC-017; BDD-027, BDD-028 | Agent | To Do |
| REQ-F-027 | Require confirmation before Topic deletion | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-016, AC-017; BDD-027, BDD-028 | Agent | To Do |
| REQ-F-028 | Remove Topic and associations on confirmed delete | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-016; BDD-027, BDD-029 | Agent | To Do |
| REQ-F-028 | Remove Topic and associations on confirmed delete | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-016; BDD-027, BDD-029 | Agent | To Do |
| REQ-F-029 | MediaItems unaffected by Topic delete | 12 | TEST-006: Тести — Topic Create View Rename Delete (позитивні) | Test | AC-016; BDD-029 | Agent | To Do |
| REQ-F-029 | MediaItems unaffected by Topic delete | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-016; BDD-029 | Agent | To Do |
| REQ-F-030 | Add Topic association from MediaItem side | 14 | TEST-008: Тести — Асоціація MediaItem–Topic (обидві сторони) | Test | AC-018; BDD-030, BDD-070 | Agent | To Do |
| REQ-F-030 | Add Topic association from MediaItem side | 27 | FEAT-006: Реалізація — MediaItem–Topic Association (обидві сторони) | Feature | AC-018; BDD-030, BDD-070 | Agent | To Do |
| REQ-F-031 | Remove Topic association from MediaItem side | 14 | TEST-008: Тести — Асоціація MediaItem–Topic (обидві сторони) | Test | AC-018; BDD-031 | Agent | To Do |
| REQ-F-031 | Remove Topic association from MediaItem side | 27 | FEAT-006: Реалізація — MediaItem–Topic Association (обидві сторони) | Feature | AC-018; BDD-031 | Agent | To Do |
| REQ-F-032 | Add MediaItem association from Topic side | 14 | TEST-008: Тести — Асоціація MediaItem–Topic (обидві сторони) | Test | AC-019; BDD-032 | Agent | To Do |
| REQ-F-032 | Add MediaItem association from Topic side | 27 | FEAT-006: Реалізація — MediaItem–Topic Association (обидві сторони) | Feature | AC-019; BDD-032 | Agent | To Do |
| REQ-F-033 | Remove MediaItem association from Topic side | 14 | TEST-008: Тести — Асоціація MediaItem–Topic (обидві сторони) | Test | AC-019; BDD-033 | Agent | To Do |
| REQ-F-033 | Remove MediaItem association from Topic side | 27 | FEAT-006: Реалізація — MediaItem–Topic Association (обидві сторони) | Feature | AC-019; BDD-033 | Agent | To Do |
| REQ-F-034 | Auto-save on successful association change | 14 | TEST-008: Тести — Асоціація MediaItem–Topic (обидві сторони) | Test | AC-020; BDD-030, BDD-032, BDD-034 | Agent | To Do |
| REQ-F-034 | Auto-save on successful association change | 27 | FEAT-006: Реалізація — MediaItem–Topic Association (обидві сторони) | Feature | AC-020; BDD-030, BDD-032, BDD-034 | Agent | To Do |
| REQ-F-035 | Navigate from Topic to associated MediaItem | 15 | TEST-009: Тести — Навігація Topic→MediaItem та MediaItem→Topic | Test | AC-021; BDD-035, BDD-070 | Agent | To Do |
| REQ-F-035 | Navigate from Topic to associated MediaItem | 28 | FEAT-007: Реалізація — Navigation (Topic↔MediaItem) | Feature | AC-021; BDD-035, BDD-070 | Agent | To Do |
| REQ-F-036 | Display all Topics a MediaItem belongs to | 15 | TEST-009: Тести — Навігація Topic→MediaItem та MediaItem→Topic | Test | AC-022; BDD-036, BDD-070 | Agent | To Do |
| REQ-F-036 | Display all Topics a MediaItem belongs to | 28 | FEAT-007: Реалізація — Navigation (Topic↔MediaItem) | Feature | AC-022; BDD-036, BDD-070 | Agent | To Do |
| REQ-F-037 | Navigate from MediaItem to associated Topic | 15 | TEST-009: Тести — Навігація Topic→MediaItem та MediaItem→Topic | Test | AC-022; BDD-036 | Agent | To Do |
| REQ-F-037 | Navigate from MediaItem to associated Topic | 28 | FEAT-007: Реалізація — Navigation (Topic↔MediaItem) | Feature | AC-022; BDD-036 | Agent | To Do |
| REQ-F-038 | Allow user to enter a search query | 16 | TEST-010: Тести — Search (пошук MediaItem та Topic) | Test | AC-023; BDD-037 | Agent | To Do |
| REQ-F-038 | Allow user to enter a search query | 29 | FEAT-008: Реалізація — Search | Feature | AC-023; BDD-037 | Agent | To Do |
| REQ-F-039 | Return MediaItems matching query by substring | 16 | TEST-010: Тести — Search (пошук MediaItem та Topic) | Test | AC-023, AC-026; BDD-037, BDD-039, BDD-067 | Agent | To Do |
| REQ-F-039 | Return MediaItems matching query by substring | 29 | FEAT-008: Реалізація — Search | Feature | AC-023, AC-026; BDD-037, BDD-039, BDD-067 | Agent | To Do |
| REQ-F-040 | Return Topics matching query by substring | 16 | TEST-010: Тести — Search (пошук MediaItem та Topic) | Test | AC-024, AC-026; BDD-038, BDD-039, BDD-067 | Agent | To Do |
| REQ-F-040 | Return Topics matching query by substring | 29 | FEAT-008: Реалізація — Search | Feature | AC-024, AC-026; BDD-038, BDD-039, BDD-067 | Agent | To Do |
| REQ-F-041 | Allow opening a Topic search result | 16 | TEST-010: Тести — Search (пошук MediaItem та Topic) | Test | AC-025; BDD-040 | Agent | To Do |
| REQ-F-041 | Allow opening a Topic search result | 29 | FEAT-008: Реалізація — Search | Feature | AC-025; BDD-040 | Agent | To Do |
| REQ-F-042 | Empty search query = search inactive | 16 | TEST-010: Тести — Search (пошук MediaItem та Topic) | Test | AC-027; BDD-041 | Agent | To Do |
| REQ-F-042 | Empty search query = search inactive | 29 | FEAT-008: Реалізація — Search | Feature | AC-027; BDD-041 | Agent | To Do |
| REQ-F-043 | Notes field not searched | 16 | TEST-010: Тести — Search (пошук MediaItem та Topic) | Test | AC-028; BDD-042 | Agent | To Do |
| REQ-F-043 | Notes field not searched | 29 | FEAT-008: Реалізація — Search | Feature | AC-028; BDD-042 | Agent | To Do |
| REQ-F-044 | Filter by media type | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-029; BDD-043 | Agent | To Do |
| REQ-F-044 | Filter by media type | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-029; BDD-043 | Agent | To Do |
| REQ-F-045 | Filter by status | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-030; BDD-044 | Agent | To Do |
| REQ-F-045 | Filter by status | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-030; BDD-044 | Agent | To Do |
| REQ-F-046 | Filter by rating range | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-031, AC-032, AC-033; BDD-045, BDD-046, BDD-047; VR-011 | Agent | To Do |
| REQ-F-046 | Filter by rating range | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-031, AC-032, AC-033; BDD-045, BDD-046, BDD-047; VR-011 | Agent | To Do |
| REQ-F-047 | Allow lower bound only, upper only, or both | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-031, AC-032, AC-033; BDD-045, BDD-046, BDD-047 | Agent | To Do |
| REQ-F-047 | Allow lower bound only, upper only, or both | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-031, AC-032, AC-033; BDD-045, BDD-046, BDD-047 | Agent | To Do |
| REQ-F-048 | Exclude unrated items when rating filter active | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-034; BDD-045, BDD-046, BDD-047 | Agent | To Do |
| REQ-F-048 | Exclude unrated items when rating filter active | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-034; BDD-045, BDD-046, BDD-047 | Agent | To Do |
| REQ-F-049 | Filter by Topic | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-035; BDD-049, BDD-050 | Agent | To Do |
| REQ-F-049 | Filter by Topic | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-035; BDD-049, BDD-050 | Agent | To Do |
| REQ-F-050 | Multiple simultaneous filters use AND logic | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-036; BDD-051, BDD-068 | Agent | To Do |
| REQ-F-050 | Multiple simultaneous filters use AND logic | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-036; BDD-051, BDD-068 | Agent | To Do |
| REQ-F-051 | Sort by name ascending | 18 | TEST-012: Тести — Sort (name та rating) | Test | AC-037; BDD-052 | Agent | To Do |
| REQ-F-051 | Sort by name ascending | 31 | FEAT-010: Реалізація — Sort (name та rating) | Feature | AC-037; BDD-052 | Agent | To Do |
| REQ-F-052 | Sort by name descending | 18 | TEST-012: Тести — Sort (name та rating) | Test | AC-038; BDD-053 | Agent | To Do |
| REQ-F-052 | Sort by name descending | 31 | FEAT-010: Реалізація — Sort (name та rating) | Feature | AC-038; BDD-053 | Agent | To Do |
| REQ-F-053 | Sort by rating ascending | 18 | TEST-012: Тести — Sort (name та rating) | Test | AC-039; BDD-054 | Agent | To Do |
| REQ-F-053 | Sort by rating ascending | 31 | FEAT-010: Реалізація — Sort (name та rating) | Feature | AC-039; BDD-054 | Agent | To Do |
| REQ-F-054 | Sort by rating descending | 18 | TEST-012: Тести — Sort (name та rating) | Test | AC-040; BDD-055 | Agent | To Do |
| REQ-F-054 | Sort by rating descending | 31 | FEAT-010: Реалізація — Sort (name та rating) | Feature | AC-040; BDD-055 | Agent | To Do |
| REQ-F-055 | Unrated items appear last in rating sort | 18 | TEST-012: Тести — Sort (name та rating) | Test | AC-039, AC-040; BDD-054, BDD-055 | Agent | To Do |
| REQ-F-055 | Unrated items appear last in rating sort | 31 | FEAT-010: Реалізація — Sort (name та rating) | Feature | AC-039, AC-040; BDD-054, BDD-055 | Agent | To Do |
| REQ-F-056 | Tie order is unspecified (by design) | 31 | FEAT-010: Реалізація — Sort (name та rating) | Feature | _(intentional gap — no AC/BDD by specification)_ | Agent | To Do |
| REQ-F-057 | Search, filter, and sort combinable | 19 | TEST-013: Тести — Combined Search+Filter+Sort | Test | AC-041; BDD-056, BDD-069 | Agent | To Do |
| REQ-F-057 | Search, filter, and sort combinable | 32 | FEAT-011: Реалізація — Combined Search+Filter+Sort | Feature | AC-041; BDD-056, BDD-069 | Agent | To Do |
| REQ-F-058 | Combined: filter first, then sort | 19 | TEST-013: Тести — Combined Search+Filter+Sort | Test | AC-041; BDD-056, BDD-069 | Agent | To Do |
| REQ-F-058 | Combined: filter first, then sort | 32 | FEAT-011: Реалізація — Combined Search+Filter+Sort | Feature | AC-041; BDD-056, BDD-069 | Agent | To Do |
| REQ-F-059 | Auto-save every successful data change | 20 | TEST-014: Тести — Auto-save та Persistence | Test | AC-049, AC-061; BDD-012, BDD-064 | Agent | To Do |
| REQ-F-059 | Auto-save every successful data change | 33 | FEAT-012: Реалізація — Auto-save та Persistence Layer | Feature | AC-049, AC-061; BDD-012, BDD-064 | Agent | To Do |
| REQ-F-060 | Notify user when auto-save fails | 21 | TEST-015: Тести — Save Failure Notification | Test | AC-050, AC-062; BDD-058 | Agent | To Do |
| REQ-F-060 | Notify user when auto-save fails | 33 | FEAT-012: Реалізація — Auto-save та Persistence Layer | Feature | AC-050, AC-062; BDD-058 | Agent | To Do |
| REQ-F-061 | Retain unsaved change in current session | 21 | TEST-015: Тести — Save Failure Notification | Test | AC-051, AC-062; BDD-059 | Agent | To Do |
| REQ-F-061 | Retain unsaved change in current session | 33 | FEAT-012: Реалізація — Auto-save та Persistence Layer | Feature | AC-051, AC-062; BDD-059 | Agent | To Do |
| REQ-F-062 | Reject empty or whitespace-only MediaItem name | 8 | TEST-002: Тести — MediaItem Create (негативні сценарії / валідація) | Test | AC-042; BDD-004, BDD-005; VR-001, VR-002 | Agent | To Do |
| REQ-F-062 | Reject empty or whitespace-only MediaItem name | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-042; BDD-004, BDD-005; VR-001, VR-002 | Agent | To Do |
| REQ-F-063 | Reject invalid or non-unique Topic name | 13 | TEST-007: Тести — Topic Validation (негативні) | Test | AC-045, AC-046; BDD-019, BDD-020, BDD-021, BDD-026; VR-003, VR-004, VR-005, VR-006 | Agent | To Do |
| REQ-F-063 | Reject invalid or non-unique Topic name | 26 | FEAT-005: Реалізація — Topic CRUD (Create View Rename Delete) | Feature | AC-045, AC-046; BDD-019, BDD-020, BDD-021, BDD-026; VR-003, VR-004, VR-005, VR-006 | Agent | To Do |
| REQ-F-064 | Reject MediaItem rating outside 1–10 | 8 | TEST-002: Тести — MediaItem Create (негативні сценарії / валідація) | Test | AC-044; BDD-007, BDD-008; VR-007 | Agent | To Do |
| REQ-F-064 | Reject MediaItem rating outside 1–10 | 22 | FEAT-001: Реалізація — MediaItem Create | Feature | AC-044; BDD-007, BDD-008; VR-007 | Agent | To Do |
| REQ-F-065 | Reject rating filter where lower > upper | 17 | TEST-011: Тести — Filter (type status rating topic) | Test | AC-048; BDD-048; VR-010 | Agent | To Do |
| REQ-F-065 | Reject rating filter where lower > upper | 30 | FEAT-009: Реалізація — Filter (type status rating topic) | Feature | AC-048; BDD-048; VR-010 | Agent | To Do |
| REQ-F-066 | Notify user of save failure (mechanism unspecified) | 21 | TEST-015: Тести — Save Failure Notification | Test | AC-050; BDD-058 | Agent | To Do |
| REQ-F-066 | Notify user of save failure (mechanism unspecified) | 33 | FEAT-012: Реалізація — Auto-save та Persistence Layer | Feature | AC-050; BDD-058 | Agent | To Do |
| CON-001 | Fixed media type set (7 values) | 2 | SPEC-001: Специфікація домену — MediaItem | Specification | AC-064; BDD-001, BDD-002 | Agent | To Do |
| CON-001 | Fixed media type set (7 values) | 34 | VER-001: Верифікація — MediaItem CRUD відповідає SRS | Verification | AC-064 | Agent | To Do |
| CON-002 | Fixed status value set (5 values) | 2 | SPEC-001: Специфікація домену — MediaItem | Specification | AC-065; BDD-017a, BDD-017b | Agent | To Do |
| CON-002 | Fixed status value set (5 values) | 34 | VER-001: Верифікація — MediaItem CRUD відповідає SRS | Verification | AC-065 | Agent | To Do |
| CON-003 | Rating domain: integer 1–10 or absent | 2 | SPEC-001: Специфікація домену — MediaItem | Specification | AC-044; BDD-007, BDD-008; VR-007 | Agent | To Do |
| CON-003 | Rating domain: integer 1–10 or absent | 34 | VER-001: Верифікація — MediaItem CRUD відповідає SRS | Verification | AC-044 | Agent | To Do |
| CON-004 | Uniform MediaItem field structure; no type-specific fields | 2 | SPEC-001: Специфікація домену — MediaItem | Specification | AC-066 | Agent | To Do |
| CON-004 | Uniform MediaItem field structure; no type-specific fields | 34 | VER-001: Верифікація — MediaItem CRUD відповідає SRS | Verification | AC-066 | Agent | To Do |
| CON-005 | No date-added field | 2 | SPEC-001: Специфікація домену — MediaItem | Specification | AC-067 | Agent | To Do |
| CON-005 | No date-added field | 34 | VER-001: Верифікація — MediaItem CRUD відповідає SRS | Verification | AC-067 | Agent | To Do |
| CON-006 | Single notes field per MediaItem | 2 | SPEC-001: Специфікація домену — MediaItem | Specification | _(enforced by model; no dedicated AC)_ | Agent | To Do |
| CON-007 | Topic name uniqueness: case-insensitive post-normalisation | 3 | SPEC-002: Специфікація домену — Topic | Specification | AC-046, AC-047; BDD-020, BDD-021, BDD-022, BDD-026; VR-005, VR-006 | Agent | To Do |
| CON-007 | Topic name uniqueness: case-insensitive post-normalisation | 35 | VER-002: Верифікація — Topic CRUD відповідає SRS | Verification | AC-046, AC-047 | Agent | To Do |
| CON-008 | Single local user; no multi-user architecture | 39 | VER-006: Верифікація — Scope Ceiling CON-013 | Verification | AC-058; BDD-061 | Agent | To Do |
| CON-009 | No network component | 39 | VER-006: Верифікація — Scope Ceiling CON-013 | Verification | AC-068; BDD-060 | Agent | To Do |
| CON-010 | All data stored locally; no external transmission | 39 | VER-006: Верифікація — Scope Ceiling CON-013 | Verification | AC-056; BDD-060 | Agent | To Do |
| CON-011 | English user-facing text only | 39 | VER-006: Верифікація — Scope Ceiling CON-013 | Verification | AC-057; BDD-065 | Agent | To Do |
| CON-012 | Platform and technology stack not prescribed | 45 | DOC-002: Документація — Architecture Decision Records (ADR) | Documentation | _(specification meta-constraint; documented in ADR)_ | Agent | To Do |
| CON-013 | Excluded features — Scope Ceiling | 39 | VER-006: Верифікація — Scope Ceiling CON-013 | Verification | AC-069; BDD-060, BDD-061, BDD-062 | Agent | To Do |

---

## Addendum 001 — Collection Statistics

The following links extend the baseline RTM for the additive, read-only
`GET /api/stats` feature. AC-070..075 and BDD-071..075 are unique identifiers
introduced by the addendum; baseline AC-047..052 retain their original meaning.

| Requirement ID | Requirement Summary | Jira Issue ID | Jira Ticket Summary | Issue Type | Traceability (AC / BDD) | Assignee Role | Status |
|---|---|---|---|---|---|---|---|
| REQ-F-070 | Return collection-wide MediaItem and Topic totals | 47 | TEST-016: Тести — Collection Statistics | Test | AC-070, AC-074; BDD-071 | Agent | To Do |
| REQ-F-070 | Return collection-wide MediaItem and Topic totals | 48 | FEAT-013: Реалізація — Collection Statistics | Feature | AC-070, AC-074; BDD-071 | Agent | To Do |
| REQ-F-071 | Return complete status and media-type distributions | 47 | TEST-016: Тести — Collection Statistics | Test | AC-071, AC-074; BDD-071, BDD-072 | Agent | To Do |
| REQ-F-071 | Return complete status and media-type distributions | 48 | FEAT-013: Реалізація — Collection Statistics | Feature | AC-071, AC-074; BDD-071, BDD-072 | Agent | To Do |
| REQ-F-072 | Return average rating and rated count | 47 | TEST-016: Тести — Collection Statistics | Test | AC-072, AC-074; BDD-071, BDD-072 | Agent | To Do |
| REQ-F-072 | Return average rating and rated count | 48 | FEAT-013: Реалізація — Collection Statistics | Feature | AC-072, AC-074; BDD-071, BDD-072 | Agent | To Do |
| REQ-F-073 | Return sorted per-Topic association counts | 47 | TEST-016: Тести — Collection Statistics | Test | AC-073; BDD-073 | Agent | To Do |
| REQ-F-073 | Return sorted per-Topic association counts | 48 | FEAT-013: Реалізація — Collection Statistics | Feature | AC-073; BDD-073 | Agent | To Do |
| REQ-F-074 | Log statistics request outcome without user-authored data | 47 | TEST-016: Тести — Collection Statistics | Test | AC-075; BDD-074, BDD-075 | Agent | To Do |
| REQ-F-074 | Log statistics request outcome without user-authored data | 48 | FEAT-013: Реалізація — Collection Statistics | Feature | AC-075; BDD-074, BDD-075 | Agent | To Do |
| CON-013 / AC-069 exception | Local read-only collection statistics are permitted only by Addendum 001; all other exclusions remain | 39 | VER-006: Верифікація — Scope Ceiling CON-013 | Verification | AC-069 is qualified only for this feature; AC-075 verifies the limited exception | Agent | To Do |

### Addendum Coverage

| Category | Baseline | Addendum 001 | Current total |
|---|---:|---:|---:|
| Functional requirements | 66 | 5 | 71 |
| Acceptance criteria | 69 | 6 | 75 |
| BDD scenarios | 70 | 5 | 75 |
| Work items | 46 | 2 | 48 |

---

## Gate Tickets

The following Gate tickets are not mapped to individual requirements but serve as lifecycle control points that block downstream phases until a human approves progress.

| Jira Issue ID | Gate Summary | Blocks Issue ID | Assignee Role | Status |
|---|---|---|---|---|
| 1 | PLAN-GATE: Специфікацію затверджено — дозвіл на старт реалізації | 2 (SPEC-001) | Human | To Do |
| 40 | DATA-PERSISTENCE-GATE: Дані зберігаються коректно — дозвіл на продовження | 41 (VALID-001) | Human | To Do |
| 46 | RELEASE-GATE: Release Gate — система готова до релізу | _(end of chain)_ | Human | To Do |

---

## Coverage Summary

### Requirement Counts

| Category | Count | Covered | Coverage Rate |
|---|---|---|---|
| Baseline Functional Requirements (REQ-F-001..REQ-F-066) | 66 | 66 | 100% |
| Constraints (CON-001..CON-013) | 13 | 13 | 100% |
| **Baseline total** | **79** | **79** | **100%** |

Addendum 001 contributes five additional functional requirements (REQ-F-070..074),
six acceptance criteria (AC-070..075), five BDD scenarios (BDD-071..075), and
two work items. See **Addendum 001 — Collection Statistics** above.

> **Note on REQ-F-056 (tie order):** Covered by FEAT-010 with an intentional documentation gap — the SRS explicitly states that tie order is unspecified and no AC or BDD scenario is possible by design (see SRS-001 §12.2).

> **Note on CON-006 (single notes field):** Enforced by the approved domain model. No dedicated AC exists by design; coverage is via model inspection (see SRS-001 §12.2).

> **Note on CON-012 (platform independence):** A specification meta-constraint. Covered via ADR documentation (DOC-002) rather than runtime testing (see SRS-001 §12.2).

### Work Item Counts

| Issue Type | Count | Assignee Role |
|---|---|---|
| Gate | 3 | Human |
| Specification | 5 | Agent |
| Test | 16 | Agent |
| Feature | 13 | Agent |
| Verification | 6 | Agent |
| Validation | 3 | Human |
| Documentation | 2 | Agent |
| **Total** | **48** | |

### Role Split

| Role | Count | Percentage |
|---|---|---|
| Agent | 42 | 87.5% |
| Human | 6 | 12.5% |

### Traceability Artefact Coverage

| Artefact Type | Total in SRS-001 | Linked in This RTM |
|---|---|---|
| Acceptance Criteria (AC) | 75 | 75 (69 baseline + 6 addendum) |
| BDD Scenarios | 75 | 75 (70 baseline + 5 addendum) |
| Validation Rules (VR) | 11 | 11 |
| Business Rules (BR) | 10 | via REQ-F |

---

*End of RTM-001 — Version 1.0 with Addendum 001*
*Source: spec/srs.md v1.0 · spec/addendum-001-collection-stats.md · docs/jira-decomposition.csv*
