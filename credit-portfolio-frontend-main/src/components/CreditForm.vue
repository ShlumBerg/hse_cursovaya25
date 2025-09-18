<template>
    <div>
        <div v-if="urClient" class="mb-8">
            <div class="mb-4">
                <span>Сведения о клиенте: </span>
                <NTag :type="urClient?.is_valid_info ? 'success' : 'warning'">
                    {{ urClient?.is_valid_info ? 'актуальные' : 'устаревшие' }}
                </NTag>
            </div>

            <div class="flex gap-4 mb-4">
                <div>
                    <span class="font-bold">
                        Оценка по модели Сайфуллина: 
                    </span>
                    <NTag v-if="urClient?.high_risk_saifullin" type="error" size="small">
                        высокая вероятность дефолта
                    </NTag>
                    <NTag v-else type="success" size="small">
                        низкая вероятность дефолта
                    </NTag>
                </div>
                <div>
                    <span class="font-bold">
                        Оценка по модели Зайцевой: 
                    </span>
                    <NTag v-if="urClient?.high_risk_zayceva" type="error" size="small">
                        высокая вероятность дефолта
                    </NTag>
                    <NTag v-else type="success" size="small">
                        низкая вероятность дефолта
                    </NTag>
                </div>
            </div>

            <n-row :gutter="[16,16]">
                <n-col :span="12">
                    <span>
                        Рейтинг ООО "НКР" клиента: <NTag size="small">{{ urClient?.ratingncr_detail?.value }}</NTag>
                    </span>
                </n-col>
                <n-col :span="12">
                    <span>
                        Рейтинг АО "Эксперт РА" клиента: <NTag size="small">{{ urClient?.ratingexpert_detail?.value }}</NTag>
                    </span>
                </n-col>
                <n-col :span="12">
                    <span>
                        Рейтинг ООО "НРА" клиента: <NTag size="small">{{ urClient?.ratingnra_detail?.value }}</NTag>
                    </span>
                </n-col>
                <n-col :span="12">
                    <span>
                        Рейтинг АКРА (АО) клиента: <NTag size="small">{{ urClient?.ratingacra_detail?.value }}</NTag>
                    </span>
                </n-col>
            </n-row>
        </div>

        <div v-if="fizClient" class="mb-8">
            <div class="mb-4">
                <span>Сведения о клиенте: </span>
                <NTag :type="fizClient?.is_valid_info ? 'success' : 'warning'">
                    {{ fizClient?.is_valid_info ? 'актуальные' : 'устаревшие' }}
                </NTag>
            </div>

            <n-row :gutter="[16,16]">
                <n-col :span="12">
                    <span>
                        Рейтинг АО "НБКИ" клиента: <NTag size="small">{{ fizClient?.nbkiRating }}</NTag>
                    </span>
                </n-col>
                <n-col :span="12">
                    <span>
                        Рейтинг АО «ОКБ» клиента: <NTag size="small">{{ fizClient?.okbRating }}</NTag>
                    </span>
                </n-col>
                <n-col :span="12">
                    <span>
                        Рейтинг ООО «БКИ КредитИнфо» клиента: <NTag size="small">{{ fizClient?.bkiCreditInfoRating }}</NTag>
                    </span>
                </n-col>
                <n-col :span="12">
                    <span>
                        Рейтинг АО «БКИ СБ» клиента: <NTag size="small">{{ fizClient?.bkiSBRating }}</NTag>
                    </span>
                </n-col>
            </n-row>
        </div>

        <div class="flex gap-8">
            <n-form ref="creditFormRef" size="small" :model="creditForm" :rules="creditFormRules" class="w-full">
                <n-form-item path="term" label="Срок выплаты кредита (в месяцах)">
                    <n-input-number size="small" v-model:value="creditForm.term" placeholder="Введите значение" class="w-full" @keydown.enter.prevent />
                </n-form-item>
                <n-form-item path="totalbase" label="Сумма кредита (в рублях)">
                    <n-input-number size="small" v-model:value="creditForm.totalbase" placeholder="Введите значение" class="w-full" @keydown.enter.prevent />
                </n-form-item>
                <n-form-item path="yearlypercents" label="Процентная ставка по кредиту (в процентах годовых)">
                    <n-input-number size="small" v-model:value="creditForm.yearlypercents" placeholder="Введите значение" class="w-full" @keydown.enter.prevent />
                </n-form-item>
                <n-form-item path="dailypennies" label="Размер пени по просрочке (в процентах в день)">
                    <n-input-number size="small" v-model:value="creditForm.dailypennies" placeholder="Введите значение" class="w-full" @keydown.enter.prevent />
                </n-form-item>
            </n-form>

            <n-form ref="pledgeFormRef" size="small" :model="pledgeForm" :rules="pledgeFormRules" class="w-full">
                <n-form-item label="Тип залога">
                    <n-flex>
                        <n-radio
                            v-for="radioButton in radioButtons" :key="radioButton.label"
                            :checked="pledgeType === radioButton.value"
                            :value="radioButton.value"
                            @change="handleChangePledgeType"
                        >
                            {{ radioButton.label }}
                        </n-radio>
                        
                    </n-flex>
                </n-form-item>

                <n-form-item v-if="pledgeType == 'auto'" path="vinCode" label="Автомобиль">
                    <n-input size="small" v-model:value="pledgeForm.vinCode" placeholder="Введите VIN-код автомобиля" @keydown.enter.prevent />
                </n-form-item>

                <n-form-item v-if="pledgeType == 'realestate'" path="cadastralNumber" label="Недвижимость">
                    <n-input size="small" v-model:value="pledgeForm.cadastralNumber" placeholder="Введите кадастровый номер недвижимости" @keydown.enter.prevent />
                </n-form-item>

                <n-form-item v-if="pledgeType !== 'no'" path="expectedPrice" label="Стоимость заложенного объекта (в рублях)">
                    <n-input-number size="small" v-model:value="pledgeForm.expectedPrice" placeholder="Введите значение" @keydown.enter.prevent />
                </n-form-item>
            </n-form>
        </div>

        <div v-if="fizClient" class="mb-4">
            <div class="flex gap-4">
                <div class="font-semibold">
                    Прогноз по модели машинного обучения
                </div>
                <NButton size="tiny" type="warning" :disabled="!isPredictionAvailable" @click="getPrediction" :loading="predictionResult.loading">
                    Получить прогноз
                </NButton>
            </div>

            <div v-if="predictionResult.predicted" class="mt-1">
                <span>Вероятность выплаты кредита клиентом: </span>
                <NTag size="small" v-if="predictionResult.ok" type="success">Высокая</NTag>
                <NTag size="small" v-else type="error">Низкая</NTag>
            </div>
        </div>
        
        <div class="flex justify-end">
            <n-button type="info" @click="submit">
                Создать
            </n-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted,computed } from 'vue';
import {
    NButton, NInputNumber, NInput, NRow, NCol, NFlex, NRadio, NForm, NFormItem, NTag,
    type FormRules, type FormItemRule, type FormValidationError,
    useMessage,
} from 'naive-ui';
import { creditCheckFizClientCreditworthinessCreate } from '@/api';
import type { CreditRequest, PledgeRequest, FizClient, UrClient } from '@/api';

interface Props {
    urClient?: UrClient;
    fizClient?: FizClient;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    submit: [credit: CreditRequest, pledge?: Omit<PledgeRequest, 'credit'>];
}>();

const message = useMessage();

const creditFormRef = ref();

const predictionResult = ref<{loading: boolean; predicted: boolean; ok: boolean | undefined;}>({
    loading: false,
    predicted: false,
    ok: undefined,
});

const isPredictionAvailable = computed(() => {
    return creditForm.value.term && creditForm.value.totalbase && creditForm.value.yearlypercents
})

const creditForm = ref<CreditRequest>({
    term: null,
    totalbase: null,
    yearlypercents: null,
    dailypennies: null,
})

const pledgeFormRef = ref();

const pledgeType = ref<'auto' | 'realestate' | 'no'>('no');

const radioButtons = [
    {
        'label': 'Без залога',
        'value': 'no',
    },
    {
        'label': 'Автомобиль',
        'value': 'auto',
    },
    {
        'label': 'Недвижимость',
        'value': 'realestate',
    }
]

const pledgeForm = ref<Omit<PledgeRequest, 'credit'>>({
    vinCode: null,
    cadastralNumber: null,
    expectedPrice: null,
})

const regexMonths=/^[1-9][0-9]*$/;
const regexBase=/^\d+(\.\d{1,2})?$/;
const regexPercents=/(^[1-9][0-9]*$)|(^0\.[0-9]+$)|(^[1-9][0-9]*\.[0-9]+$)|(^0$)/;
const regexPennies=/(^[1-9][0-9]*$)|(^0\.[0-9]+$)|(^[1-9][0-9]*\.[0-9]+$)|(^0$)/;

const regexForPledgePrice=/^[1-9][0-9]*$/;
const regexForVinCode=/^([0-9]|[A-Z]){5,}$/;
const regexForCadastralNumber=/^[0-9]{2,}:[0-9]{2,}:[0-9]{7,}:[0-9]{2,}$/;


const creditFormRules: FormRules = {
    term: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(regexMonths.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
    totalbase: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(regexBase.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
    yearlypercents: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(regexPercents.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
    dailypennies: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(regexPennies.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
}

const pledgeFormRules: FormRules = {
    vinCode: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(regexForVinCode.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
    cadastralNumber: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(regexForCadastralNumber.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    },
    expectedPrice: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            else if (!(regexForPledgePrice.test(value))) {
                return new Error('Ошибка! Некорректное значение!')
            }
            return true
        },
        trigger: ['input', 'blur'],
    }
}


onMounted(() => {
    return
})

function submit(e: MouseEvent) {
    e.preventDefault()
    creditFormRef.value?.validate((errors: Array<FormValidationError> | undefined) => {
        if (!errors) {
            pledgeFormRef.value?.validate((errors: Array<FormValidationError> | undefined) => {
                if (!errors) {
                    emit(
                        'submit',
                        creditForm.value,
                        pledgeType.value != 'no' ? pledgeForm.value : undefined,
                    )
                }
            })
        }
    })
}

function handleChangePledgeType(e: Event) {
    pledgeType.value = (e.target as HTMLInputElement)?.value
}

function getPrediction() {
    if (isPredictionAvailable.value && props.fizClient) {
        predictionResult.value.loading = true;
        creditCheckFizClientCreditworthinessCreate({
            body: {
                fiz_client: props.fizClient.id,
                term: creditForm.value.term,
                yearlypercents: creditForm.value.yearlypercents,
                dailypennies: creditForm.value.dailypennies,
                totalbase: creditForm.value.totalbase,
            },
            throwOnError: true,
        })
            .then((response) => {
                predictionResult.value.ok = response.data.ok;
                predictionResult.value.predicted = true;
            })
            .catch((err) => {
                console.error(err)
                message.error('При получении прогноза по модели машинного обучения произошла ошибка!')
            })
            .finally(() => predictionResult.value.loading = false)
    }
}

</script>
