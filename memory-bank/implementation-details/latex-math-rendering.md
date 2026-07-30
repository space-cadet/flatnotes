# Implementation Detail: LaTeX Math Rendering with KaTeX

## Overview
Added KaTeX-based LaTeX math rendering to flatnotes. Supports inline math (`$...$`) and block math (`$$...$$`) delimiters. The implementation works around Toast UI Editor's markdown parser which corrupts backslash sequences inside math blocks.

## The Problem

Toast UI Editor's markdown parser (`to-mark`) has a bizarre bug: inside `$$...$$` blocks, it **inserts a space after every backslash before a letter**:

| Input | Toast UI Output |
|-------|----------------|
| `\alpha` | `\ alpha` |
| `\begin` | `\ begin` |
| `\int` | `\ int` |

This breaks ALL LaTeX commands in block math. The behavior only occurs inside `$$...$$` delimiters — regular text handles backslashes correctly.

### Failed Approaches

**Approach 1: Double-escaping**
- Pre-process: replace `\` with `\\` inside math blocks
- Toast UI would convert `\\` → `\` during rendering
- **Failed**: Toast UI processes `\alpha` and `\\alpha` identically inside `$$...$$`

**Approach 2: KaTeX auto-render on rendered HTML**
- Let Toast UI render markdown normally
- Run `renderMathInElement()` to find `$...$` / `$$...$$` in output HTML
- **Failed**: Toast UI's mangled output (`\ alpha`) is invalid LaTeX

## The Solution: Placeholder Extraction

### Architecture

```
Raw Markdown → preprocessMath() → Toast UI → renderMath() → Final HTML
                    ↓                                      ↓
            Extract math, inject            Find placeholders,
            HTML <span> placeholders        render with KaTeX
```

### Step 1: Extract Math Blocks
**File:** `client/components/toastui/ToastViewer.vue`

```javascript
function preprocessMath(markdown) {
  // Process $$...$$ block math FIRST (greedy match)
  let result = markdown.replace(/\$\$([\s\S]*?)\$\$/g, (match, math) => {
    const encoded = utf8ToBase64(math);
    return `<span class="math-placeholder" data-display="block" data-math="${encoded}"></span>`;
  });

  // Then process $...$ inline math
  result = result.replace(/\$([^\$\n]+?)\$/g, (match, math) => {
    const encoded = utf8ToBase64(math);
    return `<span class="math-placeholder" data-display="inline" data-math="${encoded}"></span>`;
  });

  return result;
}
```

**Why base64?**
- Math may contain characters that break HTML/regex parsing (`<`, `>`, `"`, `&`)
- Base64 ensures the math content survives Toast UI's rendering pipeline unchanged
- Uses Unicode-safe base64 (handles non-ASCII via `encodeURIComponent`)

### Step 2: Toast UI Renders Markdown
Toast UI processes the markdown normally. The `<span class="math-placeholder">` elements are passed through unchanged because:
- They're valid HTML spans
- No markdown syntax inside them (just base64 strings)
- Toast UI's HTML sanitizer allows `span` with `data-*` attributes

### Step 3: KaTeX Renders Math
**File:** `client/components/toastui/ToastViewer.vue`

```javascript
function renderMath() {
  const placeholders = viewerElement.value.querySelectorAll(".math-placeholder");
  placeholders.forEach((el) => {
    const encoded = el.getAttribute("data-math");
    const display = el.getAttribute("data-display");
    
    const math = base64ToUtf8(encoded);
    const html = katex.renderToString(math, {
      displayMode: display === "block",
      throwOnError: false,
    });
    el.outerHTML = html;
  });
}
```

## File Changes

### `client/components/toastui/ToastViewer.vue`
- Imported `katex` (direct import, not auto-render)
- Added `utf8ToBase64()` / `base64ToUtf8()` helpers
- Rewrote `preprocessMath()` to extract math and inject placeholders
- Added `renderMath()` to replace placeholders with KaTeX output
- Called `renderMath()` after Toast UI viewer creation

### `client/components/toastui/ToastEditor.vue`
- Added `import "katex/dist/katex.min.css"` for editor preview styling

### `package.json`
- Added `"katex": "^0.16.23"` to dependencies

## Build Output

- KaTeX fonts bundled in `dist/assets/` (29 font files, ~1.7MB total)
- Math rendering code in `Note-*.js` chunk
- CSS inlined in main bundle

## Supported Syntax

| Type | Delimiters | Example |
|------|-----------|---------|
| Inline math | `$...$` | `$E = mc^2$` |
| Block math | `$$...$$` | `$$\int_{-\infty}^{\infty} e^{-x^2} dx$$` |

## Verified Examples

- ✅ `$E = mc^2$` — inline equation
- ✅ `$\alpha + \beta = \gamma$` — Greek letters
- ✅ `$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$` — integrals
- ✅ `$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$` — summations
- ✅ `$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$$` — matrices (the bug that was broken)

## Error Handling

- `throwOnError: false` — invalid LaTeX shows raw source instead of crashing
- If base64 decode fails, falls back to showing raw math delimiters

## Known Limitations

- **Editor preview**: Shows raw LaTeX syntax while editing (math renders on save/view)
- **No equation numbering**: KaTeX doesn't support `\eqref` or automatic numbering
- **No macro definitions**: `\newcommand` not supported
- **Single-dollar edge cases**: `$100 vs $50` could be misinterpreted — use spaces around math delimiters

## Deployment

- Commit: `153719e` on `feature/per-note-visibility`
- Live: `https://quantumofgravity.com/notes/`
- Test note: `https://quantumofgravity.com/notes/note/latex-test`

## Future Improvements

- [ ] Add equation numbering support (via KaTeX contrib or custom)
- [ ] Render math in editor preview mode (real-time)
- [ ] Support additional delimiters (`\(...\)`, `\[...\]`)
- [ ] Add copy-LaTeX button on rendered math
