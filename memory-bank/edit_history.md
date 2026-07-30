# Edit History

*Created: 2026-07-30 16:53:12 UTC*
*Last Updated: 2026-07-30 16:55:00 UTC*

---

## 2026-07-30

### 16:53:12 UTC - INIT: Memory bank initialized
- Created `memory-bank/` directory structure
- Initialized core files (tasks.md, session_cache.md, etc.)
- Set up database parser scripts and viewer

### 13:33 - 16:46 UTC - T1: Per-note visibility feature implementation
- Created fork: github.com/space-cadet/flatnotes
- Branch: feature/per-note-visibility
- Modified 12 files (+410/-282 lines)
- Deployed to quantumofgravity.com/notes/
- Added login: deepak / ***

#### Backend Changes
- server/global_config.py: Added Visibility enum
- server/notes/models.py: Added visibility field to Note models
- server/notes/file_system/file_system.py: YAML frontmatter parsing
- server/main.py: Conditional auth per note
- Pipfile: Added python-frontmatter dependency

#### Frontend Changes
- client/classes.js: Added visibility property
- client/constants.js: Added visibility enum
- client/api.js: Updated create/update note APIs
- client/views/Note.vue: Visibility toggle in editor
- client/router.js: Removed forced login redirect
- client/globalStore.js: Added auth state tracking
- client/partials/NavBar.vue: Login/Logout menu items
