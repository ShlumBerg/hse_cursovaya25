<template>
    <div>
        <h2 class="mb-4">
            Кредит № {{ credit.uuid }} погашен!
        </h2>
        <div class="mb-4">
            Внесённая сумма ({{paymentAmount}} рублей) полностью погашает задолженности по процентам и телу кредита, а также пени.
        </div>
        <div class="mb-4">
            После полного погашения кредита останется сдача в размере {{remainder}} рублей.
        </div>
    </div>
</template>

<script setup lang="ts">
import { type Credit } from '@/api';

interface Props {
    credit: Credit;
    paymentAmount: number;
    remainder: number;
}

defineProps<Props>();

</script>