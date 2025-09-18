<template>
    <div>
        <h2 class="text-lg mb-4">
            {{ title }}
        </h2>

        <div>
            При списании кредита, данные о нём удалятся из базы.
        </div>
        <div>
            На данный момент, за этот кредит должник должен:
        </div>
        <div>
            По базе кредита: {{ credit?.credit_statistics?.unpaidbase }} рублей
        </div>
        <div>
            По процентам: {{ credit?.credit_statistics?.unpaidpercents }} рублей
        </div>
        <div>
            По пеням: {{ credit?.credit_statistics?.unpaidpennies }} рублей
        </div>
        <div>
            Всего: {{ credit?.credit_statistics?.currentlyunpaid }} рублей
        </div>

        <div class="mt-4">
            Вы действительно хотите списать данный кредит?
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Credit } from '@/api';

interface Props {
    credit: Credit;
}

const props = defineProps<Props>();

const title = computed(() => {
    if (props.credit?.ur_client) {
        return `Списание кредита № ${props.credit.uuid} юридическому лицу (ОГРН ${props.credit.ogrn})`

    } else {
        return `Списание кредита № ${props.credit.uuid} физическому лицу (паспорт ${props.credit.passport})`
    }
})

</script>