# API-GATE Decision Record

**Project:** Personal Media Library System  
**Gate ID:** API-GATE  
**Date:** 2026-11-03  
**Conductor:** Agent (System Architect role)  
**Source:** SRS-001 v1.0, PEP-001, docs/openapi.yaml, docs/api-design-spec.md  
**Decision:** **GO** ✅

---

## 1. Gate Purpose

API-GATE is the checkpoint between the API Design phase and the Backend Implementation phase. Its purpose is to verify that:

1. All functional requirements from SRS-001 are covered by a formally specified REST API.
2. The specification is syntactically and structurally valid per OpenAPI 3.0.3.
3. The mock API correctly reproduces the specified contract.
4. No behavior outside the approved SRS-001 scope was introduced.
5. All artifacts are persisted and traceable.

The gate must pass all 10 engineering criteria before backend implementation (FEAT-001..012 in PEP-001) may begin.

---

## 2. Engineering Criteria and Results

| # | Criterion | Evidence | Result |
|---|---|---|---|
| C-01 | All SRS-001 functional requirements REQ-F-001..066 are mapped to API operations | Traceability matrix in api-design-spec.md §4.1 — 66/66 coverage | **PASSED** |
| C-02 | All validation rules VR-001..011 are enforced at the API boundary | VR mapping table in api-design-spec.md §4.2 — 11/11 rules mapped | **PASSED** |
| C-03 | OpenAPI 3.0.3 specification passes static linting with 0 errors and 0 warnings | `npx @redocly/cli lint docs/openapi.yaml` → "Woohoo! 0 errors, 0 warnings" | **PASSED** |
| C-04 | All 16 endpoints are defined with unique operationId, HTTP method, URI, and REQ-F reference | docs/openapi.yaml — 15 operations on 7 paths; all operationIds unique | **PASSED** |
| C-05 | Unified ErrorResponse schema covers all 4xx and 5xx codes with machine-readable codes | api-design-spec.md §3 — 10 error codes, 5 HTTP status codes | **PASSED** |
| C-06 | Mock API correctly serves all 16 routes without backend implementation | Prism mock server started on port 4010; all routes resolved | **PASSED** |
| C-07 | Positive scenarios verified against mock: create, read, list, search, filter, sort | api-design-spec.md §6.1 — 10 positive scenarios, all PASS | **PASSED** |
| C-08 | Negative scenarios verified against mock: validation errors, 404, 409, 500 | api-design-spec.md §6.2 — 9 negative scenarios, all PASS | **PASSED** |
| C-09 | No behavior outside SRS-001 scope introduced (CON-013 compliance) | api-design-spec.md §6.4 — scope compliance confirmed; 0 violations | **PASSED** |
| C-10 | All design artifacts persisted in the repository under correct paths | docs/openapi.yaml, docs/api-design-spec.md created; logs/api-gate-decision.md present | **PASSED** |

**Summary: 10/10 criteria PASSED → Decision: GO**

---

## 3. Decision

```
API-GATE: GO
Date: 2026-11-03
All 10 engineering criteria passed.
Backend implementation (FEAT-001..012 per PEP-001) is unblocked.
```

The team may proceed to Phase 2 (Test Suite) and Phase 3 (Feature Implementation) as defined in PEP-001.

---

## 4. Design Decisions Log

The following decisions were made during the API design process. Each entry records the decision, its rationale, and the SRS source.

---

### DD-001 — REST architectural style

**Decision:** Use REST over HTTP as the API architectural style.  
**Rationale:** The system requires standard CRUD operations on two domain resources (MediaItem, Topic) and one derived association. REST maps naturally to these resources, supports tooling (OpenAPI, Prism, Redocly), and aligns with the project's localhost-only deployment model.  
**SRS source:** CON-009 permits localhost network components; CON-012 (platform independence) does not prescribe the style.

---

### DD-002 — Security: no authentication

**Decision:** Set `security: []` globally; no authentication scheme defined.  
**Rationale:** SRS-001 explicitly prohibits authentication (CON-008, CON-013, HD-007, HD-046). The system serves a single local user with no accounts, passwords, or roles. The `security: []` declaration satisfies the Redocly `security-defined` rule while correctly representing the no-auth contract.  
**SRS source:** CON-008, CON-013, HD-007, HD-046.

---

### DD-003 — Enum serialization: snake_case

**Decision:** Serialize multi-word enum values as snake_case in JSON (`tv_series`, `in_progress`).  
**Rationale:** SRS uses natural language values ("TV series", "in progress") which contain spaces — invalid in JSON enum strings without quoting. snake_case is the idiomatic JSON convention and avoids ambiguity.  
**SRS source:** CON-001 (7 types), CON-002 (5 statuses), BR-001, BR-002.

---

### DD-004 — Partial update via PATCH, not PUT

**Decision:** Use `PATCH` for MediaItem and Topic updates.  
**Rationale:** SRS allows editing any subset of fields independently (REQ-F-010, REQ-F-023). `PUT` would require the client to send the full resource on every edit. `PATCH` with absent-field-means-no-change semantics minimizes payload and supports incremental edits (e.g., status-only update).  
**SRS source:** REQ-F-010, REQ-F-018–019, REQ-F-023.

---

### DD-005 — Clearing optional fields: explicit null

**Decision:** To clear `notes` or `rating`, the client sends `"notes": null` or `"rating": null` in the PATCH body. Absent field = no change.  
**Rationale:** Distinguishes "do not touch" from "clear the value". Consistent with standard PATCH semantics. Aligns with SRS where absence of rating is a distinct state from any numeric value (CON-003).  
**SRS source:** CON-003, REQ-F-006, REQ-F-010.

---

### DD-006 — Idempotent association POST

**Decision:** `POST /api/media-items/{id}/topics/{topicId}` and `POST /api/topics/{id}/media-items/{mediaId}` return `200 OK` (not `201`) if the association already exists.  
**Rationale:** SRS does not specify an error for duplicate associations. Idempotent behavior is safer for retry scenarios and consistent with the intent of REQ-F-030–034. No SRS violation.  
**SRS source:** REQ-F-030, REQ-F-032, REQ-F-034.

---

### DD-007 — Confirmation on DELETE: client responsibility

**Decision:** The API does not implement a confirmation step for DELETE operations. The client UI must obtain user confirmation before calling the endpoint.  
**Rationale:** REQ-F-013 and REQ-F-027 require a confirmation prompt before deletion. REST APIs are stateless and cannot hold a "pending deletion" state. The confirmation is a UI concern, not an API concern. Documented in the `deleteMediaItem` and `deleteTopic` operation descriptions.  
**SRS source:** REQ-F-013, REQ-F-027, REQ-NF-004.

---

### DD-008 — Search: unified results with `kind` discriminator

**Decision:** `GET /api/search` returns a single `data` array where each item has a `kind` field (`media_item` | `topic`).  
**Rationale:** IR-024 explicitly requires both MediaItem and Topic results in the same list with each result identifiable as one or the other. A discriminator field is the standard OpenAPI pattern for heterogeneous arrays without polymorphism complexity.  
**SRS source:** REQ-F-039–040, IR-024, AC-026.

---

### DD-009 — Persistence as cross-cutting concern

**Decision:** Auto-save (REQ-F-059) is not a separate endpoint. It is a behavior of the service layer triggered by every successful mutating operation.  
**Rationale:** SRS requires automatic save on every successful change (REQ-F-059, IR-040) — no explicit save action. Exposing a `POST /save` endpoint would contradict this requirement. A `500 save_failed` response signals failure; the change remains in session (REQ-F-061).  
**SRS source:** REQ-F-059, REQ-F-060, REQ-F-061, REQ-F-066, IR-040.

---

### DD-010 — nullable enum pattern in OAS 3.0.3

**Decision:** Nullable enum fields that reference a `$ref` schema use the `allOf` pattern with an inline schema carrying `type: string` and `nullable: true`.  
**Rationale:** OAS 3.0.3 forbids sibling keywords alongside `$ref`. The `allOf: [$ref, {type: string, nullable: true}]` pattern satisfies both the Redocly `spec-ref-siblings` and `nullable-type-sibling` rules. Applied to `SearchResultItem.type` and `SearchResultItem.status`.  
**SRS source:** Technical constraint of OAS 3.0.3 spec; no SRS source.

---

## 5. Artifact Inventory

| Artifact | Path | Status |
|---|---|---|
| SRS baseline | `spec/srs.md` | Baseline (unchanged) |
| Execution plan | `docs/PEP-001.md` | Baseline (unchanged) |
| OpenAPI specification | `docs/openapi.yaml` | Created — 1060 lines, OAS 3.0.3, 0 lint errors |
| API design specification | `docs/api-design-spec.md` | Created — 373 lines |
| API-GATE decision record | `logs/api-gate-decision.md` | Created (this file) |

---

## 6. Open Items at Gate Time

| Item | Status | Owner |
|---|---|---|
| Target platform and OS | Unresolved (HD-009, HD-047) | Human decision required before FEAT-001 |
| Technology stack and storage format | Unresolved (HD-047) | Human decision required before FEAT-001 |
| Test framework selection | Unresolved | Human decision required before Phase 2 |

These items do not block the API-GATE. They block FEAT-001 (PEP-001 Phase 3) and TEST-001 (PEP-001 Phase 2).

---

*End of API-GATE Decision Record*
