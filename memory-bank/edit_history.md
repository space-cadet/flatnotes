# Edit History

*Created: 2026-07-30 16:53:12 UTC*
*Last Updated: 2026-07-30 18:25:00 IST*

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

### 18:08 - 18:24 IST - T2: Add LaTeX Math Support
- Added KaTeX v0.16.23 dependency
- Modified 3 files for client-side math rendering
- Built and deployed to quantumofgravity.com/notes/
- Server restarted successfully

#### Files Changed
- `package.json`: Added `katex` dependency
- `client/components/toastui/ToastViewer.vue`: Added KaTeX auto-render hook (import CSS, call renderMathInElement after mount, watcher on initialValue)
- `client/components/toastui/ToastEditor.vue`: Added KaTeX CSS import

#### Technical Details
- Uses KaTeX auto-render for post-processing rendered HTML
- Supports `$...$` inline and `$$...$$` block delimiters
- throwOnError: false for graceful failure handling
- No server changes required
- Test note created: `latex-test.md`
