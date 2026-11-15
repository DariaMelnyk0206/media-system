# SRS-001 Addendum 001 — Collection Statistics

**Document ID:** SRS-ADD-001  
**Feature:** FEAT-013 — Collection Statistics  
**Status:** Proposed for implementation  
**Date:** 2026-11-15  
**Applies to:** SRS-001 v1.0  
**Related test ticket:** TEST-016

## 1. Purpose and Business Value

This addendum specifies a read-only summary of the user's local media collection,
exposed by `GET /api/stats`. It lets a user understand collection size, the mix
of media types and consumption statuses, rating coverage and average, and the
distribution of MediaItems across Topics without manually counting records.

The endpoint computes its response from the current local collection. It does
not persist derived statistics, make network requests, or change any existing
MediaItem or Topic.

## 2. Scope and Definitions

- **MediaItem count:** number of MediaItems currently in the collection.
- **Topic count:** number of Topics currently in the collection.
- **Status/type distribution:** counts for every defined status and media type,
  including values with a count of zero. For each distribution, the sum equals
  the total MediaItem count.
- **Rated MediaItem:** a MediaItem with a non-null rating. Each such MediaItem
  contributes once to the average and `rated_count`.
- **Topic MediaItem count:** number of distinct MediaItems associated with the
  Topic. An item associated with multiple Topics contributes once to each
  relevant Topic's count; consequently, topic counts need not sum to the
  collection-wide MediaItem count. Topics with no associated items remain in
  the summary with a count of zero.
- **Rounding:** `average_rating` is the arithmetic mean of rated MediaItems,
  rounded to two decimal places using round-half-up. It is `null` when
  `rated_count` is zero.
- **Topic ordering:** descending `media_item_count`, then ascending Topic name
  using case-insensitive alphabetical order.

The endpoint is read-only and uses the existing local data boundary. It adds no
authentication, network, export, backup, recommendation, or other excluded
capability.

## 3. Functional Requirements

**REQ-F-070 — Collection totals.**  
`GET /api/stats` shall return `total_media_items` and `total_topics`, equal to
the current counts of MediaItems and Topics, respectively.

**REQ-F-071 — Status and type distributions.**  
The response shall provide `status_counts` for all five defined statuses and
`type_counts` for all seven defined media types. Every defined value shall be
present, including zero-count values, and each distribution shall sum to
`total_media_items`.

**REQ-F-072 — Rating aggregates.**  
The response shall provide `rated_count` and `average_rating`. Only non-null
ratings shall contribute; the average shall be rounded to two decimal places
using round-half-up, or be `null` when no MediaItem is rated.

**REQ-F-073 — Topic summary.**  
The response shall provide `topics_summary`, with one item for every Topic and
its count of distinct associated MediaItems. The list shall be ordered by
descending count, then by Topic name in case-insensitive ascending order.

**REQ-F-074 — Request logging.**  
Each request to `GET /api/stats` shall produce a `stats.query` log event with
the outcome/status. The event shall not include MediaItem names, notes, Topic
names, or other user-authored content.

## 4. Acceptance Criteria

> AC-047 through AC-052 are already assigned in SRS-001 v1.0. To avoid
> duplicate identifiers and preserve the approved baseline, this addendum uses
> the next available identifiers, AC-070 through AC-075.

**AC-070** A successful statistics response reports the current number of
MediaItems and Topics in `total_media_items` and `total_topics`.

**AC-071** `status_counts` and `type_counts` include every defined value,
including zero-count values, and each distribution sums to `total_media_items`.

**AC-072** The response counts only non-null ratings in `rated_count` and
`average_rating`; the mean is rounded half-up to two decimal places, and is
`null` when there are no ratings.

**AC-073** `topics_summary` includes every Topic and its distinct associated
MediaItem count, ordered by descending count and then case-insensitive
ascending name. An item associated with multiple Topics is counted once in
each of those Topics.

**AC-074** An empty collection returns zero totals, zero for every status/type
value, `rated_count: 0`, `average_rating: null`, and an empty `topics_summary`.

**AC-075** Every statistics request produces a `stats.query` log event without
user-authored content. If processing fails, the API returns HTTP 500 using the
existing `ErrorResponse` format.

## 5. BDD Scenarios

**BDD-071 — Statistics for an empty collection**  
Given the collection has no MediaItems and no Topics  
When the user requests `GET /api/stats`  
Then both totals are zero, all status/type counts are zero, `rated_count` is
zero, `average_rating` is null, and `topics_summary` is empty  
And the response status is 200.

**BDD-072 — Rating aggregates exclude unrated items**  
Given the collection contains MediaItems rated 8 and 7, plus one unrated
MediaItem  
When the user requests `GET /api/stats`  
Then `rated_count` is 2 and `average_rating` is 7.5  
And the status and type distributions include all three MediaItems.

**BDD-073 — Topic counts reflect many-to-many associations**  
Given one MediaItem is associated with Topics "Science" and "Space", another
MediaItem is associated only with "Science", and a third Topic has no items  
When the user requests `GET /api/stats`  
Then "Science" has a count of 2, "Space" has a count of 1, and the empty Topic
has a count of 0  
And all Topics are present in descending-count, then ascending-name order.

**BDD-074 — Statistics request is logged**  
Given the collection is available  
When the user requests `GET /api/stats`  
Then a `stats.query` event records the request outcome  
And the event contains no user-authored names or notes.

**BDD-075 — Statistics processing failure**  
Given statistics processing fails unexpectedly  
When the user requests `GET /api/stats`  
Then the API returns HTTP 500 with the existing `ErrorResponse` shape  
And a `stats.query` event records the failure outcome.

## 6. Impact Analysis

| Component | Impact |
|---|---|
| `models` | Add response models for collection totals, distributions, rating aggregates, and `TopicStatItem`; existing domain/request models remain unchanged. |
| `services` | Add a read-only aggregation service over the existing repositories. It does not write or alter stored records. |
| `routes` | Add the `GET /api/stats` route. Existing routes, methods, parameters, status codes, and response schemas are unchanged. |
| `logging` | Emit `stats.query` with outcome/status and without user-authored content; retain existing request middleware logging. |
| `docs/openapi.yaml` | Add the `/stats` operation and `CollectionStatsResponse` / `TopicStatItem` schemas, with 200 and 500 responses. |
| Traceability matrices | Add links for REQ-F-070..074, AC-070..075, BDD-071..075, TEST-016, and FEAT-013; record the limited CON-013 exception. |

### Compatibility and Scope Amendment

This is an additive, read-only endpoint. Existing clients can continue using
all existing routes and payloads unchanged; no existing response is extended
or reinterpreted. The only approved scope change is a narrow exception to
CON-013 and AC-069 for locally computed collection statistics at
`GET /api/stats`. AC-069 remains applicable to every other excluded capability.
All other exclusions in CON-013 remain in force. This addendum is authoritative
for this feature where it supplements or narrowly supersedes SRS-001 v1.0; the
original AC-047..AC-052 definitions remain unchanged.

## 7. Traceability

| Requirement | Acceptance Criteria | BDD Scenarios | Tickets |
|---|---|---|---|
| REQ-F-070 | AC-070, AC-074 | BDD-071 | TEST-016, FEAT-013 |
| REQ-F-071 | AC-071, AC-074 | BDD-071, BDD-072 | TEST-016, FEAT-013 |
| REQ-F-072 | AC-072, AC-074 | BDD-071, BDD-072 | TEST-016, FEAT-013 |
| REQ-F-073 | AC-073 | BDD-073 | TEST-016, FEAT-013 |
| REQ-F-074 | AC-075 | BDD-074, BDD-075 | TEST-016, FEAT-013 |
