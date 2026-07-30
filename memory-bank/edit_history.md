# Edit History

*Created: 2026-07-30 16:53:12 UTC*
*Last Updated: 2026-07-30 19:18:00 IST*

---

## 2026-07-30

### 19:08 - 19:18 IST - T2: Fixed pmatrix and complex math (final fix)
- **Root cause**: Toast UI's markdown parser inserts spaces after backslashes inside `$$...$$` blocks (`\alpha` → `\ alpha`)
- **Solution**: Complete rewrite of math handling — extract math blocks before Toast UI, replace with HTML placeholders, render with KaTeX after
- **Files changed**:
  - `client/components/toastui/ToastViewer.vue` — replaced double-escape approach with placeholder extraction (59 insertions, 45 deletions)
- **Implementation details**: See `implementation-details/latex-math-rendering.md`
- **Verified**: Inline math, block math, integrals, Greek letters, pmatrix matrices all working
- **Deployed**: quantumofgravity.com/notes/
- **Commit**: `153719e`

### 18:08 - 18:37 IST - T2: Add LaTeX Math Support
- Added KaTeX v0.16.23 dependency
- Modified 3 files for client-side math rendering
- Built and deployed to quantumofgravity.com/notes/
- Server restarted successfully
- **Fixed backslash escaping bug**: Toast UI's markdown parser strips backslashes from LaTeX commands (e.g., `\int` → `int`)

#### Files Changed
- `package.json`: Added `katex` dependency
- `client/components/toastui/ToastViewer.vue`: Added KaTeX auto-render hook (import CSS, call renderMathInElement after mount, watcher on initialValue); Added `preprocessMath()` helper to double-escape backslashes inside math blocks before Toast UI processing; Recreate viewer on content changes
- `client/components/toastui/ToastEditor.vue`: Added KaTeX CSS import

#### Technical Details
- Uses KaTeX auto-render for post-processing rendered HTML
- Supports `$...$` inline and `$$...$$` block delimiters
- throwOnError: false for graceful failure handling
- **Backslash fix**: Pre-processes math blocks to double-escape backslashes (`\` → `\\`) before passing to Toast UI; Toast UI's `to-mark` parser converts `\\` back to `\`, preserving original LaTeX commands
- No server changes required
- Test note created: `latex-test.md`

### 13:33 - 16:46 UTC - T1: Per-note visibility feature implementation
- Created fork: github.com/space-cadet/flatnotes
- Branch: feature/per-note-visibility
- Modified 12 files (+410/-282 lines)
- Deployed to quantumofgravity.com/notes/
- Added login: deepak / ***
- **Implementation details**: See `implementation-details/per-note-visibility.md`

#### Backend Changes
- server/global_config.py: Added Visibility enum
- server/notes/models.py: Added visibility field to Note models
- server/notes/file_system/file_system.py: YAML frontmatter parsing
- server/main.py: Conditional auth per note
- Pipfile: Added python-frontmatter dependency

#### Frontend Changes
- client/views/Note.vue: Visibility toggle UI
- client/router.js: Removed global auth guards (public-first homepage)
- client/globalStore.js: Added isAuthenticated state
- client/partials/NavBar.vue: Login/Logout menu items
- client/classes.js: Added visibility property
- client/constants.js: Added visibility enum
- client/api.js: Send visibility in create/update

### 16:53:12 UTC - INIT: Memory bank initialized
- Created `memory-bank/` directory structure
- Initialized core files (tasks.md, session_cache.md, etc.)
- Set up database parser scripts and viewer
