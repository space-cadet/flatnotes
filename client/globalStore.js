import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useGlobalStore = defineStore("global", () => {
  const config = ref({});
  const isAuthenticated = ref(false);

  const authRequired = computed(() => {
    return config.value.authType && config.value.authType !== "none" && config.value.authType !== "read_only";
  });

  function setAuthenticated(value) {
    isAuthenticated.value = value;
  }

  return { config, isAuthenticated, authRequired, setAuthenticated };
});
