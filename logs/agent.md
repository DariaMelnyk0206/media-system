# Coding Agent — Project Log

**Recorded:** 2026-09-18  
**Project directory:** `C:\Users\Master\media-system`

---

## Tool Class

Kiro CLI default agent — an AI coding assistant run via the `kiro-cli chat` command in the user's terminal. Model selection is handled dynamically on the server (Auto mode).

---

## Repository Access

The agent operates directly inside the working directory (`C:\Users\Master\media-system`). It accesses the repository through a set of built-in tools:

- **Read** — reads file contents (line ranges) and lists directory trees.
- **Glob** — finds files by name pattern, respecting `.gitignore`.
- **Grep** — searches file contents with regex across the repository.
- **Code intelligence** — parses source files to find and inspect symbols, classes, and functions using AST analysis and fuzzy search.

No external repository hosting or remote API is used to read the codebase; all access is local and filesystem-based.

---

## Operations Available in This Environment

| Category | Operations |
|---|---|
| Files | Read, create, edit (string replace, insert), write new files |
| Search | Regex search across files, glob file discovery, symbol lookup |
| Shell | Execute shell commands (PowerShell / cmd.exe on Windows) |
| AWS | Call AWS CLI operations via the `use_aws` tool |
| Web | Fetch content from URLs, run web searches |
| Knowledge | Index and semantically search content across sessions |
| Orchestration | Spawn and coordinate sub-agents in parallel or sequential pipelines |

---

## Constraints

- Does not push to `main`/`master` or perform destructive git operations without explicit user permission.
- Does not transmit project code or secrets to third-party endpoints unless explicitly requested.
- Does not read or echo secret values (`.env`, credential files) without user permission.
- Confirms before taking high-risk or irreversible actions (production changes, data deletion, bulk operations).
