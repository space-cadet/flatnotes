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

onMounted(() => {
  new Viewer({
    ...baseOptions,
    extendedAutolinks,
    el: viewerElement.value,
    initialValue: props.initialValue,
  });
  // Render KaTeX math after viewer mounts
  renderMath();
});

watch(() => props.initialValue, () => {
  // Re-render math when content changes
  renderMath();
});
</script>

<style>
@import "@toast-ui/editor/dist/toastui-editor-viewer.css";
@import "prismjs/themes/prism.css";
@import "@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight.css";
@import "./toastui-editor-overrides.scss";
</style>
