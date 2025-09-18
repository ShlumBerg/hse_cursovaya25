<template>
    <n-card
        :title="title"
        :bordered="false"
        size="small"
        role="dialog"
        aria-modal="true"
    >
        <div class="mb-4">
            <div>
                Внесённые средства погашают выплаты по кредиту в следующем порядке:
            </div>
            <ul class="text-justify ml-4" style="list-style: decimal;">
                <li>задолженность по процентам</li>
                <li>задолженность по основному долгу</li>
                <li>проценты, начисленные за текущий период платежей</li>
                <li>сумма основного долга за текущий период платежей</li>
                <li>пеня</li>
                <li>досрочное погашение базы кредита</li>
            </ul>
        </div>

        <n-form ref="payoffFormRef" size="small" :model="payoffForm" :rules="payoffFormRules" class="w-full">
            <n-form-item path="total" label="Сумма для погашения кредита">
                <n-input-number v-model:value="payoffForm.total" min="0" size="small" placeholder="Введите значение" class="w-full" @keydown.enter.prevent />
            </n-form-item>

            <div class="flex justify-end">
                <n-button type="info" @click="submit">
                    Внести плату
                </n-button>
            </div>
        </n-form>
    </n-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { NButton, NCard, NForm, NFormItem, NInputNumber, type FormItemRule, type FormValidationError } from 'naive-ui';
import type { Credit, CreditPayoffRequest } from '@/api';

interface Props {
    credit: Credit;
    clientType: 'ur' | 'fiz';
}

const props = defineProps<Props>();

const emit = defineEmits<{
    submit: [total: number];
}>();

const payoffFormRef = ref();

const payoffForm = ref<{total: number | null}>({
    total: null,
});

const payoffFormRules = {
    totalPayment: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
};

const title = computed(() => {
    switch (props.clientType) {
        case 'ur':
            return `Погашение выплат по кредиту № ${props.credit.uuid} юридическому лицу (ОГРН ${props.credit.ogrn})`
        case 'fiz':
            return `Погашение выплат по кредиту № ${props.credit.uuid} физическому лицу (паспорт ${props.credit.passport})`
        default:
            break;
    }
})

function submit(e: MouseEvent) {
    e.preventDefault()
    payoffFormRef.value?.validate((errors: Array<FormValidationError> | undefined) => {
        if (!errors) {
            if (payoffForm.value.total) {
                emit('submit', payoffForm.value.total)

            }
        }
    })
}

</script>
