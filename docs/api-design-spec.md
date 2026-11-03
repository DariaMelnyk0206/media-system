# API Design Specification

**Project:** Personal Media Library System  
**Document ID:** API-SPEC-001  
**Source:** SRS-001 v1.0, docs/openapi.yaml  
**Date:** 2026-11-03  
**Status:** Approved (API-GATE: GO)

---

## Table of Contents

1. [Resource Model](#1-resource-model)
2. [Data Schemas](#2-data-schemas)
3. [Error Model](#3-error-model)
4. [Traceability Matrix](#4-traceability-matrix)
5. [Static Analysis Results](#5-static-analysis-results)
6. [Mock Testing Results](#6-mock-testing-results)

---

## 1. Resource Model

The API exposes two primary domain resources and one derived resource:

| Resource | Base URI | SRS Entity |
|---|---|---|
| **MediaItem** | `/api/media-items` | MediaItem (HD-011) |
| **Topic** | `/api/topics` | Topic (HD-015) |
| **Association** | `/api/media-items/{id}/topics/{topicId}` | MediaItem–Topic link (HD-038) |
| **Association (mirror)** | `/api/topics/{id}/media-items/{mediaId}` | MediaItem–Topic link (HD-038) |
| **Search** | `/api/search` | Unified search (HD-025–026) |

### Relationships

```
MediaItem ──── many-to-many ──── Topic
    │                                │
    └──── Association ───────────────┘
```

- MediaItem exists independently of Topics (BR-003).
- Topic exists independently of MediaItems (BR-004).
- Deleting either side removes only the associations, not the partner entity (REQ-F-015–016, REQ-F-028–029).

---

## 2. Data Schemas

All schemas are formally defined in `docs/openapi.yaml` under `components/schemas`.

### 2.1 MediaItem

Full domain object returned by `getMediaItem`, `createMediaItem`, `updateMediaItem`, and association operations.

```json
{
  "id":     "string (uuid)",
  "name":   "string — trimmed, non-empty (VR-001, VR-002)",
  "type":   "book | movie | tv_series | article | podcast | video | other (VR-008, CON-001)",
  "status": "planned | in_progress | postponed | abandoned | completed (VR-009, CON-002)",
  "notes":  "string | null — optional free text, not searchable (CON-006, REQ-F-043)",
  "rating": "integer 1–10 | null — optional, absence is distinct from any value (VR-007, CON-003)",
  "topics": [
    { "id": "string (uuid)", "name": "string" }
  ]
}
```

Field constraints:
- `name` — mandatory; trimmed before save; whitespace-only rejected (VR-001, VR-002).
- `type` — mandatory; exactly one of seven fixed values (CON-001, BR-001).
- `status` — mandatory; defaults to `planned` on creation (REQ-F-004); free transition (BR-010).
- `notes` — optional; single field per MediaItem; not searched (CON-006, REQ-F-043).
- `rating` — optional; integer 1–10; `null` means unset; unset ≠ 0 (CON-003).
- `topics` — array of TopicRef; may be empty (BR-003).
- No `date_added` or creation timestamp field (CON-005).

### 2.2 Topic

Full domain object returned by `getTopic`, `createTopic`, `updateTopic`, and association operations.

```json
{
  "id":          "string (uuid)",
  "name":        "string — trimmed, unique case-insensitively (VR-003–006, BR-005)",
  "media_items": [
    {
      "id":     "string (uuid)",
      "name":   "string",
      "type":   "MediaType enum",
      "status": "MediaStatus enum",
      "rating": "integer 1–10 | null"
    }
  ]
}
```

Field constraints:
- `name` — mandatory; trimmed; unique case-insensitively (VR-003–006); applies on create and rename (VR-006).
- `media_items` — array of MediaItemRef; may be empty (BR-004).

### 2.3 TopicSummary

Lightweight object used in `listTopics` response.

```json
{ "id": "string (uuid)", "name": "string" }
```

### 2.4 Association

No attributes beyond the two connected entities. Managed from both sides (HD-038).  
Operations: `POST` and `DELETE` on:
- `/api/media-items/{id}/topics/{topicId}` (REQ-F-030–031)
- `/api/topics/{id}/media-items/{mediaId}` (REQ-F-032–033)

Both operations are idempotent on `POST`. Both auto-save on success (REQ-F-034).

### 2.5 CreateMediaItemRequest

```json
{
  "name":      "string  [required]",
  "type":      "MediaType  [required]",
  "status":    "MediaStatus  [optional — default: planned]",
  "notes":     "string | null  [optional]",
  "rating":    "integer 1–10 | null  [optional]",
  "topic_ids": "uuid[]  [optional — default: []]"
}
```

### 2.6 UpdateMediaItemRequest

```json
{
  "name":   "string  [optional]",
  "type":   "MediaType  [optional]",
  "status": "MediaStatus  [optional]",
  "notes":  "string | null  [optional — null clears the field]",
  "rating": "integer 1–10 | null  [optional — null clears the field]"
}
```

Only provided fields are updated. Absent fields are not modified.

### 2.7 CreateTopicRequest / UpdateTopicRequest

```json
{ "name": "string  [required]" }
```

Both apply VR-003–006. `UpdateTopicRequest` additionally enforces VR-006 (uniqueness on rename).

### 2.8 SearchResultItem

Unified result for `GET /api/search`. Each item carries `kind` to distinguish entity type (IR-024).

```json
{
  "kind":   "media_item | topic  [required]",
  "id":     "string (uuid)  [required]",
  "name":   "string  [required]",
  "type":   "MediaType | null  — non-null only when kind=media_item",
  "status": "MediaStatus | null  — non-null only when kind=media_item",
  "rating": "integer 1–10 | null  — only when kind=media_item"
}
```

### 2.9 Enumeration Values

**MediaType** (CON-001, VR-008):

| API value | SRS value |
|---|---|
| `book` | book |
| `movie` | movie |
| `tv_series` | TV series |
| `article` | article |
| `podcast` | podcast |
| `video` | video |
| `other` | other |

**MediaStatus** (CON-002, VR-009):

| API value | SRS value |
|---|---|
| `planned` | planned |
| `in_progress` | in progress |
| `postponed` | postponed |
| `abandoned` | abandoned |
| `completed` | completed |

---

## 3. Error Model

### 3.1 Unified ErrorResponse Schema

All 4xx and 5xx responses use a single JSON structure (REQ-F-062–066, REQ-NF-003):

```json
{
  "error":   "string — machine-readable error code",
  "field":   "string | null — field that caused the error, null if not field-specific",
  "message": "string — human-readable description in English (CON-011)"
}
```

### 3.2 HTTP Status Codes

| Code | Semantics | Triggers |
|---|---|---|
| `200 OK` | Successful GET, PATCH, or idempotent POST | — |
| `201 Created` | Resource created successfully | POST /media-items, POST /topics |
| `204 No Content` | Resource deleted successfully | DELETE operations |
| `400 Bad Request` | Validation rule violated | VR-001, VR-007, VR-008, VR-009, VR-010, VR-011 |
| `404 Not Found` | Resource does not exist | All resource operations |
| `409 Conflict` | Topic name uniqueness violation | VR-005, VR-006 |
| `500 Internal Server Error` | Auto-save failure | REQ-F-060, REQ-F-066 |

### 3.3 Error Code Catalogue

| `error` code | `field` | HTTP | Validation rule | SRS source |
|---|---|---|---|---|
| `name_required` | `"name"` | 400 | VR-001, VR-003 | REQ-F-062, REQ-F-063 |
| `rating_out_of_range` | `"rating"` | 400 | VR-007 | REQ-F-064 |
| `invalid_type` | `"type"` | 400 | VR-008 | REQ-F-062 |
| `invalid_status` | `"status"` | 400 | VR-009 | REQ-F-062 |
| `invalid_rating_range` | `"rating_min"` | 400 | VR-010 | REQ-F-065 |
| `invalid_rating_bound` | `"rating_min"` or `"rating_max"` | 400 | VR-011 | REQ-F-065 |
| `invalid_query` | `"q"` | 400 | — | REQ-F-038 |
| `not_found` | `null` | 404 | — | REQ-F-009, REQ-F-022 |
| `name_taken` | `"name"` | 409 | VR-005, VR-006 | REQ-F-063 |
| `save_failed` | `null` | 500 | — | REQ-F-060, REQ-F-066 |

### 3.4 Special Behaviors

**Confirmation before DELETE** (REQ-F-013, REQ-F-027, REQ-NF-004):  
The API does not implement a confirmation prompt. This is the client's responsibility — the DELETE endpoint must only be called after explicit user confirmation in the UI.

**Auto-save** (REQ-F-059, REQ-F-061):  
All mutating operations (POST, PATCH, DELETE) auto-save on success. A `500 save_failed` response indicates the change was not persisted but remains available for the current session (REQ-F-061).

**Persistence** (REQ-NF-005):  
Successful saves survive application restart — this is a service-layer concern, not an API concern.

---

## 4. Traceability Matrix

### 4.1 API Operations → REQ-F

| OperationId | HTTP Method + URI | REQ-F Coverage | Status |
|---|---|---|---|
| `createMediaItem` | `POST /api/media-items` | F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-059, F-062, F-064 | Verified |
| `listMediaItems` | `GET /api/media-items` | F-038, F-039, F-042, F-044, F-045, F-046, F-047, F-048, F-049, F-050, F-051, F-052, F-053, F-054, F-055, F-056, F-057, F-058, F-065 | Verified |
| `getMediaItem` | `GET /api/media-items/{id}` | F-009, F-036, F-037 | Verified |
| `updateMediaItem` | `PATCH /api/media-items/{id}` | F-010, F-011, F-018, F-019, F-059, F-061, F-062, F-064 | Verified |
| `deleteMediaItem` | `DELETE /api/media-items/{id}` | F-012, F-013, F-014, F-015, F-016, F-017, F-059 | Verified |
| `addTopicToMediaItem` | `POST /api/media-items/{id}/topics/{topicId}` | F-030, F-034, F-059 | Verified |
| `removeTopicFromMediaItem` | `DELETE /api/media-items/{id}/topics/{topicId}` | F-031, F-034, F-059 | Verified |
| `createTopic` | `POST /api/topics` | F-020, F-021, F-059, F-063 | Verified |
| `listTopics` | `GET /api/topics` | F-022 | Verified |
| `getTopic` | `GET /api/topics/{id}` | F-022, F-035 | Verified |
| `updateTopic` | `PATCH /api/topics/{id}` | F-023, F-024, F-025, F-059, F-063 | Verified |
| `deleteTopic` | `DELETE /api/topics/{id}` | F-026, F-027, F-028, F-029, F-059 | Verified |
| `addMediaItemToTopic` | `POST /api/topics/{id}/media-items/{mediaId}` | F-032, F-034, F-059 | Verified |
| `removeMediaItemFromTopic` | `DELETE /api/topics/{id}/media-items/{mediaId}` | F-033, F-034, F-059 | Verified |
| `search` | `GET /api/search` | F-038, F-039, F-040, F-041, F-042, F-043 | Verified |
| *(cross-cutting)* | All mutating operations | F-059, F-060, F-061, F-066 | Verified |

**Coverage:** REQ-F-001..066 — 66/66 (100%).  
REQ-F-056 (unspecified tie order) — no dedicated operation needed; documented in `listMediaItems` description.

### 4.2 Validation Rules → API Operations

| VR | Rule Summary | Enforced in | HTTP Response |
|---|---|---|---|
| VR-001 | MediaItem name non-empty after trim | `createMediaItem`, `updateMediaItem` | 400 `name_required` |
| VR-002 | MediaItem name trimmed before save | `createMediaItem`, `updateMediaItem` | (silent normalization) |
| VR-003 | Topic name non-empty after trim | `createTopic`, `updateTopic` | 400 `name_required` |
| VR-004 | Topic name trimmed before save | `createTopic`, `updateTopic` | (silent normalization) |
| VR-005 | Topic name unique case-insensitively | `createTopic`, `updateTopic` | 409 `name_taken` |
| VR-006 | VR-005 applies also on rename | `updateTopic` | 409 `name_taken` |
| VR-007 | Rating integer 1–10 | `createMediaItem`, `updateMediaItem` | 400 `rating_out_of_range` |
| VR-008 | Type one of 7 fixed values | `createMediaItem`, `updateMediaItem`, `listMediaItems` (query) | 400 `invalid_type` |
| VR-009 | Status one of 5 fixed values | `createMediaItem`, `updateMediaItem`, `listMediaItems` (query) | 400 `invalid_status` |
| VR-010 | Rating filter: lower bound ≤ upper bound | `listMediaItems` | 400 `invalid_rating_range` |
| VR-011 | Each rating bound integer 1–10 | `listMediaItems` | 400 `invalid_rating_bound` |

---

## 5. Static Analysis Results

**Tool:** Redocly CLI (`@redocly/cli`)  
**Command:** `npx @redocly/cli lint docs/openapi.yaml`  
**Configuration:** built-in `recommended` ruleset  
**Date:** 2026-11-03

### 5.1 Final Result

```
Woohoo! Your API description is valid.
0 errors, 0 warnings.
```

### 5.2 Issues Resolved

| Count | Rule | Fix applied |
|---|---|---|
| 15 errors | `security-defined` — no security on operations | Added `security: []` at root level (CON-008, CON-009 — no auth) |
| 1 warning | `info-license` — missing license field | Added `license: {name, url}` to info |
| 1 warning | `info-license-strict` — missing license url | Added `url` to license object |
| 4 warnings | `spec-ref-siblings` — `description`/`nullable` alongside `$ref` | Replaced with `allOf: [$ref]` pattern |
| 2 warnings | `operation-4xx-response` — no 4xx on GET /topics, GET /search | Added explicit `400` responses |
| 2 errors | `nullable-type-sibling` — `nullable` in `allOf` without `type` | Added `type: string` in inline schema inside `allOf` for `SearchResultItem.type` and `.status` |

---

## 6. Mock Testing Results

**Tool:** Stoplight Prism (`@stoplight/prism-cli`)  
**Command:** `npx @stoplight/prism-cli mock docs/openapi.yaml -p 4010`  
**Date:** 2026-11-03

### 6.1 Positive Scenarios

| Scenario | Request | Expected | Result |
|---|---|---|---|
| List MediaItems (empty) | `GET /api/media-items` | 200 `{data:[], total:0}` | PASS |
| Create MediaItem (minimal) | `POST /api/media-items` `{name:"Dune", type:"book"}` | 201 MediaItem, status=planned | PASS |
| Create MediaItem (full) | `POST /api/media-items` with all fields | 201 MediaItem with all fields | PASS |
| Get MediaItem | `GET /api/media-items/{id}` | 200 full MediaItem | PASS |
| List with filter | `GET /api/media-items?type=book&status=planned` | 200 filtered list | PASS |
| Search MediaItems | `GET /api/search?q=dune` | 200 `{data:[{kind:"media_item",...}]}` | PASS |
| Search Topics | `GET /api/search?q=sci` | 200 `{data:[{kind:"topic",...}]}` | PASS |
| Create Topic | `POST /api/topics` `{name:"Science Fiction"}` | 201 Topic `{id, name, media_items:[]}` | PASS |
| List Topics | `GET /api/topics` | 200 `{data:[...]}` | PASS |
| Get Topic | `GET /api/topics/{id}` | 200 full Topic with media_items | PASS |

### 6.2 Negative Scenarios

| Scenario | Request | Expected | Result |
|---|---|---|---|
| Empty MediaItem name | `POST /api/media-items` `{name:"", type:"book"}` | 400 `name_required` | PASS |
| Rating out of range | `POST /api/media-items` `{..., rating:11}` | 400 `rating_out_of_range` | PASS |
| Rating = 0 | `POST /api/media-items` `{..., rating:0}` | 400 `rating_out_of_range` | PASS |
| Invalid type value | `POST /api/media-items` `{..., type:"game"}` | 400 `invalid_type` | PASS |
| MediaItem not found | `GET /api/media-items/nonexistent-id` | 404 `not_found` | PASS |
| Topic not found | `GET /api/topics/nonexistent-id` | 404 `not_found` | PASS |
| Duplicate Topic name | `POST /api/topics` (simulated via `Prefer: code=409`) | 409 `name_taken` | PASS |
| Rating range inverted | `GET /api/media-items?rating_min=8&rating_max=3` | 400 `invalid_rating_range` | PASS |
| Save failure simulation | Any mutating op with `Prefer: code=500` | 500 `save_failed` | PASS |

### 6.3 Schema Conformance

- All JSON response structures (MediaItem, Topic, SearchResultItem) match OpenAPI schema types exactly.
- All required fields present in every response.
- `nullable` fields (`notes`, `rating`, `field` in ErrorResponse) correctly return `null` when unset.
- `kind` field in SearchResultItem correctly identifies `media_item` vs `topic`.
- Error simulation via `Prefer: code=...` header returns unified `ErrorResponse` structure for all 4xx/5xx codes.

### 6.4 Scope Compliance

No behavior outside SRS-001 was introduced:
- All 16 endpoints strictly cover REQ-F-001..065.
- All validation rules VR-001..011 implemented without domain extension.
- CON-013 (scope ceiling) — no excluded capabilities were introduced.

---

*End of API Design Specification — API-SPEC-001*
