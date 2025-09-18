<template>
    <n-form ref="formRef" size="small" :model="urClientForm" :rules="rules">
        <n-form-item v-if="mode == 'create'" path="ogrn" label="ОГРН">
            <n-input size="small" v-model:value="urClientForm.ogrn" placeholder="Введите значение" @keydown.enter.prevent />
        </n-form-item>

        <n-row :gutter="[16, 16]">
            <n-col v-for="selectFormField in selectFormFields" :key="selectFormField.formValue" :span="6">
                <n-form-item :path="selectFormField.formValue" :label="selectFormField.label">
                    <n-select size="small" v-model:value="urClientForm[selectFormField.formValue]" :options="selectFormField.options.value" label-field="value" value-field="id" placeholder="Выберите значение" @keydown.enter.prevent />
                </n-form-item>
            </n-col>
        </n-row>

        <div class="my-4 text-justify">
            <div>
                Для вычисления кредитоспособности организации по моделям Сайфуллина и Зайцевой, необходимы сведения из её финансовой отчетности за предыдущий год (обозначим без индекса) и за год до него (с индексом “Прошлого года”).
            </div>
            <div>
                Введите финансовые показатели из соответствующих строк РСБУ ниже:
            </div>
        </div>
        
        <n-row :gutter="[16,0]">
            <n-col v-for="strFormField in strFormFields" :key="strFormField.formValue" :span="6">
                <n-form-item :path="strFormField.formValue" :label="strFormField.label">
                    <n-input size="small" v-model:value="urClientForm[strFormField.formValue]" placeholder="Введите значение" @keydown.enter.prevent />
                </n-form-item>
            </n-col>
        </n-row>

        <n-button type="info" @click="submit">
            {{ mode == 'create' ? 'Создать' : 'Сохранить' }}
        </n-button>
    </n-form>
</template>

<script setup lang="ts">
import { ref, onMounted, h  } from 'vue';
import {
    creditRatingAcraList,
    creditRatingNcrList,
    creditRatingNraList,
    creditRatingExpertList,
} from '@/api';
import {
    NButton, NInputGroup, NInput, NSelect, NDataTable, NRow, NCol, NCard, NModal, NForm, NFormItem,
    type FormRules, type FormItemRule, type FormValidationError, type DataTableColumn, useMessage,
} from 'naive-ui';
import type { UrClientRequest, PatchedUrClientRequest, RatingAcra, RatingNcr, RatingNra, RatingExpert, UrClient } from '@/api';

interface Props {
    mode: 'create' | 'update';
    urClient?: UrClient;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    submit: [data: UrClientRequest];
}>();

const formRef = ref();

const ratingAcra = ref<RatingAcra[]>([]);
const ratingNcr = ref<RatingNcr[]>([]);
const ratingNra = ref<RatingNra[]>([]);
const ratingExpert = ref<RatingExpert[]>([]);

const urClientForm = ref<UrClientRequest | PatchedUrClientRequest>({
    ogrn: null,
    ratingacra: null,
    ratingnra: null,
    ratingncr: null,
    ratingexpert: null,
    str2300: null,
    str1300: null,
    str2400: null,
    str2110pred: null,
    str1520: null,
    str1230: null,
    str1510: null,
    str2110: null,
    str1250: null,
    str1400: null,
    str1500: null,
    str1600: null,
    str1100: null,
    str1200: null,
    str1550: null,
    str1600pred: null,
})

const ratingRule = {
    required: true,
    validator(rule: FormItemRule, value: string) {
        if (!value) {
            return new Error('Выберите значение')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const strRule1 = {
    required: true,
    validator(rule: FormItemRule, value: string) {
        if (!value) {
            return new Error('Выберите значение')
        } else if (!(/^-[1-9][0-9]{0,11}$|^[1-9][0-9]{0,11}$/.test(value))) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const strRule2 = {
    required: true,
    validator(rule: FormItemRule, value: string) {
        if (!value) {
            return new Error('Выберите значение')
        } else if (!(/^[1-9][0-9]{0,11}$/.test(value))) {
            return new Error('Ошибка! Некорректное значение!')
        }
        return true
    },
    trigger: ['input', 'blur'],
};

const rules: FormRules = {
    ogrn: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(/^[0-9]{13}$/.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
    ratingacra: ratingRule,
    ratingnra: ratingRule,
    ratingncr: ratingRule,
    ratingexpert: ratingRule,
    str2300: strRule1,
    str1300: strRule1,
    str2400: strRule1,
    str2110pred: strRule2,
    str1520: strRule2,
    str1230: strRule2,
    str1510: strRule2,
    str2110: strRule2,
    str1250: strRule2,
    str1400: strRule2,
    str1500: strRule2,
    str1600: strRule2,
    str1100: strRule2,
    str1200: strRule2,
    str1550: strRule2,
    str1600pred: strRule2,
}


const selectFormFields = [
    {
        formValue: "ratingacra",
        options: ratingAcra,
        label: "рейтинг АКРА (АО) клиента",
    },
    {
        formValue: "ratingexpert",
        options: ratingExpert,
        label: 'рейтинг АО "Эксперт РА" клиента',
    },
    {
        formValue: "ratingncr",
        options: ratingNcr,
        label: 'рейтинг ООО "НКР" клиента',
    },
    {
        formValue: "ratingnra",
        options: ratingNra,
        label: 'рейтинг ООО "НРА" клиента',
    }
]

const strFormFields = [
    {
        formValue: 'str2300',
        label: 'стр.2300'
    },
    {
        formValue: 'str1300',
        label: 'стр.1300'
    },
    {
        formValue: 'str2400',
        label: 'стр.2400'
    },
    {
        formValue: 'str1520',
        label: 'стр.1520'
    },
    {
        formValue: 'str1230',
        label: 'стр.1230'
    },
    {
        formValue: 'str1510',
        label: 'стр.1510'
    },
    {
        formValue: 'str2110',
        label: 'стр.2110'
    },
    {
        formValue: 'str1250',
        label: 'стр.1250'
    },
    {
        formValue: 'str1400',
        label: 'стр.1400'
    },
    {
        formValue: 'str1500',
        label: 'стр.1500'
    },
    {
        formValue: 'str1600',
        label: 'стр.1600'
    },
    {
        formValue: 'str1100',
        label: 'стр.1100'
    },
    {
        formValue: 'str1200',
        label: 'стр.1200'
    },
    {
        formValue: 'str1550',
        label: 'стр.1550'
    },
    {
        formValue: 'str1600pred',
        label: 'стр.1600 прошлого года'
    },
    {
        formValue: 'str2110pred',
        label: 'стр.2110 прошлого года'
    },
]

onMounted(() => {
    if (props.mode == 'update') {
        const {
            id, ogrn, ratingncr_detail, ratingnra_detail, ratingacra_detail, ratingexpert_detail, ...formData
        } = { ...props.urClient }
        urClientForm.value = formData
    }

    Promise.all([
        creditRatingAcraList(),
        creditRatingNcrList(),
        creditRatingNraList(),
        creditRatingExpertList(),
    ])
        .then((responses) => {
            ratingAcra.value = responses[0].data || [];
            ratingNcr.value = responses[1].data || [];
            ratingNra.value = responses[2].data || [];
            ratingExpert.value = responses[3].data || [];
        })
})

function submit(e: MouseEvent) {
    e.preventDefault()
    formRef.value?.validate((errors: Array<FormValidationError> | undefined) => {
        if (!errors) {
            emit('submit', urClientForm.value)
        }
    })
}

</script>
