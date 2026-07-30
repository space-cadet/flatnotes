# Project Brief
*Last Updated: 2026-07-30 16:55:00 UTC*

## Project Overview
**Project Name**: flatnotes-fork (per-note visibility)
**Description**: Fork of dullage/flatnotes adding per-note public/private visibility using YAML frontmatter

## Objectives
1. Allow some notes to be publicly readable without authentication
2. Keep other notes private (require login)
3. Maintain compatibility with upstream flatnotes
4. Submit PR to upstream project

## Key Features
- YAML frontmatter parsing for visibility metadata
- Conditional auth: public notes readable without auth
- Search filters results by authentication status
- Visibility toggle in note editor
- Public-first homepage (no forced login redirect)

## Tech Stack
- **Language**: Python 3 (backend), JavaScript/Vue (frontend)
- **Backend**: FastAPI, Whoosh (full-text search)
- **Frontend**: Vue 3, Vite, Toast UI Editor
- **Dependencies**: python-frontmatter, whoosh, pydantic

## Constraints & Requirements
- Must work with existing flatnotes data (backward compatible)
- Private notes default to no frontmatter (clean markdown files)
- Public notes get `--- visibility: public ---` frontmatter
- Index schema version bumped (auto-rebuild on first run)

## Success Metrics
- Public notes accessible without auth
- Private notes require auth
- Search correctly filters by visibility
- UI toggle works in editor
- Existing notes remain private by default

## Repository
**Fork**: https://github.com/space-cadet/flatnotes
**Upstream**: https://github.com/dullage/flatnotes
**Branch**: feature/per-note-visibility

## Team/Contributors
- space-cadet: Feature implementation
