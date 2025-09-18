<template>
    <div>
        <div class="flex items-center gap-2">
            <n-button size="small" @click="loadUrClients">
                Обновить
            </n-button>
            <n-button size="small" @click="addUrClientDialog = true">
                Добавить клиента
            </n-button>

            <n-input-group>
                <n-input v-model:value="filterValue" size="small" placeholder="Поиск по ОГРН" @keydown.enter.prevent="loadUrClients" />
                <n-button ghost @click="loadUrClients">
                    Поиск
                </n-button>
            </n-input-group>
        </div>

        <div v-if="checkedRowKeysRef?.length" class="flex items-center gap-2 mt-2">
            <n-button size="small" @click="checkedRowKeysRef = []">
                Отменить выбор
            </n-button>
            <n-button size="small" @click="changeUrClientDialog = true">
                Изменение данных выбранного клиента
            </n-button>
            <n-popconfirm
                @positive-click="deleteUrClient"
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
                :data="urClients"
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

        <NModal v-model:show="addUrClientDialog">
            <n-card
                title="Создание Юридического лица"
                style="width: 80%"
                :bordered="false"
                size="small"
                role="dialog"
                aria-modal="true"
            >
                <UrClientForm mode="create" @submit="addUrClient" />
            </n-card>
        </NModal>

        <NModal v-model:show="changeUrClientDialog">
            <n-card
                title="Изменение данных Юридического лица"
                style="width: 80%"
                :bordered="false"
                size="small"
                role="dialog"
                aria-modal="true"
            >
                <UrClientForm mode="update" :ur-client="selectedUrClient" @submit="editUrClient" />
            </n-card>
        </NModal>

        <NModal v-model:show="createCreditDialog">
            <n-card
                :title="`Выдача кредита юридическому лицу с ОГРН ${selectedUrClient?.ogrn}`"
                style="width: 60%"
                :bordered="false"
                size="small"
                role="dialog"
                aria-modal="true"
            >
                <CreditForm mode="update" :ur-client="selectedUrClient" @submit="createUrClientCredit" />
            </n-card>
        </NModal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h, computed  } from 'vue';
import {
    creditUrClientCreate,
    creditUrClientList,
    creditUrClientDestroy,
    creditUrClientPartialUpdate,
    creditRatingAcraList,
    creditRatingNcrList,
    creditRatingNraList,
    creditRatingExpertList,
    creditCreditCreate,
    creditPledgeCreate,
} from '@/api';
import {
    NButton, NInputGroup, NInput, NPopconfirm, NDataTable, NCard, NModal,
    type DataTableColumn, useMessage,
} from 'naive-ui';
import type { UrClientRequest, PatchedUrClientRequest, RatingAcra, RatingNcr, RatingNra, RatingExpert, UrClient, CreditRequest, PledgeRequest } from '@/api';
import UrClientForm from '@/components/UrClientForm.vue';
import CreditForm from '@/components/CreditForm.vue';

const checkedRowKeysRef = ref([]);

const loading = ref(false);

const message = useMessage();

const addUrClientDialog = ref(false);

const selectedUrClient = computed(() => urClients?.value?.find((c) => c.id == checkedRowKeysRef?.value?.[0]));

const changeUrClientDialog = ref(false);

const createCreditDialog = ref(false);

const filterValue = ref('');

const columns: DataTableColumn<UrClient>[] = [
    {
      type: 'selection',
      multiple: false,
    },
    {
        title: 'ОГРН',
        key: 'ogrn',
        className: 'break-keep text-xs',
    },
    {
        title: 'Рейтинг АКРА (АО)',
        key: 'ratingacra_detail',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.ratingacra_detail?.value)
        }
    },
    {
        title: 'Рейтинг АО "Эксперт РА"',
        key: 'ratingexpert_detail',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.ratingexpert_detail?.value)
        }
    },
    {
        title: 'Рейтинг ООО "НКР"',
        key: 'ratingncr_detail',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.ratingncr_detail?.value)
        }
    },
    {
        title: 'Рейтинг ООО "НРА"',
        key: 'ratingnra_detail',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.ratingnra_detail?.value)
        }
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
        render(row: UrClient) {
            return h('span', row?.credit_statistics?.paidpennies)
        },
    },
    {
        title: 'Неоплаченные пени',
        key: 'unpaidpennies',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.credit_statistics?.unpaidpennies)
        },
    },
    {
        title: 'Оплаченная база',
        key: 'paidbase',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.credit_statistics?.paidbase)
        },
    },
    {
        title: 'Неоплаченная база',
        key: 'unpaidbase',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.credit_statistics?.unpaidbase)
        },
    },
    {
        title: 'Оплаченные проценты',
        key: 'paidpercents',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.credit_statistics?.paidpercents)
        },
    },
    {
        title: 'Неоплаченные проценты',
        key: 'unpaidpercents',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.credit_statistics?.unpaidpercents)
        },
    },
    {
        title: 'Дата подсчета статистики по кредитам',
        key: 'statusupdatedate',
        className: 'break-keep text-xs',
        render(row: UrClient) {
            return h('span', row?.credit_statistics?.timestamp)
        },
    },
]

const urClients = ref<UrClient[]>([]);
const ratingAcra = ref<RatingAcra[]>([]);
const ratingNcr = ref<RatingNcr[]>([]);
const ratingNra = ref<RatingNra[]>([]);
const ratingExpert = ref<RatingExpert[]>([]);

onMounted(() => {
    loading.value = true;

    Promise.all([
        loadUrClients(),
        creditRatingAcraList(),
        creditRatingNcrList(),
        creditRatingNraList(),
        creditRatingExpertList(),
    ])
        .then((responses) => {
            ratingAcra.value = responses[1].data || [];
            ratingNcr.value = responses[2].data || [];
            ratingNra.value = responses[3].data || [];
            ratingExpert.value = responses[4].data || [];
        })
        .finally(() => loading.value = false)
})

async function loadUrClients() {
    loading.value = true;
    creditUrClientList({
        query: {
            ogrn: filterValue.value,
        },
        throwOnError: true,
    })
        .then((response) => {
            urClients.value = response.data || [];
        })
        .catch((err) => {
            console.error(err)
            message.error('При загрузке юридических лиц произоша ошибка!')
        })
        .finally(() => loading.value = false)
}

function addUrClient(data: UrClientRequest) {
    creditUrClientCreate({
        body: { ...data },
        throwOnError: true,
    })
        .then((response) => {
            message.info(`Добавлен новый клиент (ОГРН ${data.ogrn})`)
            loadUrClients()
            addUrClientDialog.value = false;
        })
        .catch((err) => {
            console.error(err)
            message.error('При создании Юридического лица произошла ошибка!')
        })
}

function deleteUrClient() {
    const selectedClientId = selectedUrClient?.value?.id;
    if (selectedClientId) {
        creditUrClientDestroy({
            path: {id: selectedClientId},
            throwOnError: true,
        })
            .then((response) => {
                message.info('Клиент успешно удален!')
                loadUrClients()
                checkedRowKeysRef.value = [];
            })
            .catch((err) => {
                console.error(err)
                message.error('При удалении Юридического лица произошла ошибка!')
            })
    }
}

function editUrClient(data: PatchedUrClientRequest) {
    const selectedClientId = selectedUrClient?.value?.id;
    if (selectedClientId) {
        creditUrClientPartialUpdate({
            path: {id: selectedClientId},
            body: data,
            throwOnError: true,
        })
            .then((response) => {
                message.info('Данные клиента изменены!')
                loadUrClients()
                changeUrClientDialog.value = false;
            })
            .catch((err) => {
                console.error(err)
                message.error('При изменении Юридического лица произошла ошибка!')
            })
    }
}

function createUrClientCredit(credit: CreditRequest, pledge?: PledgeRequest) {
    if (selectedUrClient.value) {
        creditCreditCreate({
            body: {
                ...credit,
                ur_client: selectedUrClient.value.id,
            },
            throwOnError: true,
        })
            .then(async (response) => {
                message.info(`Кредит для юридического лица с ОГРН ${selectedUrClient.value?.ogrn} успешно выдан!`)
                if (pledge) {
                    await creditPledgeCreate({
                        body: {
                            ...pledge,
                            credit: response.data?.id as number,
                        }
                    })
                        .then((response) => {
                            loadUrClients()
                        })
                        .catch((err) => {
                            console.error(err)
                            message.error(`При создании залога по кредиту с ID ${response.data.id} произошла ошибка!`)
                        })
                } else {
                    loadUrClients()
                }
            })
            .catch((err) => {
                console.error(err)
                message.error(`При выдаче кредита юридическому лицу с ОГРН ${selectedUrClient.value?.ogrn} произошла ошибка!`)
            })
            .finally(() => createCreditDialog.value = false)
    }
}

</script>