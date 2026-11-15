# Technology Stack Decision Record

**Project:** Personal Media Library System (PMLS)  
**Document ID:** TECH-STACK-001  
**Date:** 2026-11-15  
**Author:** Human (approved) / Agent (recorded)  
**Source:** SRS-001 v1.0, PEP-001, logs/api-gate-decision.md  
**Status:** APPROVED

---

## 1. Purpose

This record closes the two open human decisions that were blocking Phase 2 (Test Suite) and
Phase 3 (Feature Implementation) of PEP-001:

| Decision ID | Description | Blocked since |
|---|---|---|
| **HD-009** | Target operating system and deployment platform | SPEC-GATE (2026-10-04) |
| **HD-047** | Technology stack — language, framework, storage, test framework | SPEC-GATE (2026-10-04) |

Both decisions were explicitly left unresolved in `logs/spec-gate.md` §Open Human Decisions
and in `logs/api-gate-decision.md` §6 Open Items. This record constitutes the authoritative
resolution of both.

---

## 2. Decisions

### HD-009 — Target Platform

**Decision:** Cross-platform (Windows and Linux).  
**Rationale:** The developer works on Windows locally; CI/CD and any future deployment targets
Linux. The chosen stack (Python + FastAPI + file-based storage) is natively cross-platform with
no OS-specific dependencies. CON-012 (platform independence of the specification) is satisfied.

---

### HD-047 — Technology Stack

#### 2.1 Language and Runtime

| Attribute | Value |
|---|---|
| Language | Python |
| Minimum version | 3.11 |
| Rationale | Mature ecosystem for REST APIs, native `logging` stdlib, first-class support in FastAPI and pytest. 3.11 chosen for `tomllib` stdlib inclusion and improved error messages. |

#### 2.2 Web Framework

| Attribute | Value |
|---|---|
| Framework | FastAPI |
| ASGI server | Uvicorn |
| Rationale | Automatic OpenAPI/JSON Schema validation from Pydantic models aligns with the approved `docs/openapi.yaml` contract. Async-capable but usable synchronously. Native TestClient via `httpx`. |

#### 2.3 Data Validation

| Attribute | Value |
|---|---|
| Library | Pydantic v2 |
| Rationale | Bundled with FastAPI. Covers VR-001..011 at the schema layer with minimal boilerplate. |

#### 2.4 Storage (FEAT-012)

| Attribute | Value |
|---|---|
| Format | JSON file |
| Path | `data/media_store.json` |
| Rationale | REQ-NF-011 forbids prescribing a database. JSON file satisfies REQ-F-059..066 (auto-save, load on start, save-failure handling) with zero external dependencies. Human-readable for debugging. CON-009 (localhost only) makes network storage unnecessary. |
| Failure handling | On `IOError` / `OSError` during save: in-memory state is preserved; response includes `save_failed` error code per api-design-spec §3 (REQ-F-061). |

#### 2.5 Test Framework

| Attribute | Value |
|---|---|
| Test runner | pytest |
| HTTP test client | httpx (via `fastapi.testclient.TestClient`) |
| Rationale | Standard Python test ecosystem. `TestClient` runs the full ASGI stack in-process — no mock server required. Covers TEST-001..015 (Phase 2 of PEP-001). |

#### 2.6 Logging (REQ-NF-005..006)

| Attribute | Value |
|---|---|
| Library | Python stdlib `logging` |
| Output — file | `logs/system.log` (append, UTF-8) |
| Output — console | `stderr`, same format |
| Format | `%(asctime)s  %(levelname)-8s  %(name)s  %(message)s` |
| Rationale | No external dependency. REQ-NF-005 requires operational logging; REQ-NF-006 requires it to be non-intrusive. Stdlib `logging` satisfies both without adding a production dependency. |

#### 2.7 Linter / Formatter

| Attribute | Value |
|---|---|
| Tool | ruff |
| Rationale | Single binary replacing flake8 + isort + pyupgrade. Configured in `pyproject.toml` under `[tool.ruff]`. |

---

## 3. Impact on SRS Constraints

| Constraint | Requirement | Compliance |
|---|---|---|
| CON-008 | No authentication | FastAPI `security: []` — no auth dependency added |
| CON-009 | Localhost network | Uvicorn bound to `127.0.0.1` by default |
| CON-012 | Platform independence of specification | Python 3.11 runs on Windows and Linux without code changes |
| CON-013 | Scope ceiling | No feature outside SRS-001 is introduced by the stack choice |
| REQ-NF-011 | Specification platform-agnostic | Resolved by this decision; specification unchanged |

---

## 4. Artifacts Created by This Decision

| Artifact | Path |
|---|---|
| This decision record | `logs/tech-stack-decision.md` |
| Python dependencies | `requirements.txt` |
| Project configuration | `pyproject.toml` |
| VCS ignore rules | `.gitignore` |
| Source package skeleton | `src/routes/`, `src/validators/`, `src/services/`, `src/repository/`, `src/models/`, `src/errors/`, `src/logging/` |
| Logging component | `src/logging/logger.py` |
| Application entry point | `src/main.py` |

---

## 5. Unblocked Work Items

This decision unblocks:

| Phase | Ticket range | Description |
|---|---|---|
| Phase 2 | TEST-001..015 | Full test suite (all 15 tickets now have a known test framework) |
| Phase 3 | FEAT-001..012 | Feature implementation (stack and storage format confirmed) |

---

*End of TECH-STACK-001 Decision Record*
