# Software Requirements Specification

**Project:** Personal Media Library System
**Document ID:** SRS-001
**Version:** 1.0
**Date:** 2026-10-04
**Status:** Baseline

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Scope](#3-system-scope)
4. [Domain Glossary](#4-domain-glossary)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Interface Requirements](#7-interface-requirements)
8. [Constraints](#8-constraints)
9. [Acceptance Criteria](#9-acceptance-criteria)
10. [BDD Scenarios](#10-bdd-scenarios)
11. [Traceability Matrix](#11-traceability-matrix)
12. [Verification Summary](#12-verification-summary)
    - [Addendum 001 implementation verification](#126-addendum-001-implementation-verification)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the complete, approved requirements baseline for the Personal Media Library System. It is the authoritative reference for all subsequent design, implementation, testing, and acceptance activities.

This document is the product of a structured SKED (Structured Knowledge Elicitation Dialogue) requirements-engineering process. All requirements originate from explicit human decisions (HD-001 through HD-068) made during that process. No requirement in this document was introduced without a traceable human decision.

### 1.2 Scope

The system is a personal media tracking application that enables a single local user to record, organise, and review media content they have consumed or plan to consume. The system allows the user to store MediaItems, assign them to user-defined Topics, record personal notes and ratings, track consumption status, and retrieve items through search, filtering, and sorting.

The system is not a content delivery platform, a social network, a recommendation engine, or a metadata aggregation service.

The current implementation also provides the narrowly scoped, local,
read-only collection summary specified by SRS-ADD-001. This addendum qualifies
the original exclusion of statistics; it does not permit external metadata
aggregation or other excluded analytics.

### 1.3 Intended Audience

This SRS is intended for:

- Developers implementing the system
- Testers verifying conformance to requirements
- Reviewers assessing specification completeness
- Stakeholders confirming that the specified system matches their intent

### 1.4 References

The following artifacts were produced during the SKED elicitation phase and are incorporated by reference:

| Artifact | Description |
|---|---|
| `spec/idea.md` | Initial project idea document |
| `logs/conflict-resolution.md` | Record of the media-topic relationship conflict resolution |
| SKED Dialogue (iterations 1–7) | Structured elicitation producing HD-001 through HD-068 |
| Approved Domain Glossary | Canonical terminology definitions |
| Approved System Scope | In-scope and out-of-scope boundaries |
| Approved Functional Requirements baseline | REQ-F-001 through REQ-F-066 |
| Approved NFR baseline | REQ-NF-001 through REQ-NF-011 |
| Approved Interface Requirements baseline | IR-001 through IR-043 |
| Approved Constraints baseline | CON-001 through CON-013 |
| Approved Acceptance Criteria baseline | AC-001 through AC-069 |
| Approved BDD Scenarios (corrected) | BDD-001 through BDD-070 |
| Approved addenda | SRS-ADD-001 — Collection Statistics (narrowly qualifies CON-013 and AC-069) |

### 1.5 Document Conventions

- **shall** — denotes a mandatory requirement.
- **should** — denotes a recommended but non-mandatory property (not used in normative requirements in this document).
- **REQ-F-NNN** — Functional Requirement identifier.
- **REQ-NF-NNN** — Non-Functional Requirement identifier.
- **IR-NNN** — Interface Requirement identifier.
- **CON-NNN** — Constraint identifier.
- **AC-NNN** — Acceptance Criterion identifier.
- **BDD-NNN** — BDD Scenario identifier.
- **BR-NNN** — Business Rule identifier.
- **VR-NNN** — Validation Rule identifier.
- **HD-NNN** — Human Decision identifier (SKED source traceability).

---

## 2. Overall Description

### 2.1 Product Perspective

The Personal Media Library System is a standalone application for a single local user. It has no predecessor system, no external system dependencies, and no network connectivity requirements. It operates entirely on the user's local machine. Data is stored locally and is not shared, synchronised, or transmitted externally.

### 2.2 Product Functions (High-Level Summary)

The system provides the following major capability groups:

1. **MediaItem management** — Create, view, edit, and permanently delete individual media records with a defined set of fields.
2. **Topic management** — Create, view, rename, and permanently delete user-defined named categories.
3. **Association management** — Establish and remove many-to-many links between MediaItems and Topics from either side.
4. **Navigation** — Move between MediaItems and Topics in both directions.
5. **Search** — Find MediaItems and Topics by name using substring, case-insensitive matching.
6. **Filtering** — Restrict the MediaItem list by type, status, rating range, and Topic.
7. **Sorting** — Order the MediaItem list by name or rating in ascending or descending direction.
8. **Combined operations** — Apply search, filters, and sorting simultaneously.
9. **Automatic persistence** — Save all successful changes without requiring a user Save action.
10. **Failure notification** — Inform the user when a save operation fails, while retaining the unsaved change for the current session.
11. **Collection statistics** — Summarize local collection totals, status/type
    distributions, ratings, and Topic associations as specified by SRS-ADD-001.

### 2.3 User Characteristics

The system serves exactly one local user per installation. No user account, login, or profile is required. The user is assumed to be a literate adult capable of operating a standard application on their local machine. No specialised technical knowledge is required; the system must be operable without consulting external documentation (REQ-NF-002).

### 2.4 Operating Environment

- **User model:** Single local user. No multi-user, networked, or cloud deployment.
- **Network:** No Internet connection required for any in-scope operation.
- **Platform:** Not yet specified. The specification is platform-independent.
- **Language:** English only.
- **Data storage:** Local to the user's machine. Specific storage technology is not prescribed.

### 2.5 Design and Implementation Constraints

See Section 8 (Constraints) for the complete list. Key constraints include:

- Fixed predefined media type set (seven values).
- Fixed predefined status value set (five values).
- Uniform MediaItem field structure for all media types.
- No date-added field.
- Topic name uniqueness enforced case-insensitively after normalisation.
- No network component permitted.
- All user-facing text in English.
- Platform and technology stack not prescribed.

### 2.6 Assumptions and Dependencies

- The operating system provides sufficient file-system or storage access for local data persistence.
- The operating system is responsible for access control to locally stored data. The application does not implement application-level access control.
- No external services, APIs, or data sources are assumed to exist or be available.

---

## 3. System Scope

### 3.1 In-Scope Capabilities

The following capabilities are within scope for the current version.

**MediaItem management**
- Create a MediaItem with required name, required type, defaulted status, and optional notes, rating, and Topic assignments.
- View a MediaItem and all its fields.
- Edit any field of a MediaItem.
- Delete a MediaItem with prior confirmation. Deletion is permanent.

**Topic management**
- Create a Topic with a unique name.
- View a Topic and its associated MediaItems.
- Rename a Topic, preserving associations and enforcing uniqueness on the new name.
- Delete a Topic with prior confirmation. Deletion removes the Topic and its associations; MediaItems are unaffected.

**MediaItem–Topic association**
- Add and remove Topic associations from the MediaItem side.
- Add and remove MediaItem associations from the Topic side.
- Navigate from Topic to associated MediaItems.
- Navigate from MediaItem to associated Topics.

**Status management**
- Set and change MediaItem status freely among the five predefined values.

**Search**
- Substring, case-insensitive search over MediaItem names and Topic names.
- Unified results list with results identified as MediaItem or Topic.

**Filtering**
- Filter by media type, status, rating range, and Topic.
- Multiple simultaneous filters with AND logic.

**Sorting**
- Sort by name or rating, ascending or descending.
- Unrated MediaItems appear after rated items in both sort directions.

**Combined operations**
- Simultaneous search, filter, and sort.

**Persistence**
- Auto-save all successful changes.
- Notify user on save failure; retain unsaved change for the session.

**Collection statistics**
- Provide a read-only summary of local collection totals, status/type
  distributions, ratings, and Topic associations, as specified by
  SRS-ADD-001.

### 3.2 Out-of-Scope Capabilities

The following are explicitly excluded from the current version.

| Excluded capability | Basis |
|---|---|
| Authentication, login, passwords, accounts | HD-007, HD-046 |
| Multiple users, profiles, or profile switching | HD-003, HD-005, HD-007 |
| Collaboration, sharing, multi-user access | HD-008 |
| External metadata retrieval | HD-027, HD-034 |
| Import from or export to external files or services | HD-034 |
| Built-in backup or restore | HD-034 |
| Statistics, analytics, or summary views, except the local read-only collection statistics narrowly specified by SRS-ADD-001 | HD-034; SRS-ADD-001 |
| Cloud storage or synchronisation | HD-034 |
| Multilingual or internationalisation support | HD-045 |
| Special accessibility features | HD-044 |
| Connection-related UI or online mode | HD-068 |
| User-defined custom media types | HD-010 |
| Type-specific MediaItem attributes | HD-014 |
| Date-added or creation-timestamp field | HD-032 |
| Multiple notes per MediaItem or separate notes subsystem | HD-019 |
| Search within notes | HD-025 |
| Secondary sort order for ties | HD-061 |
| Undo, redo, or recycle bin for deleted items | HD-022 |
| Mandatory explicit Save action | HD-042 |
| Recommendations, automatic categorisation | HD-034 |
| Notifications other than save-failure notification | HD-034 |

---


## 4. Domain Glossary

All terms below are canonical. No synonyms are introduced unless explicitly defined here.

| Term | Definition | Related Terms | Source |
|---|---|---|---|
| **MediaItem** | The primary domain object. Represents one unit of media content recorded by the user. Fields: id, name (required), type, status, notes (optional), rating (optional), Topics (zero or more). | Topic, Media type, Status, Rating, Notes | HD-011 |
| **Personal library** | The complete collection of all MediaItems and Topics stored by the user. | MediaItem, Topic | spec/idea.md, HD-002 |
| **Media type** | A fixed classification of the kind of media a MediaItem represents. Each MediaItem has exactly one type from the predefined set. | MediaItem | HD-010 |
| **book** | Media type: a written work consumed by reading. | Media type | HD-010 |
| **movie** | Media type: a feature-length film. | Media type | HD-010 |
| **TV series** | Media type: a serialised audiovisual production with multiple episodes or seasons. | Media type | HD-010 |
| **article** | Media type: a written piece shorter than a book (news article, essay, online post). | Media type | HD-010 |
| **podcast** | Media type: an episodic audio programme. | Media type | HD-010 |
| **video** | Media type: a video item that is not a movie or TV series. | Media type | HD-010 |
| **other** | Media type: a catch-all for content not fitting the six named types. | Media type | HD-010 |
| **Status** | A required field recording the user's current consumption state. Five predefined values; no workflow enforcement. | MediaItem | HD-012, HD-021 |
| **planned** | Status: the user intends to consume the item but has not started. | Status | HD-021 |
| **in progress** | Status: the user is currently consuming the item. | Status | HD-021 |
| **postponed** | Status: the user has paused and intends to return. Distinct from abandoned by the intent to resume. | Status, abandoned | HD-021 |
| **abandoned** | Status: the user has stopped with no intent to return. Distinct from postponed by the absence of intent to resume. | Status, postponed | HD-021 |
| **completed** | Status: the user has finished consuming the item. | Status | HD-021 |
| **Notes** | An optional free-text field on a MediaItem. One field per item. Edited with the MediaItem. Not searchable. | MediaItem | HD-011, HD-019, HD-025 |
| **Rating** | An optional field representing the user's personal evaluation. When present, an integer 1–10. Absence is distinct from any numeric value. | MediaItem, Unrated MediaItem | HD-011, HD-052 |
| **Unrated MediaItem** | A MediaItem whose rating has not been set. Excluded from rating-filtered results. Sorted after rated items when sorting by rating. | Rating, Rating filter | HD-036, HD-059, HD-060 |
| **Topic** | A user-defined named category for grouping MediaItems. Identified by its name. May exist with zero MediaItems. | MediaItem, Topic association | HD-015, HD-023 |
| **Topic name** | The identifying attribute of a Topic. Unique case-insensitively after normalisation. | Topic, Normalisation | HD-015, HD-050, HD-051 |
| **Topic association** | A link between one MediaItem and one Topic. No attributes beyond the two connected entities. Manageable from either side. | MediaItem, Topic | HD-038 |
| **MediaItem–Topic relationship** | The many-to-many relationship: one MediaItem may belong to zero or more Topics; one Topic may contain zero or more MediaItems. Deletion of either entity removes associations; the other entity is unaffected. | MediaItem, Topic, Topic association | HD-000, HD-016, HD-022 |
| **Normalisation** | Removal of leading and trailing whitespace from a text value before saving or uniqueness checking. Applied to MediaItem names and Topic names. | MediaItem name, Topic name | HD-049, HD-051 |
| **Search** | An operation finding MediaItems and Topics whose names contain the search query as a substring, case-insensitively. Does not inspect notes. | Search query, Substring match | HD-025, HD-026, HD-053–055 |
| **Search query** | The text string entered by the user to drive a search. Empty query means search is inactive. | Search | HD-053 |
| **Substring match** | Matching strategy: the query appears anywhere in the field value; case differences ignored. | Search | HD-026, HD-054 |
| **Topic search result** | A Topic returned when its name matches the search query. The user can open it to view associated MediaItems. | Search, Topic | HD-055 |
| **Filter** | A constraint restricting which MediaItems are displayed. Four types: type, status, rating, topic. Multiple active filters use AND logic. | Type filter, Status filter, Rating filter, Topic filter | HD-029, HD-030 |
| **Type filter** | Filter restricting to a specific media type. | Filter | HD-029 |
| **Status filter** | Filter restricting to a specific status value. | Filter | HD-029 |
| **Rating filter** | Filter restricting by rating range. Lower bound, upper bound, or both. Unrated MediaItems always excluded. | Filter, Rating, Unrated MediaItem | HD-035, HD-056–059 |
| **Rating lower bound** | Minimum rating (inclusive) for the rating filter. | Rating filter | HD-056 |
| **Rating upper bound** | Maximum rating (inclusive) for the rating filter. | Rating filter | HD-056 |
| **Topic filter** | Filter restricting to MediaItems associated with a specific Topic. | Filter, Topic | HD-029 |
| **AND logic** | Combination rule: a MediaItem is included only if it satisfies all active filters simultaneously. | Filter | HD-030 |
| **Sort** | Operation ordering the MediaItem list by a specified field and direction. | Sort field, Ascending, Descending | HD-031 |
| **Sort field** | The attribute used for ordering. Supported: name (alphabetical) and rating (numeric). | Sort | HD-031 |
| **Ascending** | Sort direction: smallest to largest (A–Z for name; lowest to highest for rating). Unrated items appear last. | Sort | HD-031, HD-060 |
| **Descending** | Sort direction: largest to smallest (Z–A for name; highest to lowest for rating). Unrated items appear last. | Sort | HD-031, HD-060 |
| **Tie** | Condition where two MediaItems have equal values for the active sort field. Relative order of tied items is unspecified. | Sort | HD-061 |
| **Auto-save** | Automatic persistence of every successful data change without a user Save action. | Save failure, Session | HD-042, HD-062 |
| **Save failure** | A condition where auto-save does not succeed. The user is notified; the unsaved change remains available for the session. | Auto-save, Session | HD-063–065 |
| **Session** | The period from application launch to close. Unsaved changes after a save failure are available only for the current session. | Auto-save, Save failure | HD-064 |

---


## 5. Functional Requirements

### 5.1 MediaItem Management

#### 5.1.1 Create

**REQ-F-001** The system shall allow the user to create a new MediaItem.
**REQ-F-002** When creating a MediaItem, the system shall require the user to provide a name.
**REQ-F-003** When creating a MediaItem, the system shall require the user to select a media type from the predefined set.
**REQ-F-004** When creating a MediaItem, the system shall assign *planned* as the default status if the user does not select a status.
**REQ-F-005** When creating a MediaItem, the system shall allow the user to leave the notes field empty.
**REQ-F-006** When creating a MediaItem, the system shall allow the user to leave the rating unset.
**REQ-F-007** When creating a MediaItem, the system shall allow the user to assign the new MediaItem to zero or more Topics at creation time.
**REQ-F-008** The system shall auto-save a newly created MediaItem upon successful creation.

*Traceability: HD-011, HD-037, HD-042, HD-062.*

#### 5.1.2 View

**REQ-F-009** The system shall allow the user to view a MediaItem and all of its fields: name, type, status, notes, rating, and associated Topics.

*Traceability: HD-011, HD-039.*

#### 5.1.3 Edit

**REQ-F-010** The system shall allow the user to edit any field of an existing MediaItem: name, type, status, notes, and rating.
**REQ-F-011** The system shall auto-save a MediaItem upon successful edit.

*Traceability: HD-011, HD-017, HD-042, HD-062.*

#### 5.1.4 Delete

**REQ-F-012** The system shall allow the user to delete a MediaItem.
**REQ-F-013** Before executing a deletion, the system shall require the user to confirm the delete action.
**REQ-F-014** Upon confirmed deletion, the system shall permanently remove the MediaItem.
**REQ-F-015** Upon confirmed deletion of a MediaItem, the system shall remove all Topic associations belonging to that MediaItem.
**REQ-F-016** Upon confirmed deletion of a MediaItem, the system shall not delete or modify any Topic.
**REQ-F-017** A deleted MediaItem shall not be restorable.

*Traceability: HD-017, HD-022, HD-040.*

#### 5.1.5 Status Management

**REQ-F-018** The system shall allow the user to set the status of a MediaItem to any of the five values: *planned*, *in progress*, *postponed*, *abandoned*, *completed*.
**REQ-F-019** The system shall allow the user to change the status of a MediaItem to any other valid status value at any time without enforcing a transition workflow.

*Traceability: HD-012, HD-021.*

---

### 5.2 Topic Management

#### 5.2.1 Create

**REQ-F-020** The system shall allow the user to create a new Topic by providing a name.
**REQ-F-021** The system shall auto-save a newly created Topic upon successful creation.

*Traceability: HD-015, HD-018, HD-042, HD-062.*

#### 5.2.2 View

**REQ-F-022** The system shall allow the user to view a Topic, displaying its name and all MediaItems currently associated with it.

*Traceability: HD-018, HD-039.*

#### 5.2.3 Rename

**REQ-F-023** The system shall allow the user to rename an existing Topic.
**REQ-F-024** When a Topic is renamed, all existing MediaItem associations with that Topic shall be preserved.
**REQ-F-025** The system shall auto-save a Topic rename upon successful completion.

*Traceability: HD-018, HD-024, HD-042, HD-062.*

#### 5.2.4 Delete

**REQ-F-026** The system shall allow the user to delete a Topic.
**REQ-F-027** Before executing a Topic deletion, the system shall require the user to confirm the delete action.
**REQ-F-028** Upon confirmed deletion, the system shall permanently remove the Topic and all of its MediaItem associations.
**REQ-F-029** Upon confirmed deletion of a Topic, the system shall not delete or modify any MediaItem.

*Traceability: HD-016, HD-018, HD-040.*

---

### 5.3 MediaItem–Topic Association

**REQ-F-030** The system shall allow the user to add a MediaItem to one or more Topics while viewing or editing that MediaItem.
**REQ-F-031** The system shall allow the user to remove a MediaItem from a Topic while viewing or editing that MediaItem.
**REQ-F-032** The system shall allow the user to add a MediaItem to a Topic while viewing that Topic.
**REQ-F-033** The system shall allow the user to remove a MediaItem from a Topic while viewing that Topic.
**REQ-F-034** The system shall auto-save any association change upon successful completion.

*Traceability: HD-000, HD-038, HD-042, HD-062.*

---

### 5.4 Navigation

**REQ-F-035** The system shall allow the user, while viewing a Topic, to open any MediaItem associated with that Topic.
**REQ-F-036** The system shall allow the user, while viewing a MediaItem, to see all Topics to which that MediaItem belongs.
**REQ-F-037** The system shall allow the user, while viewing a MediaItem, to open any Topic to which that MediaItem belongs.

*Traceability: HD-039, spec/idea.md.*

---

### 5.5 Search

**REQ-F-038** The system shall allow the user to enter a search query against the personal library.
**REQ-F-039** When the search query is non-empty, the system shall return all MediaItems whose name contains the search query as a substring, matched case-insensitively.
**REQ-F-040** When the search query is non-empty, the system shall return all Topics whose name contains the search query as a substring, matched case-insensitively.
**REQ-F-041** When a Topic is returned as a search result, the system shall allow the user to open that Topic to view its associated MediaItems.
**REQ-F-042** When the search query is empty, the system shall treat search as inactive and shall not restrict results on the basis of search.
**REQ-F-043** Search shall not inspect or match against the notes field of any MediaItem.

*Traceability: HD-025, HD-026, HD-053, HD-054, HD-055.*

---

### 5.6 Filtering

**REQ-F-044** The system shall allow the user to filter the MediaItem list by media type, restricting results to MediaItems of the selected type.
**REQ-F-045** The system shall allow the user to filter the MediaItem list by status, restricting results to MediaItems with the selected status.
**REQ-F-046** The system shall allow the user to filter the MediaItem list by rating range.
**REQ-F-047** The system shall allow the user to specify a lower rating bound only, an upper rating bound only, or both bounds simultaneously when applying a rating filter.
**REQ-F-048** When a rating filter is active, the system shall exclude all unrated MediaItems from the results.
**REQ-F-049** The system shall allow the user to filter the MediaItem list by Topic, restricting results to MediaItems associated with the selected Topic.
**REQ-F-050** When two or more filters are active simultaneously, the system shall return only MediaItems that satisfy all active filters (AND logic).

*Traceability: HD-029, HD-030, HD-035, HD-036, HD-056, HD-059.*

---

### 5.7 Sorting

**REQ-F-051** The system shall allow the user to sort the MediaItem list by name in ascending alphabetical order.
**REQ-F-052** The system shall allow the user to sort the MediaItem list by name in descending alphabetical order.
**REQ-F-053** The system shall allow the user to sort the MediaItem list by rating in ascending order.
**REQ-F-054** The system shall allow the user to sort the MediaItem list by rating in descending order.
**REQ-F-055** When sorting by rating in either direction, the system shall place all unrated MediaItems after all rated MediaItems.
**REQ-F-056** When two or more MediaItems have equal values for the active sort field, their relative order is unspecified.

*Traceability: HD-031, HD-060, HD-061.*

---

### 5.8 Combined Search, Filter, and Sort

**REQ-F-057** The system shall allow the user to apply a search query, one or more filters, and a sort order simultaneously in any combination.
**REQ-F-058** When search, filters, and sorting are combined, the system shall first restrict results by active search and filters, then order the restricted results according to the active sort.

*Traceability: HD-033.*

---

### 5.9 Persistence

**REQ-F-059** The system shall automatically save every successful data change without requiring an explicit user Save action.
**REQ-F-060** If an automatic save fails, the system shall notify the user.
**REQ-F-061** After a save failure, the unsaved change shall remain available to the user for the duration of the current session.

*Traceability: HD-042, HD-062, HD-063, HD-064, HD-065.*

---

### 5.10 Validation and Error Handling

**REQ-F-062** If a MediaItem name fails VR-001, the system shall reject the create or edit operation and inform the user that the name must not be empty or whitespace-only.
**REQ-F-063** If a Topic name fails VR-003 or VR-005, the system shall reject the create or rename operation and inform the user of the violation.
**REQ-F-064** If a MediaItem rating value fails VR-007, the system shall reject the create or edit operation and inform the user that the rating must be between 1 and 10.
**REQ-F-065** If a rating filter range fails VR-010, the system shall reject the filter and inform the user that the lower bound must not exceed the upper bound.
**REQ-F-066** When a save operation fails (REQ-F-060), the system shall notify the user. The specific notification mechanism is not prescribed.

*Traceability: HD-048–052, HD-057–058, HD-063.*

---

### 5.11 Business Rules

**BR-001** A MediaItem has exactly one media type, selected from the predefined set: book, movie, TV series, article, podcast, video, other.
*Traceability: HD-010, HD-011.*

**BR-002** A MediaItem has exactly one status at any point in time, selected from: planned, in progress, postponed, abandoned, completed.
*Traceability: HD-012.*

**BR-003** A MediaItem may belong to zero, one, or multiple Topics simultaneously.
*Traceability: HD-000, HD-011.*

**BR-004** A Topic may contain zero, one, or multiple MediaItems simultaneously.
*Traceability: HD-000, HD-023.*

**BR-005** Topic names are unique within the personal library. Uniqueness is evaluated case-insensitively on the normalised name.
*Traceability: HD-015, HD-050, HD-051.*

**BR-006** Duplicate MediaItem names are permitted.
*Traceability: HD-013.*

**BR-007** When both a lower and upper rating bound are specified in a rating filter, the lower bound must not exceed the upper bound.
*Traceability: HD-057.*

**BR-008** Unrated MediaItems are excluded from rating-filtered results regardless of the bound(s) specified.
*Traceability: HD-059.*

**BR-009** Deletion of a MediaItem or Topic is permanent and requires prior user confirmation.
*Traceability: HD-022, HD-040.*

**BR-010** No state-transition workflow is enforced on MediaItem status changes.
*Traceability: HD-012.*

---

### 5.12 Validation Rules

**VR-001** A MediaItem name, after removing leading and trailing whitespace, must not be empty.
*Traceability: HD-048, HD-049.*

**VR-002** Leading and trailing whitespace in a MediaItem name shall be removed before the name is saved.
*Traceability: HD-049.*

**VR-003** A Topic name, after removing leading and trailing whitespace, must not be empty.
*Traceability: HD-051.*

**VR-004** Leading and trailing whitespace in a Topic name shall be removed before the name is saved and before uniqueness is checked.
*Traceability: HD-051.*

**VR-005** A Topic name, after normalisation, must not be identical to any existing Topic name under case-insensitive comparison.
*Traceability: HD-050, HD-051.*

**VR-006** VR-005 applies on both Topic creation and Topic rename.
*Traceability: HD-015, HD-024, HD-050.*

**VR-007** A MediaItem rating, when provided, must be an integer value in the range 1 to 10 inclusive. Values outside this range shall be rejected.
*Traceability: HD-052.*

**VR-008** A MediaItem type must be one of the seven predefined values: book, movie, TV series, article, podcast, video, other.
*Traceability: HD-010.*

**VR-009** A MediaItem status must be one of the five predefined values: planned, in progress, postponed, abandoned, completed.
*Traceability: HD-012.*

**VR-010** When both rating bounds are specified in a rating filter, the lower bound must not exceed the upper bound. A range where lower bound exceeds upper bound shall be rejected.
*Traceability: HD-057, HD-058.*

**VR-011** Each rating bound, when specified, must be an integer value in the range 1 to 10 inclusive.
*Traceability: HD-035, HD-052.*

---


## 6. Non-Functional Requirements

**REQ-NF-001** — **Performance**
The system shall execute common read operations — displaying the MediaItem list, opening a MediaItem, opening a Topic, and displaying search, filter, and sort results — without perceptible delay for a personal library of typical size. No quantitative response-time threshold and no maximum library size are defined.
*Traceability: HD-041.*

**REQ-NF-002** — **Usability: Self-Evident Operation**
The system shall allow the user to perform all main operations — creating, viewing, editing, and deleting MediaItems and Topics; managing Topic associations; and performing search, filter, and sort — without consulting external documentation.
*Traceability: HD-043.*

**REQ-NF-003** — **Usability: Validation Feedback**
The system shall present an informative message to the user when an operation is rejected due to a validation rule violation, identifying the nature of the violation.
*Traceability: HD-043, REQ-F-062–065.*

**REQ-NF-004** — **Usability: Deletion Confirmation**
The system shall present a confirmation prompt to the user before executing any permanent deletion of a MediaItem or Topic.
*Traceability: HD-040, REQ-F-013, REQ-F-027.*

**REQ-NF-005** — **Data Durability: Persistence Across Sessions**
Successfully auto-saved data shall be available when the application is next launched.
*Traceability: HD-042, HD-062, REQ-F-059.*

**REQ-NF-006** — **Data Integrity: Save-Failure Isolation**
A save failure on one data change shall not corrupt or affect any previously persisted data.
*Traceability: HD-063, HD-064, REQ-F-060–061.*

**REQ-NF-007** — **Data Integrity: Referential Consistency**
The system shall maintain referential consistency of MediaItem–Topic associations after every successfully completed operation. No association shall reference a MediaItem or a Topic that does not exist in the personal library.
*Traceability: HD-000, HD-016, HD-022, REQ-F-015–016, REQ-F-028–029.*

**REQ-NF-008** — **Offline Operation**
The system shall not require any network request to perform any operation within the defined system scope.
*Traceability: HD-006, HD-066, HD-067, HD-068.*

**REQ-NF-009** — **Privacy: Local Data Boundary**
The system shall not transmit user data to any destination outside the local machine.
*Traceability: HD-046, HD-034, HD-066.*

**REQ-NF-010** — **Language**
All user-facing text produced by the system — including labels, prompts, messages, error notifications, and confirmation dialogues — shall be in English.
*Traceability: HD-045.*

**REQ-NF-011** — **Platform Independence of Specification**
The target operating system and technology stack are not established for the current version. This specification shall not be interpreted as requiring or excluding any specific platform, operating system, programming language, framework, database, or file format.
*Traceability: HD-009, HD-047.*

### Explicit Non-Requirements

The following are confirmed non-requirements for the current version:

| Concern | Basis |
|---|---|
| Quantitative response-time threshold | Q-NFR-02 |
| Maximum library size or capacity ceiling | Q-NFR-03 |
| Quantitative reliability metrics (MTBF, uptime %) | Q-NFR-04 |
| Accessibility features | HD-044 |
| Authentication, passwords, encryption at rest | HD-046 |
| Connection UI or online mode | HD-068 |
| Multilingual support | HD-045 |
| Code-quality or maintainability metrics | Not established |

---

## 7. Interface Requirements

### 7.1 General

**IR-001** The system shall present all user-facing text, labels, messages, prompts, and notifications in English.
*Traceability: HD-045, REQ-NF-010.*

**IR-002** The system shall not present any element related to authentication, login, user accounts, passwords, or profiles.
*Traceability: HD-007, HD-046.*

**IR-003** The system shall not present any element related to network connectivity, connection status, online mode, or Internet access.
*Traceability: HD-068, REQ-NF-008.*

### 7.2 MediaItem Operations

**IR-004** The system shall provide a means for the user to initiate the creation of a new MediaItem.
*Traceability: REQ-F-001.*

**IR-005** When creating a MediaItem, the system shall present input areas for: name, type, status, notes, and rating. The system shall also allow the user to assign Topics during creation.
*Traceability: REQ-F-002–007.*

**IR-006** When creating a MediaItem, the system shall present the status field with *planned* pre-selected as the default value.
*Traceability: HD-037, REQ-F-004.*

**IR-007** The system shall provide a means for the user to view an existing MediaItem showing all of its fields: name, type, status, notes, rating, and associated Topics.
*Traceability: REQ-F-009.*

**IR-008** The system shall provide a means for the user to initiate editing of an existing MediaItem, with all editable fields — name, type, status, notes, and rating — accessible for modification.
*Traceability: REQ-F-010.*

**IR-009** The system shall provide a means for the user to initiate deletion of an existing MediaItem.
*Traceability: REQ-F-012.*

**IR-010** Before executing a MediaItem deletion, the system shall present a confirmation prompt that allows the user to confirm or cancel the deletion.
*Traceability: REQ-F-013, REQ-NF-004, HD-040.*

### 7.3 Topic Operations

**IR-011** The system shall provide a means for the user to initiate the creation of a new Topic by entering a name.
*Traceability: REQ-F-020.*

**IR-012** The system shall provide a means for the user to view an existing Topic, displaying its name and the MediaItems currently associated with it.
*Traceability: REQ-F-022.*

**IR-013** The system shall provide a means for the user to initiate renaming of an existing Topic.
*Traceability: REQ-F-023.*

**IR-014** The system shall provide a means for the user to initiate deletion of an existing Topic.
*Traceability: REQ-F-026.*

**IR-015** Before executing a Topic deletion, the system shall present a confirmation prompt that allows the user to confirm or cancel the deletion.
*Traceability: REQ-F-027, REQ-NF-004, HD-040.*

### 7.4 MediaItem–Topic Association

**IR-016** When viewing or editing a MediaItem, the system shall provide a means for the user to add the MediaItem to one or more Topics and to remove the MediaItem from one or more Topics.
*Traceability: REQ-F-030–031, HD-038.*

**IR-017** When viewing a Topic, the system shall provide a means for the user to add a MediaItem to that Topic and to remove a MediaItem from that Topic.
*Traceability: REQ-F-032–033, HD-038.*

### 7.5 Navigation

**IR-018** When viewing a Topic, the system shall provide a means for the user to open any MediaItem listed as associated with that Topic.
*Traceability: REQ-F-035, HD-039.*

**IR-019** When viewing a MediaItem, the system shall display all Topics to which that MediaItem belongs and provide a means for the user to open any of those Topics.
*Traceability: REQ-F-036–037, HD-039.*

### 7.6 Search

**IR-020** The system shall provide a means for the user to enter a search query against the personal library.
*Traceability: REQ-F-038.*

**IR-021** When the search query is non-empty, the system shall present matching MediaItems as results accessible to the user.
*Traceability: REQ-F-039.*

**IR-022** When the search query is non-empty, the system shall present matching Topics as distinct results accessible to the user.
*Traceability: REQ-F-040, HD-055.*

**IR-023** When a Topic is presented as a search result, the system shall provide a means for the user to open that Topic and view its associated MediaItems.
*Traceability: REQ-F-041, HD-055.*

**IR-024** The system shall, when a search query matches both MediaItems and Topics, present both MediaItem results and Topic results within the same search results list, with each result clearly identifiable as either a MediaItem or a Topic.
*Traceability: REQ-F-039–040, HD-055, Q-IR-01.*

**IR-025** When the search query is empty, the system shall not restrict the displayed results based on search. Any active filters and sort order shall still apply.
*Traceability: REQ-F-042, HD-053.*

### 7.7 Filtering

**IR-026** The system shall provide a means for the user to apply a filter by media type, restricting displayed MediaItems to those of the selected type.
*Traceability: REQ-F-044, HD-029.*

**IR-027** The system shall provide a means for the user to apply a filter by status, restricting displayed MediaItems to those with the selected status value.
*Traceability: REQ-F-045, HD-029.*

**IR-028** The system shall provide a means for the user to specify a rating filter by entering a lower bound, an upper bound, or both.
*Traceability: REQ-F-046–047, HD-035, HD-056.*

**IR-029** The system shall provide a means for the user to apply a filter by Topic, restricting displayed MediaItems to those associated with the selected Topic.
*Traceability: REQ-F-049, HD-029.*

**IR-030** When multiple filters are active simultaneously, the system shall present only MediaItems satisfying all active filters, reflecting AND logic to the user without requiring any additional action.
*Traceability: REQ-F-050, HD-030.*

### 7.8 Sorting

**IR-031** The system shall provide a means for the user to select sorting of the MediaItem list by name, with the choice of ascending or descending direction.
*Traceability: REQ-F-051–052, HD-031.*

**IR-032** The system shall provide a means for the user to select sorting of the MediaItem list by rating, with the choice of ascending or descending direction.
*Traceability: REQ-F-053–054, HD-031.*

**IR-033** When the MediaItem list is sorted by rating, the system shall display unrated MediaItems after all rated MediaItems regardless of the selected sort direction, visibly placing them at the end of the list.
*Traceability: REQ-F-055, HD-060.*

### 7.9 Combined Operations

**IR-034** The system shall allow the user to have a search query, one or more filters, and a sort order active simultaneously, with the displayed results reflecting all active constraints at once.
*Traceability: REQ-F-057–058, HD-033.*

### 7.10 Validation Feedback

**IR-035** When a MediaItem create or edit operation is rejected because the name is empty or whitespace-only after normalisation, the system shall present a message identifying the name field as the source of the violation.
*Traceability: REQ-F-062, VR-001–002, REQ-NF-003.*

**IR-036** When a MediaItem create or edit operation is rejected because the rating value is outside 1–10, the system shall present a message stating that the rating must be a value between 1 and 10.
*Traceability: REQ-F-064, VR-007, REQ-NF-003.*

**IR-037** When a Topic create or rename operation is rejected because the resulting normalised name is empty, the system shall present a message identifying the name field as the source of the violation.
*Traceability: REQ-F-063, VR-003–004, REQ-NF-003.*

**IR-038** When a Topic create or rename operation is rejected because the normalised name already exists (case-insensitively), the system shall present a message informing the user that the name is already in use.
*Traceability: REQ-F-063, VR-005–006, REQ-NF-003.*

**IR-039** When a rating filter is rejected because the lower bound exceeds the upper bound, the system shall present a message informing the user that the lower bound must not exceed the upper bound.
*Traceability: REQ-F-065, VR-010, REQ-NF-003.*

### 7.11 Auto-Save and Save-Failure Feedback

**IR-040** The system shall not require the user to perform any explicit save action after creating, editing, deleting, renaming, or modifying a Topic association.
*Traceability: REQ-F-059, REQ-NF-005, HD-042.*

**IR-041** When an auto-save operation fails, the system shall present a notification informing the user that the save operation did not succeed.
*Traceability: REQ-F-060, REQ-F-066, HD-063, REQ-NF-006.*

**IR-042** After a save failure notification, the unsaved change shall remain accessible and visible to the user for the duration of the current session.
*Traceability: REQ-F-061, HD-064.*

### 7.12 Persistence Across Restarts

**IR-043** When the application is launched, the system shall present the user's personal library — all previously saved MediaItems, Topics, and associations — as it existed at the end of the prior session.
*Traceability: REQ-NF-005, HD-042, HD-062.*

### Explicit Interface Non-Requirements

| Concern | Basis |
|---|---|
| Authentication UI (login, password, profile) | HD-007, HD-046 |
| Connection status, online mode, network indicators | HD-068, REQ-NF-008 |
| Accessibility controls | HD-044 |
| Platform-specific UI controls, widgets, or layouts | HD-009, HD-047, REQ-NF-011 |
| Quantitative response-time indicators or progress bars | Q-NFR-02, REQ-NF-001 |
| Import/export UI | HD-034 |
| Backup/restore UI | HD-034 |
| Statistics or analytics views | HD-034 |
| Undo/redo/recycle bin UI | HD-022 |
| Explicit Save button or Save action | HD-042 |
| Multilingual or locale-switching UI | HD-045 |

---

## 8. Constraints

**CON-001** — **Fixed Media Type Set**
The set of supported media types is fixed for the current version: book, movie, TV series, article, podcast, video, other. No mechanism for user-defined or runtime-defined media types shall be included. Extension is by future development only.
*Traceability: HD-010, BR-001, REQ-F-003, VR-008.*

**CON-002** — **Fixed Status Value Set**
The set of supported MediaItem status values is fixed: planned, in progress, postponed, abandoned, completed. No user-defined or runtime-defined status values are permitted.
*Traceability: HD-012, HD-021, BR-002, VR-009.*

**CON-003** — **Rating Domain**
A MediaItem rating, when present, must be an integer value in the inclusive range 1 to 10. Values outside this range are invalid. Absence of rating is a valid and distinct state.
*Traceability: HD-052, VR-007, VR-011, REQ-F-064.*

**CON-004** — **Uniform MediaItem Field Structure**
All media types share the same field set: id, name, type, status, notes, rating, and Topic associations. No type-specific fields may be introduced in the current version.
*Traceability: HD-014, HD-011.*

**CON-005** — **No Date-Added Field**
No date-added, creation-timestamp, or equivalent temporal metadata field may be included in the MediaItem model.
*Traceability: HD-032.*

**CON-006** — **Single Notes Field Per MediaItem**
Each MediaItem has at most one notes field. No multiple-notes, notes-log, or timestamped-note structure may be included. Notes do not constitute a separate subsystem.
*Traceability: HD-011, HD-019.*

**CON-007** — **Topic Name Uniqueness Rule**
Topic names must be unique within the personal library. Uniqueness is evaluated case-insensitively after removing leading and trailing whitespace. This constraint applies at creation and at rename.
*Traceability: HD-015, HD-050, HD-051, BR-005, VR-005–006.*

**CON-008** — **Single Local User — No Multi-User Architecture**
The system is designed for exactly one local user. No component, data structure, or mechanism intended to support concurrent users, accounts, roles, or permissions may be included.
*Traceability: HD-002, HD-003, HD-005, HD-007, HD-008.*

**CON-009** — **No Network Component**
The system shall not include any component that initiates, receives, or depends upon network communication. No remote endpoint, network protocol, HTTP client, or external API integration may be present.
*Traceability: HD-006, HD-066, HD-067, HD-068, REQ-NF-008.*

**CON-010** — **Local Data Boundary**
All user data must be stored and remain on the local machine. No mechanism for transmitting, replicating, synchronising, or backing up user data to any external destination may be included.
*Traceability: HD-046, HD-034, REQ-NF-009.*

**CON-011** — **English User-Facing Text**
All text strings presented to the user — including labels, prompts, messages, error notifications, and confirmations — must be in English. No internationalisation layer or non-English string set may be present.
*Traceability: HD-045, REQ-NF-010, IR-001.*

**CON-012** — **Platform and Technology Stack Independence**
The target OS, programming language, framework, database engine, file format, UI toolkit, and deployment mechanism are not established. No specification artifact may be interpreted as requiring or excluding any specific technology choice.
*Traceability: HD-009, HD-047, REQ-NF-011.*

**CON-013** — **Excluded Features — Scope Ceiling**
The following capabilities must not be introduced: external metadata retrieval; data import or export; built-in backup or restore; statistics or analytics views; cloud synchronisation; recommendations; notifications other than save-failure notification; undo, redo, or recycle bin for deleted entities; authentication, encryption-at-rest, or application-level access control.
*Traceability: HD-022, HD-027, HD-034, HD-044, HD-046.*

---


## 9. Acceptance Criteria

Each criterion defines an observable, independently verifiable Pass/Fail condition. Traceability is provided for every criterion.

### 9.1 MediaItem Management

**AC-001** When the user submits a create-MediaItem operation with a valid name and a selected type, a new MediaItem appears in the personal library with the submitted name and type.
*Traceability: REQ-F-001–003, HD-011, HD-037.*

**AC-002** When a MediaItem is created without the user explicitly selecting a status, the created MediaItem has status *planned*.
*Traceability: REQ-F-004, HD-037.*

**AC-003** A MediaItem can be successfully created when the notes field is empty and the rating field is unset.
*Traceability: REQ-F-005–006, HD-011.*

**AC-004** When the user assigns one or more Topics to a MediaItem during creation, the created MediaItem is associated with those Topics.
*Traceability: REQ-F-007, HD-037, HD-038.*

**AC-005** A MediaItem created successfully is present in the personal library when the application is next launched, without requiring any explicit save action from the user.
*Traceability: REQ-F-008, REQ-NF-005, HD-042.*

**AC-006** When the user opens a MediaItem, all fields are visible: name, type, status, notes, rating, and associated Topics (including when optional fields are empty or the Topic list is empty).
*Traceability: REQ-F-009, HD-011.*

**AC-007** When the user edits and saves any field of a MediaItem, the updated value is reflected when the item is next viewed, without requiring an explicit save action.
*Traceability: REQ-F-010–011, HD-017, HD-042.*

**AC-008** When the user initiates MediaItem deletion and confirms the confirmation prompt, the MediaItem is permanently removed from the personal library.
*Traceability: REQ-F-012–014, HD-022, HD-040.*

**AC-009** When the user initiates MediaItem deletion and cancels at the confirmation prompt, the MediaItem is not deleted and remains unchanged in the personal library.
*Traceability: REQ-F-013, HD-040, REQ-NF-004.*

**AC-010** When a MediaItem is deleted, all its Topic associations are removed, and all associated Topics still exist with their other associations unchanged.
*Traceability: REQ-F-015–016, HD-022.*

**AC-011** After a MediaItem has been deleted, no restore, undo, or recycle-bin operation is available to return the item.
*Traceability: REQ-F-017, HD-022, CON-013.*

**AC-012** The user can change a MediaItem's status to any of the five values from any other status value, with no sequence restriction.
*Traceability: REQ-F-018–019, HD-012, BR-010.*

### 9.2 Topic Management

**AC-013** When the user creates a Topic with a valid unique name, the Topic appears in the personal library and is available after relaunch without an explicit save action.
*Traceability: REQ-F-020–021, HD-015, HD-042.*

**AC-014** When the user views a Topic, the Topic's name and all currently associated MediaItems are displayed. When no MediaItems are associated, the Topic is displayed with an empty association list.
*Traceability: REQ-F-022, HD-023.*

**AC-015** When a Topic is renamed to a valid unique name, the Topic's name is updated, all previously associated MediaItems remain associated with the renamed Topic, and the change persists without an explicit save action and survives application relaunch.
*Traceability: REQ-F-023–025, HD-024, HD-050, REQ-NF-005.*

**AC-016** When a Topic is deleted after user confirmation, the Topic is removed from the library, all its MediaItem associations are removed, and all previously associated MediaItems still exist with their other fields unchanged.
*Traceability: REQ-F-026–029, HD-016, HD-040.*

**AC-017** When the user initiates Topic deletion and cancels at the confirmation prompt, the Topic is not deleted and all its associations remain intact.
*Traceability: REQ-F-027, HD-040, REQ-NF-004.*

### 9.3 Association and Navigation

**AC-018** From a MediaItem's view or edit state, the user can add the MediaItem to a Topic and the association is immediately reflected. The user can also remove the MediaItem from a Topic and the removal is immediately reflected.
*Traceability: REQ-F-030–031, HD-038.*

**AC-019** From a Topic's view, the user can add a MediaItem not already associated, and the association is immediately reflected. The user can also remove an associated MediaItem, and the removal is immediately reflected.
*Traceability: REQ-F-032–033, HD-038.*

**AC-020** An association change made from either side (MediaItem or Topic) is persisted without an explicit save action and survives application relaunch.
*Traceability: REQ-F-034, HD-042, REQ-NF-005.*

**AC-021** When viewing a Topic that has at least one associated MediaItem, the user can open any of those MediaItems and view its full details.
*Traceability: REQ-F-035, HD-039.*

**AC-022** When viewing a MediaItem that belongs to at least one Topic, all associated Topics are displayed, and the user can open any of them and view its details.
*Traceability: REQ-F-036–037, HD-039.*

### 9.4 Search

**AC-023** When a non-empty search query is entered, MediaItems whose names contain the query string (regardless of letter case) are returned as results; MediaItems not matching are excluded.
*Traceability: REQ-F-038–039, HD-026, HD-054.*

**AC-024** When a non-empty search query is entered, Topics whose names contain the query string (regardless of letter case) are returned as Topic results; each Topic result is identifiable as a Topic.
*Traceability: REQ-F-040, HD-055, IR-022.*

**AC-025** When a Topic appears as a search result, the user can open it and view its associated MediaItems.
*Traceability: REQ-F-041, HD-055, IR-023.*

**AC-026** When a search query matches both MediaItems and Topics, both MediaItem results and Topic results are presented in the same results list, and each result is visibly identified as either a MediaItem or a Topic.
*Traceability: IR-024, REQ-F-039–040, HD-055, Q-IR-01.*

**AC-027** When the search query is empty, no items are excluded from the results on the basis of search. All items satisfying active filters and sort order are displayed.
*Traceability: REQ-F-042, HD-053.*

**AC-028** Notes content is never returned as a search result, even when the search query matches text present in a MediaItem's notes field.
*Traceability: REQ-F-043, HD-025.*

### 9.5 Filtering

**AC-029** When a type filter is active, only MediaItems of the selected type are displayed; all others are excluded.
*Traceability: REQ-F-044, HD-029.*

**AC-030** When a status filter is active, only MediaItems with the selected status are displayed.
*Traceability: REQ-F-045, HD-029.*

**AC-031** When a rating filter with a lower bound only is applied (e.g., ≥ 7), only rated MediaItems with rating ≥ lower bound are returned; unrated items are excluded.
*Traceability: REQ-F-046–047, HD-056, HD-059.*

**AC-032** When a rating filter with an upper bound only is applied (e.g., ≤ 5), only rated MediaItems with rating ≤ upper bound are returned; unrated items are excluded.
*Traceability: REQ-F-046–047, HD-056, HD-059.*

**AC-033** When a rating filter with both bounds is applied (e.g., 4–7), only rated MediaItems with rating within the inclusive range are returned; unrated items are excluded.
*Traceability: REQ-F-046–047, HD-035, HD-056, HD-059.*

**AC-034** When any rating filter (lower bound only, upper bound only, or both bounds) is active, MediaItems with no rating set are absent from the filtered results.
*Traceability: REQ-F-048, HD-036, HD-059.*

**AC-035** When a Topic filter is active, only MediaItems associated with the selected Topic are displayed. If the selected Topic has no associated MediaItems, the result list is empty.
*Traceability: REQ-F-049, HD-029.*

**AC-036** When two or more filters are active simultaneously, only MediaItems satisfying all active filters are displayed (AND logic); a MediaItem satisfying only some is excluded. When no item satisfies all active filters, the result list is empty.
*Traceability: REQ-F-050, HD-030.*

### 9.6 Sorting

**AC-037** When sorting by name ascending, MediaItems are ordered alphabetically A to Z.
*Traceability: REQ-F-051, HD-031.*

**AC-038** When sorting by name descending, MediaItems are ordered alphabetically Z to A.
*Traceability: REQ-F-052, HD-031.*

**AC-039** When sorting by rating ascending, rated MediaItems are ordered from lowest to highest rating; all unrated MediaItems appear after all rated MediaItems.
*Traceability: REQ-F-053, REQ-F-055, HD-060.*

**AC-040** When sorting by rating descending, rated MediaItems are ordered from highest to lowest rating; all unrated MediaItems appear after all rated MediaItems.
*Traceability: REQ-F-054–055, HD-060.*

### 9.7 Combined Operations

**AC-041** When a search query, a filter, and a sort order are all active simultaneously, the results contain only MediaItems matching the search query and all active filters, ordered by the active sort.
*Traceability: REQ-F-057–058, HD-033.*

### 9.8 Validation

**AC-042** When the user attempts to create or edit a MediaItem with a name that is empty or contains only whitespace, the operation is rejected and a message identifies the name field as the source of the violation.
*Traceability: REQ-F-062, VR-001–002, HD-048, REQ-NF-003.*

**AC-043** When the user enters a MediaItem name with leading or trailing whitespace, the stored name has that whitespace removed.
*Traceability: VR-002, HD-049.*

**AC-044** When the user attempts to save a MediaItem rating with a value outside 1–10, the operation is rejected and a message states the rating must be between 1 and 10.
*Traceability: REQ-F-064, VR-007, HD-052, REQ-NF-003.*

**AC-045** When the user attempts to create or rename a Topic with a name that is empty or whitespace-only, the operation is rejected and a message identifies the name field as the source of the violation.
*Traceability: REQ-F-063, VR-003–004, REQ-NF-003.*

**AC-046** When the user attempts to create or rename a Topic with a name that, after trimming, is identical (case-insensitively) to an existing Topic name, the operation is rejected and a message informs the user the name is already in use.
*Traceability: REQ-F-063, VR-005–006, HD-050–051, REQ-NF-003.*

**AC-047** When the user enters a Topic name with leading or trailing whitespace, the stored name has that whitespace removed.
*Traceability: VR-004, HD-051.*

**AC-048** When the user specifies a rating filter with a lower bound that exceeds the upper bound, the filter is rejected and a message informs the user that the lower bound must not exceed the upper bound.
*Traceability: REQ-F-065, VR-010, HD-057–058, REQ-NF-003.*

### 9.9 Persistence and Save Failure

**AC-049** After any successful create, edit, delete, rename, or association change, closing and relaunching the application shows the personal library reflecting that change, without any explicit save action.
*Traceability: REQ-F-059, REQ-NF-005, HD-042.*

**AC-050** When an auto-save operation fails, the user is notified of the failure. Previously persisted data is not affected by the failure.
*Traceability: REQ-F-060, REQ-F-066, HD-063, REQ-NF-006.*

**AC-051** After a save failure, the change that was not persisted remains visible and accessible to the user in the current session.
*Traceability: REQ-F-061, HD-064.*

### 9.10 Non-Functional

**AC-052** Common read operations complete without a perceptible delay under typical personal library conditions. This criterion requires evaluator judgment; no quantitative threshold applies.
*Traceability: REQ-NF-001, HD-041.*

**AC-053** A user with no prior knowledge of the system is able to successfully complete each main operation using only the information presented by the system.
*Traceability: REQ-NF-002, HD-043.*

**AC-054** After any deletion of a MediaItem or Topic, no association exists in the system that references the deleted entity.
*Traceability: REQ-NF-007, HD-000, HD-016, HD-022.*

**AC-055** All in-scope operations complete successfully with no network connection active.
*Traceability: REQ-NF-008, HD-066–068.*

**AC-056** During any operation, no network traffic originating from the application is transmitted to any destination outside the local machine.
*Traceability: REQ-NF-009, HD-046.*

**AC-057** All user-facing text presented by the system is in English. No non-English text is present in any user-facing element.
*Traceability: REQ-NF-010, HD-045, IR-001.*

### 9.11 Interface

**AC-058** No element related to authentication, login, user accounts, passwords, or profiles appears anywhere in the application.
*Traceability: IR-002, HD-007, HD-046.*

**AC-059** No element related to network connectivity, connection status, online mode, or Internet access appears anywhere in the application.
*Traceability: IR-003, HD-068, REQ-NF-008.*

**AC-060** When the MediaItem creation form is first presented, the status field shows *planned* as the pre-selected default, without any user action.
*Traceability: IR-006, HD-037, REQ-F-004.*

**AC-061** No explicit Save button, Save action, or Save prompt is required or presented to the user as a mandatory step when creating, editing, deleting, renaming, or modifying associations.
*Traceability: IR-040, REQ-F-059, HD-042.*

**AC-062** When a save failure occurs, a notification is presented to the user, and the change that was not persisted remains visible in the current session without requiring the user to re-enter it.
*Traceability: IR-041–042, REQ-F-060–061, HD-063–064.*

**AC-063** When the application is launched, the personal library presented to the user reflects all data that was successfully saved in previous sessions.
*Traceability: IR-043, REQ-NF-005, HD-042.*

### 9.12 Constraints

**AC-064** The type field of every MediaItem contains exactly one of the seven predefined values. No other value can be stored or accepted.
*Traceability: CON-001, VR-008, HD-010.*

**AC-065** The status field of every MediaItem contains exactly one of the five predefined values. No other value can be stored or accepted.
*Traceability: CON-002, VR-009, HD-012.*

**AC-066** No MediaItem has any field beyond the approved set: id, name, type, status, notes, rating, and Topic associations. No type-specific field exists.
*Traceability: CON-004, HD-014.*

**AC-067** No date-added, creation-timestamp, or equivalent temporal metadata field exists on any MediaItem or is presented in the user interface.
*Traceability: CON-005, HD-032.*

**AC-068** The application makes no outbound network calls during any operation.
*Traceability: CON-009, REQ-NF-008, HD-066–068.*

**AC-069** None of the following capabilities exist in the application: external metadata retrieval, data import, data export, built-in backup, built-in restore, statistics view, analytics view, recommendations, notifications other than save-failure notification, undo, redo, recycle bin, or application-level authentication or access control.
*Traceability: CON-013, HD-022, HD-027, HD-034, HD-046.*

---


## 10. BDD Scenarios

All scenarios use the Given–When–Then structure. BDD-017 was split into BDD-017a and BDD-017b during the independent review. Total: 70 scenarios.

---

**Scenario: BDD-001 — Create a MediaItem with required fields only**
Given the personal library is open
When the user creates a new MediaItem with name "Dune" and type "book"
Then a MediaItem named "Dune" of type "book" appears in the personal library
And its status is "planned", notes field is empty, rating is unset, and it has no Topic associations
*Traceability: REQ-F-001–007 | AC-001–003*

---

**Scenario: BDD-002 — Create a MediaItem with all optional fields provided**
Given the personal library is open and a Topic named "Science Fiction" exists
When the user creates a new MediaItem with name "Arrival", type "movie", status "completed", notes "Excellent film", rating 9, and assigns Topic "Science Fiction"
Then a MediaItem named "Arrival" appears with all submitted fields and is associated with Topic "Science Fiction"
*Traceability: REQ-F-001–007 | AC-001, AC-003, AC-004*

---

**Scenario: BDD-003 — Create a MediaItem and confirm it persists after relaunch**
Given a MediaItem named "Foundation" of type "book" has been created
When the application is closed and relaunched
Then the MediaItem "Foundation" is present in the personal library with all its fields unchanged
*Traceability: REQ-F-008, REQ-NF-005 | AC-005*

---

**Scenario: BDD-004 — Reject creation with empty name**
Given the personal library is open
When the user attempts to create a MediaItem with an empty name and type "article"
Then the creation is rejected
And an informative message identifies the name field as the source of the violation
*Traceability: REQ-F-062, VR-001 | AC-042*

---

**Scenario: BDD-005 — Reject creation with whitespace-only name**
Given the personal library is open
When the user attempts to create a MediaItem with name "   " (whitespace only) and type "podcast"
Then the creation is rejected
And an informative message identifies the name field as the source of the violation
*Traceability: REQ-F-062, VR-001 | AC-042*

---

**Scenario: BDD-006 — MediaItem name is trimmed before saving**
Given the personal library is open
When the user creates a MediaItem with name "  Cosmos  " and type "video"
Then the MediaItem is created successfully
And the stored name is "Cosmos" without leading or trailing whitespace
*Traceability: VR-002 | AC-043*

---

**Scenario: BDD-007 — Reject MediaItem rating above valid range**
Given the personal library is open
When the user attempts to create a MediaItem with name "Neuromancer", type "book", and rating 11
Then the creation is rejected
And a message states that the rating must be between 1 and 10
*Traceability: REQ-F-064, VR-007 | AC-044*

---

**Scenario: BDD-008 — Reject MediaItem rating of zero**
Given the personal library is open
When the user attempts to create a MediaItem with name "Ghost in the Shell", type "movie", and rating 0
Then the creation is rejected
And a message states that the rating must be between 1 and 10
*Traceability: REQ-F-064, VR-007 | AC-044*

---

**Scenario: BDD-009 — View a fully populated MediaItem**
Given a MediaItem named "The Martian" exists with type "movie", status "completed", notes "Great survival story", rating 8, and associated Topic "Science Fiction"
When the user opens the MediaItem "The Martian"
Then all of the following fields are visible to the user without requiring any additional navigation or expansion action: name "The Martian", type "movie", status "completed", notes "Great survival story", rating 8, and associated Topic "Science Fiction"
*Traceability: REQ-F-009, IR-007 | AC-006*

---

**Scenario: BDD-010 — View a MediaItem with optional fields unset**
Given a MediaItem named "Brief History of Time" exists with type "book", status "planned", no notes, no rating, and no Topic associations
When the user opens the MediaItem "Brief History of Time"
Then the name, type, and status are displayed correctly
And the notes field is shown as empty
And the rating is shown as unset
And the Topic association list is shown as empty
*Traceability: REQ-F-009 | AC-006*

---

**Scenario: BDD-011 — Edit a MediaItem field and confirm persistence**
Given a MediaItem named "Sapiens" exists with status "planned"
When the user edits the MediaItem and changes its status to "completed"
And the application is closed and relaunched
Then the MediaItem "Sapiens" shows status "completed"
*Traceability: REQ-F-010–011, REQ-NF-005 | AC-007, AC-049*

---

**Scenario: BDD-012 — Edit requires no explicit save action**
Given a MediaItem named "Interstellar" exists with rating unset
When the user edits the MediaItem and sets rating to 7
Then the rating 7 is reflected immediately without the user performing any explicit save action
*Traceability: REQ-F-011, REQ-F-059 | AC-007, AC-061*

---

**Scenario: BDD-013 — Delete a MediaItem after confirmation**
Given a MediaItem named "Arrival" exists in the personal library
When the user initiates deletion of "Arrival" and confirms the deletion prompt
Then "Arrival" is no longer present in the personal library
*Traceability: REQ-F-012–014 | AC-008*

---

**Scenario: BDD-014 — Cancel MediaItem deletion**
Given a MediaItem named "Contact" exists in the personal library
When the user initiates deletion of "Contact" and cancels at the confirmation prompt
Then "Contact" still exists in the personal library with all fields unchanged
*Traceability: REQ-F-013 | AC-009*

---

**Scenario: BDD-015 — Delete a MediaItem removes its Topic associations but not the Topics**
Given a MediaItem named "Gravity" is associated with Topics "Space" and "Movies"
When the user initiates deletion of "Gravity" and confirms the deletion prompt
Then "Gravity" is no longer in the personal library
And Topic "Space" still exists and Topic "Movies" still exists
And neither Topic lists "Gravity" as an associated MediaItem
*Traceability: REQ-F-014–016 | AC-010*

---

**Scenario: BDD-016 — Deleted MediaItem cannot be restored**
Given a MediaItem named "Inception" has been deleted
When the user inspects all available actions in the personal library
Then no restore, undo, or recycle-bin action for "Inception" is available
*Traceability: REQ-F-017 | AC-011*

---

**Scenario: BDD-017a — Change MediaItem status from planned to abandoned**
Given a MediaItem named "Ender's Game" has status "planned"
When the user changes its status to "abandoned"
Then the status of "Ender's Game" is "abandoned"
*Traceability: REQ-F-018–019 | AC-012*

---

**Scenario: BDD-017b — Change MediaItem status from abandoned to completed**
Given a MediaItem named "Ender's Game" has status "abandoned"
When the user changes its status to "completed"
Then the status of "Ender's Game" is "completed"
*Traceability: REQ-F-018–019 | AC-012*

---

**Scenario: BDD-018 — Create a Topic and confirm it persists**
Given the personal library is open
When the user creates a Topic named "Philosophy"
Then the Topic "Philosophy" appears in the personal library
When the application is closed and relaunched
Then the Topic "Philosophy" is still present
*Traceability: REQ-F-020–021 | AC-013*

---

**Scenario: BDD-019 — Reject Topic with empty name**
Given the personal library is open
When the user attempts to create a Topic with an empty name
Then the creation is rejected and an informative message identifies the name field as the source of the violation
*Traceability: REQ-F-063, VR-003 | AC-045*

---

**Scenario: BDD-020 — Reject duplicate Topic name (case-insensitive)**
Given a Topic named "Science" exists in the personal library
When the user attempts to create a Topic named "science"
Then the creation is rejected and a message informs the user that the name is already in use
*Traceability: REQ-F-063, VR-005 | AC-046*

---

**Scenario: BDD-021 — Reject duplicate Topic name with surrounding whitespace**
Given a Topic named "Science" exists in the personal library
When the user attempts to create a Topic named "  Science  "
Then the creation is rejected and a message informs the user that the name is already in use
*Traceability: REQ-F-063, VR-005–006 | AC-046*

---

**Scenario: BDD-022 — Topic name is trimmed before saving**
Given the personal library is open
When the user creates a Topic named "  History  "
Then the Topic is created successfully and the stored name is "History" without leading or trailing whitespace
*Traceability: VR-004 | AC-047*

---

**Scenario: BDD-023 — View a Topic with associated MediaItems**
Given a Topic named "Space" exists and is associated with MediaItems "The Martian" and "Interstellar"
When the user opens the Topic "Space"
Then the Topic name "Space" is displayed and both "The Martian" and "Interstellar" are listed
*Traceability: REQ-F-022 | AC-014*

---

**Scenario: BDD-024 — View an empty Topic**
Given a Topic named "Unassigned" exists with no associated MediaItems
When the user opens the Topic "Unassigned"
Then the Topic name "Unassigned" is displayed and the associated MediaItems list is empty
*Traceability: REQ-F-022 | AC-014*

---

**Scenario: BDD-025 — Rename a Topic, confirm associations preserved, and confirm persistence after relaunch**
Given a Topic named "Sci-Fi" is associated with MediaItems "Dune" and "Arrival"
When the user renames the Topic to "Science Fiction"
Then the Topic is now named "Science Fiction" and "Dune" and "Arrival" are still listed under "Science Fiction"
When the application is closed and relaunched
Then the Topic is still named "Science Fiction" and "Dune" and "Arrival" are still associated with it
*Traceability: REQ-F-023–025, REQ-NF-005 | AC-015*

---

**Scenario: BDD-026 — Reject Topic rename to existing name (case-insensitive)**
Given Topics "History" and "Science" exist
When the user attempts to rename "History" to "science"
Then the rename is rejected and a message informs the user that the name is already in use
And the Topic name remains "History"
*Traceability: REQ-F-063, VR-006 | AC-046*

---

**Scenario: BDD-027 — Delete a Topic after confirmation**
Given a Topic named "Classics" exists
When the user initiates deletion of "Classics" and confirms the deletion prompt
Then "Classics" is no longer present in the personal library
*Traceability: REQ-F-026–028 | AC-016*

---

**Scenario: BDD-028 — Cancel Topic deletion**
Given a Topic named "Fantasy" exists with associated MediaItem "The Hobbit"
When the user initiates deletion of "Fantasy" and cancels at the confirmation prompt
Then "Fantasy" still exists and "The Hobbit" is still associated with "Fantasy"
*Traceability: REQ-F-027 | AC-017*

---

**Scenario: BDD-029 — Delete a Topic does not delete its MediaItems**
Given a Topic named "Drama" is associated with MediaItems "Roma" and "Parasite"
When the user confirms deletion of "Drama"
Then "Drama" no longer exists in the personal library
And "Roma" and "Parasite" still exist in the personal library
*Traceability: REQ-F-028–029 | AC-016*

---

**Scenario: BDD-030 — Add a Topic association from the MediaItem side**
Given a MediaItem named "Cosmos" exists with no Topic associations and a Topic named "Science" exists
When the user opens "Cosmos" and adds Topic "Science" to it
Then "Cosmos" is associated with "Science" and "Science" lists "Cosmos" as an associated MediaItem
*Traceability: REQ-F-030, REQ-F-034 | AC-018, AC-020*

---

**Scenario: BDD-031 — Remove a Topic association from the MediaItem side**
Given a MediaItem named "Cosmos" is associated with Topic "Science"
When the user opens "Cosmos" and removes Topic "Science" from it
Then "Cosmos" is no longer associated with "Science" and "Science" no longer lists "Cosmos"
*Traceability: REQ-F-031 | AC-018*

---

**Scenario: BDD-032 — Add a MediaItem association from the Topic side**
Given a Topic named "History" exists and a MediaItem named "Sapiens" exists with no association to "History"
When the user opens Topic "History" and adds "Sapiens" to it
Then "Sapiens" appears in Topic "History" and "Sapiens" lists "History" among its associated Topics
*Traceability: REQ-F-032, REQ-F-034 | AC-019, AC-020*

---

**Scenario: BDD-033 — Remove a MediaItem association from the Topic side**
Given a MediaItem named "Sapiens" is associated with Topic "History"
When the user opens Topic "History" and removes "Sapiens" from it
Then "Sapiens" no longer appears in Topic "History" and "Sapiens" no longer lists "History" among its Topics
*Traceability: REQ-F-033 | AC-019*

---

**Scenario: BDD-034 — Association change persists across relaunch**
Given a MediaItem named "Origin" has been added to Topic "Science" from the MediaItem side
When the application is closed and relaunched
Then "Origin" is still listed under Topic "Science"
*Traceability: REQ-F-034, REQ-NF-005 | AC-020, AC-049*

---

**Scenario: BDD-035 — Navigate from Topic to a MediaItem**
Given a Topic named "Space" contains MediaItems "The Martian" and "Gravity"
When the user opens Topic "Space" and selects "The Martian"
Then the full details of MediaItem "The Martian" are displayed
*Traceability: REQ-F-035 | AC-021*

---

**Scenario: BDD-036 — Navigate from MediaItem to a Topic**
Given a MediaItem named "Interstellar" is associated with Topics "Space" and "Science Fiction"
When the user opens "Interstellar" and selects Topic "Space"
Then the full details of Topic "Space" are displayed including its associated MediaItems
*Traceability: REQ-F-036–037 | AC-022*

---

**Scenario: BDD-037 — Search returns MediaItems matching by substring (case-insensitive)**
Given MediaItems "Space Odyssey", "space travel", and "Ocean Deep" exist
When the user enters search query "space"
Then "Space Odyssey" and "space travel" appear in the search results and "Ocean Deep" does not
*Traceability: REQ-F-038–039 | AC-023*

---

**Scenario: BDD-038 — Search returns matching Topics as Topic results**
Given Topics "Science Fiction" and "History" exist
When the user enters search query "sci"
Then "Science Fiction" appears in the search results identified as a Topic and "History" does not appear
*Traceability: REQ-F-040 | AC-024*

---

**Scenario: BDD-039 — Search result contains both MediaItem and Topic matches in one list**
Given a MediaItem named "Science" exists and a Topic named "Science" exists
When the user enters search query "science"
Then both the MediaItem "Science" and the Topic "Science" appear in the same results list
And each result is identifiable as either a MediaItem or a Topic
*Traceability: REQ-F-039–040 | AC-026*

---

**Scenario: BDD-040 — Open a Topic from search results**
Given a Topic named "Philosophy" is associated with MediaItem "Meditations"
When the user enters search query "philo" and opens the Topic "Philosophy" from the search results
Then the Topic "Philosophy" is displayed showing "Meditations" as an associated MediaItem
*Traceability: REQ-F-041 | AC-025*

---

**Scenario: BDD-041 — Empty search query does not restrict MediaItem results**
Given MediaItems "Dune", "Foundation", and "Neuromancer" exist and a status filter for "planned" is active
When the user clears the search query to empty
Then all MediaItems with status "planned" are displayed and no MediaItem is excluded based on the search query
Note: this scenario concerns MediaItem results only; Topics are not subject to the status filter.
*Traceability: REQ-F-042 | AC-027*

---

**Scenario: BDD-042 — Notes content is not searchable**
Given a MediaItem named "Arrival" exists with notes "contains the word cosmos" and name containing no search term
When the user enters search query "cosmos"
Then "Arrival" does not appear in the search results
*Traceability: REQ-F-043 | AC-028*

---

**Scenario: BDD-043 — Filter by media type**
Given MediaItems of types "book" and "movie" exist
When the user applies a type filter for "book"
Then only MediaItems of type "book" are displayed and no "movie" items appear
*Traceability: REQ-F-044 | AC-029*

---

**Scenario: BDD-044 — Filter by status**
Given MediaItems with statuses "planned" and "completed" exist
When the user applies a status filter for "completed"
Then only MediaItems with status "completed" are displayed
*Traceability: REQ-F-045 | AC-030*

---

**Scenario: BDD-045 — Rating filter with lower bound only**
Given MediaItems with ratings 5, 7, 9 and one unrated MediaItem exist
When the user applies a rating filter with lower bound 7 only
Then MediaItems with ratings 7 and 9 are displayed; rating 5 and the unrated item are not displayed
*Traceability: REQ-F-046–048 | AC-031, AC-034*

---

**Scenario: BDD-046 — Rating filter with upper bound only**
Given MediaItems with ratings 3, 5, 8 and one unrated MediaItem exist
When the user applies a rating filter with upper bound 5 only
Then MediaItems with ratings 3 and 5 are displayed; rating 8 and the unrated item are not displayed
*Traceability: REQ-F-046–048 | AC-032, AC-034*

---

**Scenario: BDD-047 — Rating filter with both bounds**
Given MediaItems with ratings 3, 4, 7, 8 and one unrated MediaItem exist
When the user applies a rating filter with lower bound 4 and upper bound 7
Then MediaItems with ratings 4 and 7 are displayed; ratings 3 and 8 and the unrated item are not displayed
*Traceability: REQ-F-046–048 | AC-033, AC-034*

---

**Scenario: BDD-048 — Reject inverted rating range**
Given the personal library is open
When the user attempts to apply a rating filter with lower bound 8 and upper bound 3
Then the filter is rejected and a message informs the user that the lower bound must not exceed the upper bound
*Traceability: REQ-F-065, VR-010 | AC-048*

---

**Scenario: BDD-049 — Filter by Topic returns only associated MediaItems**
Given Topic "Classics" is associated with MediaItems "Hamlet" and "Othello" and MediaItem "Dune" is not associated
When the user applies a Topic filter for "Classics"
Then "Hamlet" and "Othello" are displayed and "Dune" is not displayed
*Traceability: REQ-F-049 | AC-035*

---

**Scenario: BDD-050 — Filter by empty Topic returns empty results**
Given a Topic named "Unassigned" exists with no associated MediaItems
When the user applies a Topic filter for "Unassigned"
Then no MediaItems are displayed
*Traceability: REQ-F-049 | AC-035*

---

**Scenario: BDD-051 — Multiple filters combined with AND logic**
Given MediaItems include: a "book" with status "completed", a "book" with status "planned", and a "movie" with status "completed"
When the user applies a type filter for "book" and a status filter for "completed"
Then only the "book" with status "completed" is displayed; the "book" with status "planned" and the "movie" with status "completed" are not displayed
*Traceability: REQ-F-050 | AC-036*

---

**Scenario: BDD-052 — Sort by name ascending**
Given MediaItems named "Cosmos", "Astronomy", and "Zebra" exist
When the user selects sort by name ascending
Then the displayed order is: "Astronomy", "Cosmos", "Zebra"
*Traceability: REQ-F-051 | AC-037*

---

**Scenario: BDD-053 — Sort by name descending**
Given MediaItems named "Cosmos", "Astronomy", and "Zebra" exist
When the user selects sort by name descending
Then the displayed order is: "Zebra", "Cosmos", "Astronomy"
*Traceability: REQ-F-052 | AC-038*

---

**Scenario: BDD-054 — Sort by rating ascending places unrated items last**
Given MediaItems with ratings 3, 5, 7 and one unrated MediaItem exist
When the user selects sort by rating ascending
Then the display order is: rating 3, rating 5, rating 7, then the unrated item
*Traceability: REQ-F-053, REQ-F-055 | AC-039*

---

**Scenario: BDD-055 — Sort by rating descending places unrated items last**
Given MediaItems with ratings 3, 5, 7 and one unrated MediaItem exist
When the user selects sort by rating descending
Then the display order is: rating 7, rating 5, rating 3, then the unrated item
*Traceability: REQ-F-054–055 | AC-040*

---

**Scenario: BDD-056 — Combined search + filter + rating sort**
Given MediaItems include: "Astronomy Guide" (book, completed, rating 8), "Astronomy Manual" (book, planned, rating 6), "Physics Primer" (article, completed, rating 9)
When the user enters search query "astro", applies a type filter for "book", and applies sort by rating descending
Then "Astronomy Guide" and "Astronomy Manual" are displayed in order: "Astronomy Guide" (8) then "Astronomy Manual" (6)
And "Physics Primer" is not displayed
*Traceability: REQ-F-057–058 | AC-041*

---

**Scenario: BDD-057 — All data types persist across application relaunch**
Given a MediaItem "Hyperion" (book, in progress, notes "epic", rating 9) associated with Topic "Science Fiction" exists
When the application is closed and relaunched
Then "Hyperion" is present with all its fields unchanged and is still associated with Topic "Science Fiction"
*Traceability: REQ-F-008, REQ-NF-005 | AC-049, AC-063*

---

**Scenario: BDD-058 — Save failure triggers notification and prior data remains intact**
Given a MediaItem exists in the personal library with previously saved data
And a save failure condition is simulated at the test-environment level for the next write operation
Note: failure injection is a verification setup condition, not a system requirement; the mechanism is implementation-dependent
When the user edits the MediaItem's name
Then a save failure notification is presented to the user
And the previously persisted data remains intact and accessible
*Traceability: REQ-F-060, REQ-F-066, REQ-NF-006 | AC-050*

---

**Scenario: BDD-059 — Unsaved change remains accessible in current session after save failure**
Given a save failure occurs after the user edits a MediaItem's rating to 8
When the user continues in the same session without relaunching
Then the rating value 8 is still visible and accessible to the user
*Traceability: REQ-F-061 | AC-051, AC-062*

---

**Scenario: BDD-060 — All core operations succeed without network access**
Given the application is running with all network interfaces disabled on the test machine
When the user performs each of: create a MediaItem, edit a MediaItem, delete a MediaItem, create a Topic, rename a Topic, delete a Topic, add an association, remove an association, search for a MediaItem, apply a filter, and sort the list
Then all operations complete successfully
And no network-related error, prompt, or degraded behavior is presented
And all in-scope features remain fully available and functional with no reduction in capability
*Traceability: REQ-NF-008 | AC-055*

---

**Scenario: BDD-061 — No authentication UI is present**
Given the application is launched and running
When the user inspects all available screens and states
Then no login form, password prompt, account creation screen, or profile selection screen is present at any point
*Traceability: IR-002 | AC-058*

---

**Scenario: BDD-062 — No connection-related UI is present**
Given the application is launched and running
When the user inspects all available screens and states
Then no network status indicator, online/offline toggle, or connectivity prompt is present at any point
*Traceability: IR-003 | AC-059*

---

**Scenario: BDD-063 — Status field defaults to "planned" on new MediaItem creation**
Given the user opens the MediaItem creation form
When the form is first displayed, before any user input
Then the status field shows "planned" as the pre-selected value
*Traceability: IR-006 | AC-060*

---

**Scenario: BDD-064 — No explicit Save action is required**
Given the user creates a new MediaItem with valid fields
When the user completes the creation without performing any explicit save action
Then the MediaItem is present in the personal library immediately
*Traceability: IR-040, REQ-F-059 | AC-061*

---

**Scenario: BDD-065 — All user-facing text is in English**
Given the application is running
When the user navigates through all available screens, forms, labels, prompts, confirmation dialogs, validation messages, and error notifications present in the application
Then all text visible to the user is in English and no non-English text is present in any user-facing element
*Traceability: REQ-NF-010, IR-001 | AC-057*

---

**Scenario: BDD-066 — Explicitly selected non-default status is preserved at creation**
Given the personal library is open
When the user creates a new MediaItem with name "Arrival", type "movie", and explicitly selects status "in progress"
Then the created MediaItem named "Arrival" has status "in progress"
And the status is not "planned"
*Traceability: REQ-F-001, REQ-F-003, REQ-F-004 | AC-001, AC-002*

---

**Scenario: BDD-067 — Unified search results with heterogeneous types via substring matching**
Given a MediaItem named "Science" exists and a Topic named "Science Fiction" exists
When the user enters search query "scie"
Then both a result for MediaItem "Science" and a result for Topic "Science Fiction" appear in the same results list
And the MediaItem result is identifiable as a MediaItem and the Topic result is identifiable as a Topic
*Traceability: REQ-F-039–040, IR-024 | AC-023, AC-024, AC-026*

---

**Scenario: BDD-068 — AND-logic multi-filter produces empty result when no item satisfies all filters**
Given MediaItems of type "book" with status "planned" and type "movie" with status "completed" exist
And no MediaItem of type "book" with status "completed" exists
When the user applies a type filter for "book" and a status filter for "completed" simultaneously
Then no MediaItems are displayed and the result list is empty
*Traceability: REQ-F-050 | AC-036*

---

**Scenario: BDD-069 — Combined search, filter, and name-ascending sort**
Given MediaItems include: "Astronomy Guide" (book, completed), "Astronomy Manual" (book, planned), "Biology Primer" (book, completed), "Physics Atlas" (article, completed)
When the user enters search query "astro", applies a type filter for "book", and applies sort by name ascending
Then "Astronomy Guide" and "Astronomy Manual" are displayed in name-ascending order
And "Biology Primer" is not displayed (does not match search query)
And "Physics Atlas" is not displayed (does not match type filter)
*Traceability: REQ-F-057–058 | AC-041*

---

**Scenario: BDD-070 — One MediaItem associated with multiple Topics simultaneously (many-to-many)**
Given a MediaItem named "Cosmos" exists and Topics "Science" and "Space" exist
When the user associates "Cosmos" with Topic "Science" and also with Topic "Space"
Then when viewing the MediaItem "Cosmos", both "Science" and "Space" are listed as associated Topics
And when viewing Topic "Science", "Cosmos" is listed as an associated MediaItem
And when viewing Topic "Space", "Cosmos" is also listed as an associated MediaItem
*Traceability: REQ-F-030, REQ-F-035–036 | AC-018, AC-021, AC-022*

---


## 11. Traceability Matrix

### 11.1 Functional Requirements → Acceptance Criteria → BDD Scenarios

| REQ-F | Description (abbreviated) | AC | BDD |
|---|---|---|---|
| REQ-F-001 | Create MediaItem | AC-001 | BDD-001, BDD-002, BDD-066 |
| REQ-F-002 | Name required | AC-001, AC-042 | BDD-001, BDD-004, BDD-005 |
| REQ-F-003 | Type required | AC-001 | BDD-001, BDD-002, BDD-066 |
| REQ-F-004 | Default status planned | AC-002 | BDD-002, BDD-063, BDD-066 |
| REQ-F-005 | Notes optional | AC-003 | BDD-001, BDD-003 |
| REQ-F-006 | Rating optional | AC-003 | BDD-001, BDD-003 |
| REQ-F-007 | Topics at creation | AC-004 | BDD-002 |
| REQ-F-008 | Auto-save on create | AC-005 | BDD-003, BDD-057 |
| REQ-F-009 | View MediaItem | AC-006 | BDD-009, BDD-010 |
| REQ-F-010 | Edit MediaItem | AC-007 | BDD-011, BDD-012 |
| REQ-F-011 | Auto-save on edit | AC-007 | BDD-011, BDD-012 |
| REQ-F-012 | Delete MediaItem | AC-008 | BDD-013 |
| REQ-F-013 | Deletion confirmation | AC-008, AC-009 | BDD-013, BDD-014 |
| REQ-F-014 | Permanent delete | AC-008 | BDD-013 |
| REQ-F-015 | Remove associations on delete | AC-010 | BDD-015 |
| REQ-F-016 | Topics unaffected by item delete | AC-010 | BDD-015 |
| REQ-F-017 | No restore | AC-011 | BDD-016 |
| REQ-F-018 | Set status | AC-012 | BDD-017a, BDD-017b |
| REQ-F-019 | Free status change | AC-012 | BDD-017a, BDD-017b |
| REQ-F-020 | Create Topic | AC-013 | BDD-018 |
| REQ-F-021 | Auto-save Topic create | AC-013 | BDD-018 |
| REQ-F-022 | View Topic | AC-014 | BDD-023, BDD-024 |
| REQ-F-023 | Rename Topic | AC-015 | BDD-025 |
| REQ-F-024 | Rename preserves associations | AC-015 | BDD-025 |
| REQ-F-025 | Auto-save Topic rename | AC-015 | BDD-025 |
| REQ-F-026 | Delete Topic | AC-016 | BDD-027 |
| REQ-F-027 | Topic deletion confirmation | AC-016, AC-017 | BDD-027, BDD-028 |
| REQ-F-028 | Remove associations on Topic delete | AC-016 | BDD-027, BDD-029 |
| REQ-F-029 | MediaItems unaffected by Topic delete | AC-016 | BDD-029 |
| REQ-F-030 | Associate from MediaItem side (add) | AC-018 | BDD-030, BDD-070 |
| REQ-F-031 | Disassociate from MediaItem side | AC-018 | BDD-031 |
| REQ-F-032 | Associate from Topic side (add) | AC-019 | BDD-032 |
| REQ-F-033 | Disassociate from Topic side | AC-019 | BDD-033 |
| REQ-F-034 | Auto-save association change | AC-020 | BDD-030, BDD-032, BDD-034 |
| REQ-F-035 | Navigate Topic → MediaItem | AC-021 | BDD-035, BDD-070 |
| REQ-F-036 | See Topics from MediaItem | AC-022 | BDD-036, BDD-070 |
| REQ-F-037 | Navigate MediaItem → Topic | AC-022 | BDD-036 |
| REQ-F-038 | Enter search query | AC-023 | BDD-037 |
| REQ-F-039 | Search MediaItem names | AC-023, AC-026 | BDD-037, BDD-039, BDD-067 |
| REQ-F-040 | Search Topic names | AC-024, AC-026 | BDD-038, BDD-039, BDD-067 |
| REQ-F-041 | Open Topic from search | AC-025 | BDD-040 |
| REQ-F-042 | Empty search = inactive | AC-027 | BDD-041 |
| REQ-F-043 | Notes not searchable | AC-028 | BDD-042 |
| REQ-F-044 | Filter by type | AC-029 | BDD-043 |
| REQ-F-045 | Filter by status | AC-030 | BDD-044 |
| REQ-F-046 | Filter by rating range | AC-031–033 | BDD-045–047 |
| REQ-F-047 | One or both rating bounds | AC-031–033 | BDD-045–047 |
| REQ-F-048 | Exclude unrated when filtering | AC-034 | BDD-045–047 |
| REQ-F-049 | Filter by Topic | AC-035 | BDD-049, BDD-050 |
| REQ-F-050 | AND logic for multiple filters | AC-036 | BDD-051, BDD-068 |
| REQ-F-051 | Sort name ascending | AC-037 | BDD-052 |
| REQ-F-052 | Sort name descending | AC-038 | BDD-053 |
| REQ-F-053 | Sort rating ascending | AC-039 | BDD-054 |
| REQ-F-054 | Sort rating descending | AC-040 | BDD-055 |
| REQ-F-055 | Unrated items last in rating sort | AC-039, AC-040 | BDD-054, BDD-055 |
| REQ-F-056 | Unspecified tie order | — | — |
| REQ-F-057 | Combine search+filter+sort | AC-041 | BDD-056, BDD-069 |
| REQ-F-058 | Filter then sort in combined | AC-041 | BDD-056, BDD-069 |
| REQ-F-059 | Auto-save | AC-049, AC-061 | BDD-012, BDD-064 |
| REQ-F-060 | Notify on save failure | AC-050, AC-062 | BDD-058 |
| REQ-F-061 | Retain unsaved change in session | AC-051, AC-062 | BDD-059 |
| REQ-F-062 | Reject empty name | AC-042 | BDD-004, BDD-005 |
| REQ-F-063 | Reject invalid Topic name | AC-045, AC-046 | BDD-019–021, BDD-026 |
| REQ-F-064 | Reject rating out of range | AC-044 | BDD-007, BDD-008 |
| REQ-F-065 | Reject inverted rating range | AC-048 | BDD-048 |
| REQ-F-066 | Save failure notification mechanism | AC-050 | BDD-058 |

### 11.2 Non-Functional Requirements → Acceptance Criteria → BDD Scenarios

| REQ-NF | Description (abbreviated) | AC | BDD |
|---|---|---|---|
| REQ-NF-001 | Performance — no perceptible delay | AC-052 | — (qualitative; evaluator judgment) |
| REQ-NF-002 | Usable without documentation | AC-053 | — (qualitative; evaluator judgment) |
| REQ-NF-003 | Informative validation feedback | AC-042–048 | BDD-004–008, BDD-019–021, BDD-026, BDD-048 |
| REQ-NF-004 | Deletion confirmation prompt | AC-008, AC-009, AC-016, AC-017 | BDD-013, BDD-014, BDD-027, BDD-028 |
| REQ-NF-005 | Data durability across sessions | AC-005, AC-013, AC-015, AC-020, AC-049, AC-063 | BDD-003, BDD-018, BDD-025, BDD-034, BDD-057 |
| REQ-NF-006 | Save failure isolation | AC-050 | BDD-058 |
| REQ-NF-007 | Referential consistency | AC-054 | BDD-015, BDD-029 |
| REQ-NF-008 | Offline operation | AC-055, AC-068 | BDD-060 |
| REQ-NF-009 | Local data boundary | AC-056 | BDD-060 |
| REQ-NF-010 | English language | AC-057 | BDD-065 |
| REQ-NF-011 | Platform independence | — | — (specification meta-constraint) |

### 11.3 Interface Requirements → Acceptance Criteria → BDD Scenarios

| IR | Description (abbreviated) | AC | BDD |
|---|---|---|---|
| IR-001 | English text | AC-057 | BDD-065 |
| IR-002 | No auth UI | AC-058 | BDD-061 |
| IR-003 | No connection UI | AC-059 | BDD-062 |
| IR-004 | Create MediaItem entry point | AC-001 | BDD-001 |
| IR-005 | All fields at creation | AC-001–004 | BDD-001, BDD-002 |
| IR-006 | Default status pre-selected | AC-060 | BDD-063 |
| IR-007 | View all fields | AC-006 | BDD-009, BDD-010 |
| IR-008 | All fields editable | AC-007 | BDD-011, BDD-012 |
| IR-009 | Delete MediaItem entry point | AC-008 | BDD-013 |
| IR-010 | Delete confirmation prompt | AC-008, AC-009 | BDD-013, BDD-014 |
| IR-011 | Create Topic entry point | AC-013 | BDD-018 |
| IR-012 | View Topic with items | AC-014 | BDD-023, BDD-024 |
| IR-013 | Rename Topic entry point | AC-015 | BDD-025 |
| IR-014 | Delete Topic entry point | AC-016 | BDD-027 |
| IR-015 | Topic deletion confirmation | AC-016, AC-017 | BDD-027, BDD-028 |
| IR-016 | Associate from MediaItem side | AC-018 | BDD-030, BDD-031 |
| IR-017 | Associate from Topic side | AC-019 | BDD-032, BDD-033 |
| IR-018 | Navigate Topic → MediaItem | AC-021 | BDD-035 |
| IR-019 | Navigate MediaItem → Topic | AC-022 | BDD-036 |
| IR-020 | Search entry | AC-023 | BDD-037 |
| IR-021 | Present MediaItem search results | AC-023 | BDD-037 |
| IR-022 | Present Topic search results | AC-024 | BDD-038 |
| IR-023 | Open Topic from search | AC-025 | BDD-040 |
| IR-024 | Unified search results list | AC-026 | BDD-039, BDD-067 |
| IR-025 | Empty search = no restriction | AC-027 | BDD-041 |
| IR-026 | Type filter | AC-029 | BDD-043 |
| IR-027 | Status filter | AC-030 | BDD-044 |
| IR-028 | Rating filter bounds | AC-031–033 | BDD-045–047 |
| IR-029 | Topic filter | AC-035 | BDD-049, BDD-050 |
| IR-030 | AND logic reflected | AC-036 | BDD-051, BDD-068 |
| IR-031 | Sort by name | AC-037, AC-038 | BDD-052, BDD-053 |
| IR-032 | Sort by rating | AC-039, AC-040 | BDD-054, BDD-055 |
| IR-033 | Unrated last in rating sort | AC-039, AC-040 | BDD-054, BDD-055 |
| IR-034 | Combined operations | AC-041 | BDD-056, BDD-069 |
| IR-035 | Feedback: MediaItem name violation | AC-042 | BDD-004, BDD-005 |
| IR-036 | Feedback: rating violation | AC-044 | BDD-007, BDD-008 |
| IR-037 | Feedback: Topic name empty | AC-045 | BDD-019 |
| IR-038 | Feedback: Topic name not unique | AC-046 | BDD-020, BDD-021, BDD-026 |
| IR-039 | Feedback: rating range invalid | AC-048 | BDD-048 |
| IR-040 | No explicit Save action | AC-061 | BDD-012, BDD-064 |
| IR-041 | Save failure notification | AC-050, AC-062 | BDD-058 |
| IR-042 | Unsaved change visible after failure | AC-051, AC-062 | BDD-059 |
| IR-043 | Library present on launch | AC-063 | BDD-057 |

### 11.4 Constraints → Acceptance Criteria

| CON | AC |
|---|---|
| CON-001 | AC-064 |
| CON-002 | AC-065 |
| CON-003 | AC-044 |
| CON-004 | AC-066 |
| CON-005 | AC-067 |
| CON-006 | — (no dedicated AC; enforced via model) |
| CON-007 | AC-046, AC-047 |
| CON-008 | AC-058 |
| CON-009 | AC-068 |
| CON-010 | AC-056 |
| CON-011 | AC-057 |
| CON-012 | — (specification meta-constraint) |
| CON-013 | AC-069 |

---

## 12. Verification Summary

### 12.1 Requirements Coverage

| Category | Count | AC Coverage | BDD Coverage |
|---|---|---|---|
| Functional requirements (REQ-F) | 66 | All except REQ-F-056 (tie order — untestable by design) | All with meaningful user behavior |
| Business rules (BR) | 10 | Covered via associated REQ-F | Covered via associated REQ-F |
| Validation rules (VR) | 11 | Covered via REQ-F-062–065 | BDD-004–008, BDD-019–022, BDD-026, BDD-047–048 |
| Non-functional requirements (REQ-NF) | 11 | All. REQ-NF-001, REQ-NF-002, REQ-NF-011 noted below. | All with user-visible behavior |
| Interface requirements (IR) | 43 | All | All |
| Constraints (CON) | 13 | All except CON-006 and CON-012 (noted below) | Via associated requirements |

### 12.2 Intentional Verification Gaps

The following items have no dedicated acceptance criterion or BDD scenario; this is intentional and documented.

| Item | Reason |
|---|---|
| REQ-F-056 (tie order) | Approved specification explicitly states relative order within ties is unspecified. No criterion is possible. |
| REQ-NF-001 (performance) | AC-052 exists but is qualitative (evaluator judgment). No quantitative threshold was approved. |
| REQ-NF-002 (usability) | AC-053 exists but requires human evaluator judgment, not automated verification. |
| REQ-NF-011 (platform independence) | Specification meta-constraint. Verified by reviewing specification artifacts, not by testing the system. |
| CON-006 (single notes field) | Enforced by the approved domain model and the absence of any multi-note mechanism. No separate AC needed. |
| CON-012 (platform independence) | Same as REQ-NF-011. |

### 12.3 Verification Methods by Requirement Type

| Requirement type | Primary verification method |
|---|---|
| Functional requirements | Functional testing against ACs and BDD scenarios |
| Validation rules | Boundary-value testing of accept/reject conditions |
| Non-functional (qualitative) | Expert evaluation or structured walkthrough |
| Non-functional (behavioral) | System-level testing (offline test, network monitoring) |
| Interface requirements | Inspection and interaction testing |
| Constraints | Model inspection, negative testing, scope audit |
| Data durability | Session-boundary tests (close/relaunch cycles) |
| Save failure | Test-environment failure injection (mechanism is implementation-dependent) |

### 12.4 Specification Completeness Assessment

| Criterion | Status |
|---|---|
| All in-scope capabilities specified | Complete |
| All out-of-scope capabilities declared | Complete |
| Domain model fully defined | Complete |
| All validation rules specified | Complete |
| All lifecycle operations specified | Complete |
| Persistence and failure behavior specified | Complete |
| Search, filter, and sort behavior fully specified | Complete |
| Qualitative NFRs acknowledged as qualitative | Complete |
| Platform and technology stack intentionally deferred | Documented |
| Traceability from requirements to ACs to BDD complete | Complete |
| No new functionality introduced during SRS construction | Verified |
| No approved decision contradicted | Verified |

### 12.5 Open Items

| Item | Status | Resolution path |
|---|---|---|
| Target platform and OS | Unresolved by human decision (HD-009, HD-047) | Requires a new explicit human decision before implementation begins |
| Technology stack | Unresolved by human decision | Same as above |
| Quantitative performance threshold | Confirmed as not required (Q-NFR-02) | No action needed |
| Maximum library size | Confirmed as not required (Q-NFR-03) | No action needed |
| Quantitative reliability target | Confirmed as not required (Q-NFR-04) | No action needed |

### 12.6 Addendum 001 Implementation Verification

The original SRS-001 v1.0 requirements remain the approved baseline; the
following additive requirements and acceptance artifacts are defined by
SRS-ADD-001:

| Addendum artifact | Scope | Verification status |
|---|---|---|
| Functional requirements | REQ-F-070..074 | PASS |
| Acceptance criteria | AC-070..075 | PASS |
| BDD scenarios | BDD-071..075 | PASS |
| Unit and OpenAPI contract suite | `pytest tests/ --tb=short -q` | PASS — 297/297 |
| API contract | `GET /api/stats`, responses 200 and 500 | PASS |

The additive operation does not change any existing route or response
contract. See [SRS-ADD-001](addendum-001-collection-stats.md) and
[RTM-001](traceability.md) for detailed scope and verification links.

---

*End of Software Requirements Specification — Version 1.0*
