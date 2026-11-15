# Personal Media Library System

PMLS is a local REST API for managing a personal media collection. It supports
MediaItems and Topics, their many-to-many associations, ratings and status,
search, filtering, sorting, automatic JSON persistence, and read-only collection
statistics. The application does not require network access or an external
service.

## Features

- Create, view, edit, and delete MediaItems and Topics.
- Associate MediaItems and Topics from either side.
- Search names, filter MediaItems, and sort results.
- Automatically persist changes and report save failures using a consistent
  `ErrorResponse`.
- Return collection totals, status/type distributions, rated-item statistics,
  and sorted Topic counts from `GET /api/stats`.

## Requirements and Setup

Python 3.11 or later is required. From the repository root, create and
populate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the API

```powershell
.\.venv\Scripts\uvicorn.exe src.main:app --reload
```

The API is served at `http://127.0.0.1:8000/api`. Interactive OpenAPI
documentation is available at `http://127.0.0.1:8000/docs`; the OpenAPI
contract is maintained in [`docs/openapi.yaml`](docs/openapi.yaml).

## REST API

All paths below are relative to the `/api` prefix. The API has 16 operations:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/media-items` | List MediaItems; supports filtering and sorting |
| `POST` | `/media-items` | Create a MediaItem |
| `GET` | `/media-items/{id}` | Get a MediaItem |
| `PATCH` | `/media-items/{id}` | Update a MediaItem |
| `DELETE` | `/media-items/{id}` | Delete a MediaItem |
| `POST` | `/media-items/{id}/topics/{topicId}` | Associate a Topic with a MediaItem |
| `DELETE` | `/media-items/{id}/topics/{topicId}` | Remove that association |
| `GET` | `/topics` | List Topics |
| `POST` | `/topics` | Create a Topic |
| `GET` | `/topics/{id}` | Get a Topic and its associated MediaItems |
| `PATCH` | `/topics/{id}` | Rename a Topic |
| `DELETE` | `/topics/{id}` | Delete a Topic |
| `POST` | `/topics/{id}/media-items/{mediaId}` | Associate a MediaItem with a Topic |
| `DELETE` | `/topics/{id}/media-items/{mediaId}` | Remove that association |
| `GET` | `/search?q={query}` | Search MediaItem and Topic names |
| `GET` | `/stats` | Get read-only collection statistics |

`GET /stats` reports total MediaItems and Topics, counts for every supported
status and media type, the rounded average of non-null ratings and rated count,
and per-Topic distinct MediaItem counts. Topic summaries sort by descending
count and then case-insensitive name. An empty collection returns zero counts,
`average_rating: null`, and an empty Topic summary.

## Architecture

The implementation separates HTTP handling, business logic, and persistence:

| Component | Responsibility |
|---|---|
| `src/models/` | Domain and Pydantic request/response models |
| `src/errors/` | Unified error codes, `ErrorResponse`, and exception handlers |
| `src/validators/` | Input validation and normalization rules |
| `src/repository/` | Collection access and JSON storage operations |
| `src/services/` | Business operations and aggregation over repositories |
| `src/routes/` | FastAPI endpoints; delegates application work to services |
| `src/logging/` | Application logging configuration and helpers |
| `src/main.py` | Application setup, router registration, and request middleware |

The default JSON store is `data/media_store.json`; application events are
written to `logs/system.log`.

## Tests and Lint

Run the complete unit and OpenAPI contract test suite:

```powershell
.\.venv\Scripts\pytest.exe tests\ --tb=short -q
```

Run Ruff over the implementation and tests:

```powershell
.\.venv\Scripts\ruff.exe check src\ tests\
```

## Project Documentation

- [Software Requirements Specification](spec/srs.md)
- [Collection Statistics Addendum](spec/addendum-001-collection-stats.md)
- [Requirements traceability matrix](spec/traceability.md)
- [Project traceability and work-item status](docs/TRACEABILITY.md)
- [Work-item decomposition](docs/jira-decomposition.csv)
- [OpenAPI contract](docs/openapi.yaml)
