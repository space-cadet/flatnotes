<template>
  <nav class="mb-2 flex justify-between align-top md:mb-12">
    <RouterLink :to="{ name: 'home' }" v-if="!hideLogo">
      <Logo responsive></Logo>
    </RouterLink>
    <div class="flex grow items-start justify-end">
      <!-- New Note -->
      <RouterLink v-if="showNewButton" :to="{ name: 'new' }">
        <CustomButton :iconPath="mdilPlusCircle" label="New Note" />
      </RouterLink>
      <!-- Menu -->
      <CustomButton
        class="ml-1"
        :iconPath="mdilMenu"
        label="Menu"
        @click="toggleMenu"
      />
      <PrimeMenu ref="menu" :model="menuItems" :popup="true" />
    </div>
  </nav>
</template>

<script setup>
import {
  mdilLogin,
  mdilLogout,
  mdilMagnify,
  mdilMenu,
  mdilMonitor,
  mdilNoteMultiple,
  mdilPlusCircle,
} from "@mdi/light-js";
import { computed, ref, watch } from "vue";
import { RouterLink, useRouter } from "vue-router";

import CustomButton from "../components/CustomButton.vue";
import Logo from "../components/Logo.vue";
import PrimeMenu from "../components/PrimeMenu.vue";
import { authTypes, params, searchSortOptions } from "../constants.js";
import { useGlobalStore } from "../globalStore.js";
import { toggleTheme } from "../helpers.js";
import { clearStoredToken, getStoredToken } from "../tokenStorage.js";

const globalStore = useGlobalStore();
const menu = ref();
const router = useRouter();

defineProps({
  hideLogo: Boolean,
});

const emit = defineEmits(["toggleSearchModal"]);

const menuItems = computed(() => [
  {
    label: "Search",
    icon: mdilMagnify,
    command: () => emit("toggleSearchModal"),
    keyboardShortcut: "/",
  },
  {
    label: "All Notes",
    icon: mdilNoteMultiple,
    command: () =>
      router.push({
        name: "search",
        query: {
          [params.searchTerm]: "*",
          [params.sortBy]: searchSortOptions.title,
        },
      }),
  },
  {
    label: "Toggle Theme",
    icon: mdilMonitor,
    command: toggleTheme,
  },
  {
    separator: true,
    visible: globalStore.authRequired,
  },
  globalStore.isAuthenticated
    ? {
        label: "Log Out",
        icon: mdilLogout,
        command: logOut,
        visible: globalStore.authRequired,
      }
    : {
        label: "Log In",
        icon: mdilLogin,
        command: logIn,
        visible: globalStore.authRequired,
      },
]);

const showNewButton = computed(() => {
  // Only show New Note button if auth is not required or user is authenticated
  if (globalStore.authRequired && !globalStore.isAuthenticated) {
    return false;
  }
  return globalStore.config.authType !== authTypes.readOnly;
});

function logIn() {
  router.push({
    name: "login",
    query: { [params.redirect]: router.currentRoute.value.fullPath },
  });
}

function logOut() {
  clearStoredToken();
  localStorage.clear();
  globalStore.setAuthenticated(false);
  router.push({ name: "home" });
}

function toggleMenu(event) {
  menu.value.toggle(event);
}
</script>
