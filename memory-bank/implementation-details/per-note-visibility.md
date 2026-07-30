# Implementation Detail: Per-Note Public/Private Visibility

## Overview
Added per-note visibility controls to flatnotes, allowing individual notes to be marked as public (readable without auth) or private (requires authentication). Previously, flatnotes auth was global — all-or-nothing.

## Architecture

### Backend (Python/FastAPI)

#### 1. Visibility Enum
**File:** `server/global_config.py`

```python
class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
```

#### 2. YAML Frontmatter Parsing
**File:** `server/notes/file_system/file_system.py`

Notes store visibility in YAML frontmatter:
```markdown
---
title: My Note
visibility: public
last_modified: 2026-07-30T12:00:00
---

# Note content...
```

- On read: Parse frontmatter, extract `visibility` field (default: `private`)
- On write: Include `visibility` in frontmatter
- Whoosh index schema bumped from v5 → v6 to include `visibility` field

#### 3. Conditional Auth
**File:** `server/main.py`

```python
def get_note(title: str, request: Request):
    note = note_storage.get(title)
    if note.visibility == Visibility.PRIVATE and not _is_authenticated(request):
        raise HTTPException(status_code=401, detail="Authentication required")
    return note
```

- Public notes: accessible without auth
- Private notes: require valid JWT token
- Search: Unauthenticated users only see public results

### Frontend (Vue.js)

#### 1. Data Models
**Files:** `client/classes.js`, `client/constants.js`

Added `visibility` property to Note class and API constants.

#### 2. Visibility Toggle UI
**File:** `client/views/Note.vue`

- Toggle switch in note editor (public/private)
- Visual indicator on note cards (lock icon for private)
- Visibility passed in create/update API calls

#### 3. Auth State Management
**File:** `client/globalStore.js`

Added `isAuthenticated` reactive state:
- Checked on app mount via `/api/auth-check`
- Controls visibility of login/logout menu items
- Determines if private notes should be fetched

#### 4. Public-First Homepage
**File:** `client/router.js`

Removed global auth guards — no forced redirect to login. Users see public notes immediately. Login link available in NavBar.

#### 5. NavBar Updates
**File:** `client/partials/NavBar.vue`

- Added Login/Logout menu items
- Shows user state (authenticated vs anonymous)
- No forced login redirect

## API Changes

### GET /api/notes/{title}
Now returns 401 for private notes if unauthenticated. Previously returned note regardless.

### GET /api/search
Unauthenticated users receive only public notes. Authenticated users see all.

### POST /api/notes
Accepts `visibility` field in request body.

### PATCH /api/notes/{title}
Accepts `visibility` field in request body.

## Deployment Notes

- Fork: `github.com/space-cadet/flatnotes`
- Branch: `feature/per-note-visibility`
- Deployed: `https://quantumofgravity.com/notes/`
- Apache ProxyPass: `/notes/` → `http://127.0.0.1:8089/notes/`
- Server env: `FLATNOTES_AUTH_TYPE=password`, `FLATNOTES_PATH_PREFIX=/notes`

## Security Considerations

- Frontmatter is parsed server-side — users cannot forge visibility by editing raw markdown
- Auth check happens BEFORE note content is returned
- Search index filters at query time, not post-processing
- Default visibility is `private` (safe-by-default)

## Future Work

- [ ] UI polish: visibility toggle styling, login-required messages
- [ ] Full browser testing of public/private flow
- [ ] PR submission to upstream `dullage/flatnotes`
