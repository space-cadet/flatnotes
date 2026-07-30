<template>
  <div ref="viewerElement"></div>
</template>

<script setup>
import Viewer from "@toast-ui/editor/dist/toastui-editor-viewer";
import { onMounted, ref, watch } from "vue";
import katex from "katex";
import "katex/dist/katex.min.css";

import baseOptions from "./baseOptions.js";
import extendedAutolinks from "./extendedAutolinks.js";

const props = defineProps({
  initialValue: String,
});

const viewerElement = ref();
let toastViewer = null;

/**
 * Unicode-safe base64 encode
 */
function utf8ToBase64(str) {
  return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, (match, p1) =>
    String.fromCharCode("0x" + p1)
  ));
}

/**
 * Unicode-safe base64 decode
 */
function base64ToUtf8(str) {
  return decodeURIComponent(
    atob(str)
      .split("")
      .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
      .join("")
  );
}

/**
 * Extract math blocks from markdown and replace with HTML placeholders.
 * Toast UI passes HTML spans through unchanged, so we can render math
 * with KaTeX after Toast UI finishes.
 * 
 * This avoids Toast UI's markdown parser mangling LaTeX backslashes
 * inside $$...$$ blocks (it bizarrely inserts spaces: \alpha -> \ alpha).
 */
function preprocessMath(markdown) {
  if (!markdown) return markdown;

  // Process $$...$$ block math FIRST
  let result = markdown.replace(/\$\$([\s\S]*?)\$\$/g, (match, math) => {
    const encoded = utf8ToBase64(math);
    return `<span class="math-placeholder" data-display="block" data-math="${encoded}"></span>`;
  });

  // Then process $...$ inline math
  // Match $...$ where ... doesn't contain $ or newline
  result = result.replace(/\$([^\$\n]+?)\$/g, (match, math) => {
    const encoded = utf8ToBase64(math);
    return `<span class="math-placeholder" data-display="inline" data-math="${encoded}"></span>`;
  });

  return result;
}

function renderMath() {
  if (!viewerElement.value) return;

  const placeholders = viewerElement.value.querySelectorAll(".math-placeholder");
  placeholders.forEach((el) => {
    const encoded = el.getAttribute("data-math");
    const display = el.getAttribute("data-display");
    if (!encoded) return;

    try {
      const math = base64ToUtf8(encoded);
      const html = katex.renderToString(math, {
        displayMode: display === "block",
        throwOnError: false,
      });
      el.outerHTML = html;
    } catch (e) {
      // If KaTeX fails, show raw math
      el.textContent = display === "block" ? `$$${base64ToUtf8(encoded)}$$` : `$${base64ToUtf8(encoded)}$`;
    }
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
  // Render math after Toast UI has rendered the markdown
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
