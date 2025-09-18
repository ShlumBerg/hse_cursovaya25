<template>
  <div>
    <n-config-provider :theme-overrides="themeOverrides">
      <n-message-provider>
        <n-dialog-provider>
          <RouterView />
        </n-dialog-provider>
      </n-message-provider>
    </n-config-provider>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import { NMessageProvider, NDialogProvider, NConfigProvider } from 'naive-ui';

const themeOverrides = {
    common: {
      primaryColor: '#1A62C1FF',
      primaryColorHover: '#1A62C1FF',
      primaryColorPressed: '#1A62C1FF',
      primaryColorSuppl: '#1A62C1FF',
    },
  }

</script>
