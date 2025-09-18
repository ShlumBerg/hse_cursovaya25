<template>
  <header>
    <div class="flex justify-between">
      <NMenu
        :options="menuOptions"
        :value="currentMenuOption"
        mode="horizontal"
        @update-value="onMenuOptionChange"
      />
      <NButton :bordered="false" :focusable="false" ghost @click="logout">
        Выход
      </NButton>
    </div>
  </header>

  <div class="page">
    <h2 class="pb-4 text-lg">
      {{ currentPageTitle }}
    </h2>

    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue';
import { RouterView, useRouter, useRoute } from 'vue-router';
import { NButton, NMenu, type MenuOption } from 'naive-ui';
import { useUserStore } from '@/stores/user-store';

const userStore = useUserStore();

const menuOptions: MenuOption[] = [
  {
    "label": "Главная",
    "key": "home",
  },
  {
    "label": "Физические лица",
    "key": "fiz-litsa",
  },
  {
    "label": "Юридические лица",
    "key": "yur-litsa",
  },
  {
    "label": "Кредиты физ. лицам",
    "key": "fiz-litsa-credits",
  },
  {
    "label": "Кредиты юр. лицам",
    "key": "yur-litsa-credits",
  },
]

const router = useRouter();

const route = useRoute();

const currentMenuOption = ref<string | null>(null);

const currentPageTitle = computed(() => menuOptions?.find((o) => o.key == currentMenuOption.value)?.label);

onBeforeMount(() => {
  const currentRoute = route.name;
  currentMenuOption.value = currentRoute?.toString() || null;
})

function onMenuOptionChange(key: string, item: MenuOption) {
  currentMenuOption.value = key;
  router.push({
    name: key
  })
}

async function logout() {
  await userStore.logout()
  router.push({name: 'login'})
}

</script>


<style lang="css" scoped>
  .page {
    padding: 1rem;
  }
</style>