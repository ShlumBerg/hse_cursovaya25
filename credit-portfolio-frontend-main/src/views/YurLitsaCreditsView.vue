<template>
    <div>
        <div class="flex items-center gap-2">
            <n-button size="small" @click="loadCredits">
                Обновить
            </n-button>

            <n-input-group>
                <n-input v-model:value="filterOgrn" size="small" placeholder="Поиск по ОГРН" @keydown.enter.prevent="loadCredits" />
                <n-input v-model:value="filterUuid" size="small" placeholder="Поиск по счету" @keydown.enter.prevent="loadCredits" />
                <n-button ghost @click="loadCredits">
                    Поиск
                </n-button>
            </n-input-group>
        </div>

        <div v-show="checkedRowKeysRef?.length" class="flex items-center gap-2 mt-2">
            <n-button size="small" @click="checkedRowKeysRef = []">
                Отменить выбор
            </n-button>
            <n-button v-if="selectedCredit?.credit_statistics?.unpaid_payments" size="small" @click="creditDestructureDialog = true">
                Реструктуризация выбранного кредита
            </n-button>
            <n-button v-if="selectedCredit?.credit_statistics?.unpaid_payments" size="small" @click="onDeleteCredit">
                Списание кредита
            </n-button>
            <n-button size="small" @click="creditInfoDialog = true">
                Выписка по выбранному кредиту
            </n-button>
            <n-button v-if="selectedCredit?.credit_statistics?.unpaid_payments" size="small" @click="creditPayoffDialog = true">
                Внесение оплаты по выбранному кредиту
            </n-button>
        </div>

        <div class="mt-4">
            <n-data-table
                v-model:checked-row-keys="checkedRowKeysRef"
                :data="credits"
                :columns="columns"
                :single-line="false"
                :loading="loading"
                :row-key="(row) => row.id"
                size="small"
            >
                <template v-slot:empty>
                    <div>Данные не найдены...</div>
                </template>
            </n-data-table>
        </div>

        <NModal v-if="selectedCredit" v-model:show="creditInfoDialog" size="small">
            <CreditInfo
                :credit="selectedCredit"
                client-type="ur"
                style="width: 80%;"
            />
        </NModal>

        <NModal v-if="selectedCredit" v-model:show="creditPayoffDialog" size="small">
            <CreditPayoffForm
                :credit="selectedCredit"
                client-type="ur"
                style="width: 50%;"
                @submit="createCreditPayoff"
            />
        </NModal>

         <NModal v-if="selectedCredit" v-model:show="creditDestructureDialog" size="small">
            <CreditRestructureForm
                :credit="selectedCredit"
                client-type="ur"
                style="width: 50%;"
                @submit="restructureUrClientCredit"
            />
        </NModal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h, computed } from 'vue';
import {
    creditCreditList, creditCreditDestroy, creditCreateCreditPayoffCreate, creditRestructureCreditCreate, creditPledgeCreate,
    type CreditRestructureCreateRequest, type Credit, type PledgeRequest,
} from '@/api';
import {
    NButton, NInputGroup, NInput, NDataTable, NModal, NTag,
    type DataTableColumn,
    useMessage, useDialog,
} from 'naive-ui';
import CreditInfo from '@/components/CreditInfo.vue';
import CreditDeleteInfo from '@/components/CreditDeleteInfo.vue';
import CreditPayoffForm from '@/components/CreditPayoffForm.vue';
import CreditRestructureForm from '@/components/CreditRestructureForm.vue';
import CreditPaidNotification from '@/components/CreditPaidNotification.vue';

const message = useMessage();

const dialog = useDialog();

const creditInfoDialog = ref(false);

const creditPayoffDialog = ref(false);

const creditDestructureDialog = ref(false);

const loading = ref(false);

const filterOgrn = ref('');

const filterUuid = ref('');

const checkedRowKeysRef = ref([]);

const selectedCredit = computed(() => credits?.value?.find((c) => c.id == checkedRowKeysRef?.value?.[0]));

const columns: DataTableColumn<Credit>[] = [
    {
      type: 'selection',
      multiple: false,
    },
    {
      title: 'Статус',
      key: 'status',
      className: 'break-keep text-xs',
      render(row: Credit) {
        return h(
            NTag,
            {
                type: row?.credit_statistics?.unpaid_payments ? 'warning' : 'success',
                size: 'tiny',
                round: true,
            },
            {
                default: row?.credit_statistics?.unpaid_payments ? 'Не выплачен' : 'Выплачен'
            },
        )
      },
    },
    {
        title: 'Номер счёта',
        key: 'uuid',
        className: 'break-keep text-xs',
    },
    {
        title: 'ОГРН клиента',
        key: 'ogrn',
        className: 'break-keep text-xs',
    },
    {
        title: 'Пеня',
        key: 'dailypennies',
        className: 'break-keep text-xs',
    },
    {
        title: 'База кредита',
        key: 'totalbase',
        className: 'break-keep text-xs',
    },
    {
        title: 'Процент',
        key: 'yearlypercents',
        className: 'break-keep text-xs',
    },
    {
        title: 'Количество выплат',
        key: 'term',
        className: 'break-keep text-xs',
    },
    {
        title: 'Полностью погашенные выплаты',
        key: 'paidpennies',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.credit_statistics?.paid_payments)
        },
    },
    {
        title: 'Остаток к оплате',
        key: 'unpaidpennies',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.credit_statistics?.currentlyunpaid)
        },
    },
    {
        title: 'Оплаченная база',
        key: 'paidbase',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.credit_statistics?.paidbase)
        },
    },
    {
        title: 'Неоплаченная база',
        key: 'unpaidbase',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.credit_statistics?.unpaidbase)
        },
    },
    {
        title: 'Оплаченные проценты',
        key: 'paidpercents',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.credit_statistics?.paidpercents)
        },
    },
    {
        title: 'Неоплаченные проценты',
        key: 'unpaidpercents',
        className: 'break-keep text-xs',
            render(row: Credit) {
            return h('span', row?.credit_statistics?.unpaidpercents)
        },
    },
    {
        title: 'Оплаченные пени',
        key: 'paidpennies',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.credit_statistics?.paidpennies)
        },
    },
    {
        title: 'Неоплаченные пени',
        key: 'unpaidpennies',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.credit_statistics?.unpaidpennies)
        },
    },
        {
        title: 'Стоимость заложенного объекта',
        key: 'expectedPrice',
        className: 'break-keep text-xs',
        render(row: Credit) {
            return h('span', row?.pledges?.[0]?.expectedPrice || 'Без залога')
        },
    },
]

const credits = ref<Credit[]>([])

onMounted(() => {
    loadCredits()
})

function loadCredits() {
    loading.value = true;
    creditCreditList({
        query: {
            ur_clients_only: true,
            ur_client__ogrn: filterOgrn.value,
            uuid: filterUuid.value,
        },
        throwOnError: true,
    })
        .then((response) => credits.value = response.data || [])
        .catch((err) => {
            console.error(err)
            message.error('При загрузке кредитов произошла ошибка!')
        })
        .finally(() => loading.value = false)
}

function onDeleteCredit() {
    if (selectedCredit.value) {
        dialog.warning({
            content() {
                return h(CreditDeleteInfo, {credit: {...selectedCredit.value as Credit}})
            },
            positiveText: 'Подтвердить',
            negativeText: 'Закрыть',
            autoFocus: false,
            closable: false,
            onPositiveClick: () => {
                deleteCredit()
            },
        })
    }
}

function deleteCredit() {
    if (selectedCredit.value) {
        loading.value = true;
        creditCreditDestroy({
            path: {
                id: selectedCredit.value.id,
            },
            throwOnError: true,
        })
            .then((response) => {
                message.info(`Кредит успешно списан!`)
                checkedRowKeysRef.value = [];
                loadCredits()
            })
            .catch((err) => {
                console.error(err)
                message.error('При списании кредита произошла ошибка!')
            })
            .finally(() => loading.value = false)
    }
}

function createCreditPayoff(total: number) {
    if (selectedCredit.value) {
        creditCreateCreditPayoffCreate({
            body: {
                credit: selectedCredit.value.id,
                payoff_amount: total,
            },
            throwOnError: true,
        })
            .then((response) => {
                message.info(`По счету ${selectedCredit.value?.uuid} внесена оплата в размере ${total} рублей`)
                loadCredits()
                creditPayoffDialog.value = false;
                if (response.data.remainder) {
                    dialog.success({
                        content() {
                            return h(CreditPaidNotification, {
                                credit: {...selectedCredit.value as Credit},
                                paymentAmount: total,
                                remainder: response.data.remainder,
                            })
                        },
                        positiveText: `Вернуть сдачу (${response.data.remainder} рублей)`,
                        autoFocus: false,
                        closable: false,
                    })
                } else {
                    creditInfoDialog.value = true;
                }
            })
            .catch((err) => {
                console.error(err)
                message.error('При погашении кредита произошла ошибка!')
            })
            
    }
}

function restructureUrClientCredit(credit_data: CreditRestructureCreateRequest, pledge?: PledgeRequest) {
    const oldUuid = selectedCredit?.value?.uuid;

    if (selectedCredit.value) {
        creditRestructureCreditCreate({
            body: {
                ...credit_data,
                credit: selectedCredit.value.id,
            },
            throwOnError: true,
        })
            .then(async (response) => {
                const newCreditUuid = response.data?.uuid;
                const newCreditOgrn = response.data?.ogrn;
                message.info(`Был добавлен кредит с номером счета ${newCreditUuid} юридическому лицу (ОГРН ${newCreditOgrn}). Старый кредит с номером счета ${oldUuid} был удалён!`)
                if (pledge) {
                    await creditPledgeCreate({
                        body: {
                            ...pledge,
                            credit: response.data?.id as number,
                        }
                    })
                        .then((response) => {
                            loadCredits()
                        })
                        .catch((err) => {
                            console.error(err)
                            message.error(`При создании залога по кредиту с ID ${response.data.id} произошла ошибка!`)
                        })
                } else {
                    loadCredits()
                }
                checkedRowKeysRef.value = [];
            })
            .catch((err) => {
                console.error(err)
                message.error(`При реструктуризации кредита № ${oldUuid} произошла ошибка!`)
            })
            .finally(() => creditDestructureDialog.value = false)
    }
}
</script>