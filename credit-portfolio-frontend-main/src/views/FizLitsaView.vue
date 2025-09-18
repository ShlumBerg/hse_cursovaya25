<template>
    <div>
        <div class="flex items-center gap-2">
            <n-button size="small" @click="loadClients">
                Обновить
            </n-button>
            <n-button size="small" @click="addClientDialog = true">
                Добавить клиента
            </n-button>

            <n-input-group>
                <n-input v-model:value="filterValue" size="small" placeholder="Поиск по паспорту" @keydown.enter.prevent="loadClients" />
                <n-button ghost @click="loadClients">
                    Поиск
                </n-button>
            </n-input-group>
        </div>

        <div v-if="checkedRowKeysRef?.length" class="flex items-center gap-2 mt-2">
            <n-button size="small" @click="checkedRowKeysRef = []">
                Отменить выбор
            </n-button>
            <n-button size="small" @click="changeClientDialog = true">
                Изменение данных выбранного клиента
            </n-button>
            <n-popconfirm
                @positive-click="deleteClient"
                positive-text="Да"
                negative-text="Нет"
            >
                <template #trigger>
                    <n-button size="small">
                        Удаление выбранного клиента
                    </n-button>
                </template>
                Вы действительно хотите удалить выбранного клиента?
            </n-popconfirm>
            <n-button size="small" @click="createCreditDialog = true">
                Создать кредит
            </n-button>
        </div>

        <div class="mt-4">
            <n-data-table
                v-model:checked-row-keys="checkedRowKeysRef"
                :data="clients"
                :columns="columns"
                :single-line="false"
                :loading="loading"
                :row-key="(row) => row?.id"
                size="small"
            >
                <template v-slot:empty>
                    <div>Данные не найдены...</div>
                </template>
            </n-data-table>
        </div>

        <NModal v-model:show="addClientDialog">
            <n-card
                title="Создание Физического лица"
                style="width: 80%"
                :bordered="false"
                size="small"
                role="dialog"
                aria-modal="true"
            >
                <FizClientForm mode="create" @submit="addClient" />
            </n-card>
        </NModal>

        <NModal v-model:show="changeClientDialog">
            <n-card
                :title="`Изменение данных Физического лица (паспорт № ${selectedClient?.passport})`"
                style="width: 80%"
                :bordered="false"
                size="small"
                role="dialog"
                aria-modal="true"
            >
                <FizClientForm mode="update" :client="selectedClient" @submit="editClient" />
            </n-card>
        </NModal>

        <NModal v-model:show="createCreditDialog">
            <n-card
                :title="`Выдача кредита физическому лицу (паспорт № ${selectedClient?.passport})`"
                style="width: 60%"
                :bordered="false"
                size="small"
                role="dialog"
                aria-modal="true"
            >
                <CreditForm mode="update" :fiz-client="selectedClient" @submit="createClientCredit" />
            </n-card>
        </NModal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h, computed  } from 'vue';
import {
    creditFizClientCreate,
    creditFizClientList,
    creditFizClientDestroy,
    creditFizClientPartialUpdate,
    creditCreditCreate,
    creditPledgeCreate,
} from '@/api';
import {
    NButton, NInputGroup, NInput, NPopconfirm, NDataTable, NCard, NModal,
    type DataTableColumn, useMessage,
} from 'naive-ui';
import type { FizClientRequest, PatchedFizClientRequest, FizClient, CreditRequest, PledgeRequest } from '@/api';
import FizClientForm from '@/components/FizClientForm.vue';
import CreditForm from '@/components/CreditForm.vue';

const checkedRowKeysRef = ref([]);

const loading = ref(false);

const message = useMessage();

const addClientDialog = ref(false);

const selectedClient = computed(() => clients?.value?.find((c) => c.id == checkedRowKeysRef?.value?.[0]));

const changeClientDialog = ref(false);

const createCreditDialog = ref(false);

const filterValue = ref('');

const columns: DataTableColumn<FizClient>[] = [
    {
      type: 'selection',
      multiple: false,
    },
    {
        title: 'Паспорт',
        key: 'passport',
        className: 'break-keep text-xs',
    },
    {
        title: 'Ежегодный доход',
        key: 'annualinc',
        className: 'break-keep text-xs',
    },
    {
        title: 'Рейтинг АО "НБКИ"',
        key: 'nbkiRating',
        className: 'break-keep text-xs',
    },
    {
        title: 'Рейтинг АО «ОКБ»',
        key: 'okbRating',
        className: 'break-keep text-xs',
    },
    {
        title: 'Рейтинг ООО «БКИ КредитИнфо»',
        key: 'bkiCreditInfoRating',
        className: 'break-keep text-xs',
    },
    {
        title: 'Рейтинг АО «БКИ СБ»',
        key: 'bkiSBRating',
        className: 'break-keep text-xs',
    },
    {
        title: 'Дата обновления сведений',
        key: 'infoupdatedate',
        className: 'break-keep text-xs',
    },
    {
        title: 'Оплаченные пени',
        key: 'paidpennies',
        className: 'break-keep text-xs',
        render(row: FizClient) {
            return h('span', row?.credit_statistics?.paidpennies)
        },
    },
    {
        title: 'Неоплаченные пени',
        key: 'unpaidpennies',
        className: 'break-keep text-xs',
        render(row: FizClient) {
            return h('span', row?.credit_statistics?.unpaidpennies)
        },
    },
    {
        title: 'Оплаченная база',
        key: 'paidbase',
        className: 'break-keep text-xs',
        render(row: FizClient) {
            return h('span', row?.credit_statistics?.paidbase)
        },
    },
    {
        title: 'Неоплаченная база',
        key: 'unpaidbase',
        className: 'break-keep text-xs',
        render(row: FizClient) {
            return h('span', row?.credit_statistics?.unpaidbase)
        },
    },
    {
        title: 'Оплаченные проценты',
        key: 'paidpercents',
        className: 'break-keep text-xs',
        render(row: FizClient) {
            return h('span', row?.credit_statistics?.paidpercents)
        },
    },
    {
        title: 'Неоплаченные проценты',
        key: 'unpaidpercents',
        className: 'break-keep text-xs',
        render(row: FizClient) {
            return h('span', row?.credit_statistics?.unpaidpercents)
        },
    },
    {
        title: 'Дата подсчета статистики по кредитам',
        key: 'statusupdatedate',
        className: 'break-keep text-xs',
        render(row: FizClient) {
            return h('span', row?.credit_statistics?.timestamp)
        },
    },
]

const clients = ref<FizClient[]>([]);

onMounted(() => {
    loadClients()
})

function loadClients() {
    loading.value = true;
    creditFizClientList({
        query: {
            passport: filterValue.value,
        },
        throwOnError: true,
    })
        .then((response) => {
            clients.value = response.data || [];
        })
        .catch((err) => {
            console.error(err)
            message.error('При загрузке физических лиц произоша ошибка!')
        })
        .finally(() => loading.value = false)
}

function addClient(data: FizClientRequest) {
    creditFizClientCreate({
        body: { ...data },
        throwOnError: true,
    })
        .then((response) => {
            message.info(`Добавлен новый клиент (паспорт ${data.passport})`)
            loadClients()
            addClientDialog.value = false;
        })
        .catch((err) => {
            console.error(err)
            message.error('При создании физического лица произошла ошибка!')
        })
}

function deleteClient() {
    const selectedClientId = selectedClient?.value?.id;
    if (selectedClientId) {
        creditFizClientDestroy({
            path: {id: selectedClientId},
            throwOnError: true,
        })
            .then((response) => {
                message.info('Клиент успешно удален!')
                loadClients()
                checkedRowKeysRef.value = [];
            })
            .catch((err) => {
                console.error(err)
                message.error(`При удалении физического лица (паспорт № ${selectedClient.value?.passport}) произошла ошибка!`)
            })
    }
}

function editClient(data: PatchedFizClientRequest) {
    const selectedClientId = selectedClient?.value?.id;
    if (selectedClientId) {
        creditFizClientPartialUpdate({
            path: {id: selectedClientId},
            body: data,
            throwOnError: true,
        })
            .then((response) => {
                message.info('Данные клиента изменены!')
                loadClients()
                changeClientDialog.value = false;
            })
            .catch((err) => {
                console.error(err)
                message.error(`При изменении физического лица (паспорт № ${selectedClient.value?.passport}) произошла ошибка!`)
            })
    }
}

function createClientCredit(credit: CreditRequest, pledge?: PledgeRequest) {
    if (selectedClient.value) {
        creditCreditCreate({
            body: {
                ...credit,
                fiz_client: selectedClient.value.id,
            },
            throwOnError: true,
        })
            .then(async (response) => {
                message.info(`Кредит для физического лица (паспорт № ${selectedClient.value?.passport}) успешно выдан!`)
                if (pledge) {
                    await creditPledgeCreate({
                        body: {
                            ...pledge,
                            credit: response.data?.id as number,
                        }
                    })
                        .then((response) => {
                            loadClients()
                        })
                        .catch((err) => {
                            console.error(err)
                            message.error(`При создании залога по кредиту с ID ${response.data.id} произошла ошибка!`)
                        })
                } else {
                    loadClients()
                }
            })
            .catch((err) => {
                console.error(err)
                message.error(`При выдаче кредита физическому лицу (паспорт № ${selectedClient.value?.passport}) произошла ошибка!`)
            })
            .finally(() => createCreditDialog.value = false)
    }
}

</script>