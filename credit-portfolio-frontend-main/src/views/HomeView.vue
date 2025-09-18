<template>
    <div>
        Здравствуйте, {{ userStore.user?.username }}!
    </div>
</template>


<script setup lang="ts">
import { useUserStore } from '@/stores/user-store';

const userStore = useUserStore();

</script>
