<template>
  <div ref="viewerElement"></div>
</template>

<script setup>
import Viewer from "@toast-ui/editor/dist/toastui-editor-viewer";
import { onMounted, ref, watch } from "vue";
import renderMathInElement from "katex/dist/contrib/auto-render";
import "katex/dist/katex.min.css";

import baseOptions from "./baseOptions.js";
import extendedAutolinks from "./extendedAutolinks.js";

const props = defineProps({
  initialValue: String,
});

const viewerElement = ref();
let toastViewer = null;

/**
 * Pre-process markdown to preserve LaTeX backslashes.
 * Toast UI's markdown parser strips backslashes from unknown escapes,
 * which breaks LaTeX commands like \int, \sum, etc.
 * We double-escape backslashes inside math blocks so that when
 * Toast UI converts \\ -> \, the original LaTeX commands are preserved.
 */
function preprocessMath(markdown) {
  if (!markdown) return markdown;

  const parts = [];
  let i = 0;

  while (i < markdown.length) {
    // Check for $$ (block math)
    if (markdown.slice(i, i + 2) === "$$") {
      const end = markdown.indexOf("$$", i + 2);
      if (end !== -1) {
        const math = markdown.slice(i + 2, end);
        // Double backslashes inside math
        const processed = math.replace(/\\/g, "\\\\");
        parts.push("$$" + processed + "$$");
        i = end + 2;
        continue;
      }
    }

    // Check for $ (inline math) — avoid matching $ inside $$
    if (markdown[i] === "$" && markdown[i + 1] !== "$") {
      const end = markdown.indexOf("$", i + 1);
      if (end !== -1 && markdown[end + 1] !== "$") {
        const math = markdown.slice(i + 1, end);
        // Double backslashes inside math
        const processed = math.replace(/\\/g, "\\\\");
        parts.push("$" + processed + "$");
        i = end + 1;
        continue;
      }
    }

    parts.push(markdown[i]);
    i++;
  }

  return parts.join("");
}

function renderMath() {
  if (!viewerElement.value) return;
  renderMathInElement(viewerElement.value, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
    ],
    throwOnError: false,
  });
}

function createViewer(content) {
  if (toastViewer) {
    toastViewer.destroy();
  }
  toastViewer = new Viewer({
    ...baseOptions,
    extendedAutolinks,
    el: viewerElement.value,
    initialValue: preprocessMath(content),
  });
  renderMath();
}

onMounted(() => {
  createViewer(props.initialValue);
});

watch(() => props.initialValue, (newValue) => {
  createViewer(newValue);
});
</script>

<style>
@import "@toast-ui/editor/dist/toastui-editor-viewer.css";
@import "prismjs/themes/prism.css";
@import "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight.css";
@import "./toastui-editor-overrides.scss";
</style>
