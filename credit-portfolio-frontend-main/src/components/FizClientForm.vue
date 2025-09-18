<template>
    <n-form ref="formRef" size="small" :model="clientForm" :rules="rules">
        <n-form-item v-if="mode == 'create'" path="passport" label="Паспорт">
            <n-input size="small" v-model:value="clientForm.passport" placeholder="Введите значение" @keydown.enter.prevent />
        </n-form-item>

        <n-row :gutter="[16,0]">
            <n-col v-for="formField in requiredFormFields" :key="formField.formValue" :span="6">
                <n-form-item :path="formField.formValue" :label="formField.label">
                    <NInputNumber :show-button="false" size="small" v-model:value="clientForm[formField.formValue]" placeholder="Введите значение" @keydown.enter.prevent class="w-full" />
                </n-form-item>
            </n-col>
        </n-row>

        <n-row :gutter="[16,0]">
            <n-col v-for="formField in nonRequiredFormFields" :key="formField.formValue" :span="6">
                <n-form-item :path="formField.formValue" :label="formField.label">
                    <NInputNumber :show-button="false" size="small" v-model:value="clientForm[formField.formValue]" placeholder="Введите значение" @keydown.enter.prevent class="w-full" />
                </n-form-item>
            </n-col>
        </n-row>

        <n-button type="info" @click="submit">
            {{ mode == 'create' ? 'Создать' : 'Сохранить' }}
        </n-button>
    </n-form>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import {
    NButton, NInput, NInputNumber, NRow, NCol, NForm, NFormItem,
    type FormRules, type FormItemRule, type FormValidationError,
} from 'naive-ui';
import type { FizClientRequest, PatchedFizClientRequest, FizClient } from '@/api';

interface Props {
    mode: 'create' | 'update';
    client?: FizClient;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    submit: [data: FizClientRequest];
}>();

const formRef = ref();

const clientForm = ref<FizClientRequest | PatchedFizClientRequest>({
    passport: null,
    annualinc: null,
    avgcurbal: null,
    totalacc: null,
    accopenpast24mths: null,
    totalbclimit: null,
    totalilhighcreditlimit: null,
    totalilrevhilim: null,
    emplength: null,
    totalbalexmort: null,
    bcopentobuy: null,

    nbkiRating: null,
    okbRating: null,
    bkiCreditInfoRating: null,
    bkiSBRating: null,
    dti: null,
    revolbal: null,
    mthssincerecentbc: null,
    bcutil: null,
    revolutil: null,
})

const regexNonNegativeFloat=/^[1-9][0-9]{0,9}(\.[0-9]{1,2})?$|^0$|^0\.[0-9]{1,2}$/
const regexNonNegativeSmallInt=/^[1-9][0-9]{0,2}$|^0$/

const smallIntNonNullRule = {
    required: true,
    validator(rule: FormItemRule, value: string) {
        if (!regexNonNegativeSmallInt.test(value)) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const empLengthRule = {
    required: true,
    validator(rule: FormItemRule, value: string) {
        if (!/^[1-9][0-9]{0,1}$|^0$/.test(value)) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const floatNonNullRule = {
    required: true,
    validator(rule: FormItemRule, value: string) {
        if (!regexNonNegativeFloat.test(value)) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};


const percentRule = {
    required: true,
    validator(rule: FormItemRule, value: string) {
        if (!value) {
            return true
        }
        else if (!(/^(([1-9][0-9]{0,1})|(0))(\.[0-9]{1,2})?$|^100$/.test(value))) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const ratingsRule = {
    required: false,
    validator(rule: FormItemRule, value: string) {
        if (!value) {
            return true
        }
        else if (!(/^[1-9][0-9]{0,2}$/.test(value))) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const smallIntNullRule = {
    required: false,
    validator(rule: FormItemRule, value: string) {
        if (!value) {
            return true
        }
        else if (!(regexNonNegativeSmallInt.test(value))) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const rules: FormRules = {
    passport: {required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(/^[0-9]{10}$/.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
    annualinc: floatNonNullRule,
    avgcurbal: floatNonNullRule,
    totalacc: smallIntNonNullRule,
    accopenpast24mths: smallIntNonNullRule,
    totalbclimit: floatNonNullRule,
    totalilhighcreditlimit: floatNonNullRule,
    totalilrevhilim: floatNonNullRule,
    emplength: empLengthRule,
    totalbalexmort: floatNonNullRule,
    bcopentobuy: floatNonNullRule,

    nbkiRating: ratingsRule,
    okbRating: ratingsRule,
    bkiCreditInfoRating: ratingsRule,
    bkiSBRating: ratingsRule,
    dti: percentRule,
    revolbal: {required: false,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return true
            }
            else if (!regexNonNegativeFloat.test(value)) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        }
        ,trigger: ['input', 'blur'],
    },
    mthssincerecentbc: smallIntNullRule,
    bcutil: percentRule,
    revolutil: percentRule,
};

const requiredFormFields = [
    {
        formValue: 'annualinc',
        label: 'Ежегодный доход'
    },
    {
        formValue: 'avgcurbal',
        label: 'Средняя задолженность среди всех кредитных счетов'
    },
    {
        formValue: 'totalacc',
        label: 'Количество всех кредитных счетов в кредитной истории'
    },
    {
        formValue: 'accopenpast24mths',
        label: 'Количество кредитных счетов, открытых за последние 24 месяца'
    },
    {
        formValue: 'totalbclimit',
        label: 'Суммарный кредитный лимит по всем кредитным картам'
    },
    {
        formValue: 'totalilhighcreditlimit',
        label: 'Суммарная база кредита по всем невозобновляемым кредитам'
    },
    {
        formValue: 'totalilrevhilim',
        label: 'Суммарный кредитный лимит по всем возобновляемым кредитам'
    },
    {
        formValue: 'emplength',
        label: 'Срок трудоустройства в годах'
    },
    {
        formValue: 'totalbalexmort',
        label: 'Суммарная задолженность по кредитам (исключая ипотеку)'
    },
    {
        formValue: 'bcopentobuy',
        label: 'Сумма, доступная к займу по всем кредитным картам'
    },
];

const nonRequiredFormFields = [
    {
        formValue: 'nbkiRating',
        label: 'Рейтинг АО «НБКИ»'
    },
    {
        formValue: 'okbRating',
        label: 'Рейтинг АО «ОКБ»'
    },
    {
        formValue: 'bkiCreditInfoRating',
        label: 'Рейтинг ООО «БКИ КредитИнфо»'
    },
    {
        formValue: 'bkiSBRating',
        label: 'Рейтинг АО «БКИ СБ»'
    },
    {
        formValue: 'dti',
        label: 'Отношение платежей по кредитам (исключая ипотеку) к месячному доходу'
    },
    {
        formValue: 'revolbal',
        label: 'Суммарная задолженность по возобновляемым кредитам'
    },
    {
        formValue: 'mthssincerecentbc',
        label: 'Количество месяцев с открытия последней кредитной карты'
    },
    {
        formValue: 'bcutil',
        label: 'Доля задолженности по кредитным картам к кредитному лимиту по ним'
    },
    {
        formValue: 'revolutil',
        label: 'Доля задолженности по возобновляемым кредитам к кредитному лимиту по ним'
    },
];

onMounted(() => {
    if (props.mode == 'update') {
        const {
            id, passport, ...formData
        } = { ...props.client }
        clientForm.value = formData
    }
})

function submit(e: MouseEvent) {
    e.preventDefault()
    formRef.value?.validate((errors: Array<FormValidationError> | undefined) => {
        if (!errors) {
            const payload = {};
            Object.entries(clientForm.value).forEach(([k, v]) => {
                payload[k] = v ? v : v == 0 ? 0 : null;
            });
            emit('submit', payload)
        }
    })
}

</script>
