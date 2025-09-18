<template>
    <n-card
        :title="title"
        :bordered="false"
        size="small"
        role="dialog"
        aria-modal="true"
    >
        <NTag v-if="!credit?.credit_statistics?.unpaid_payments" type="success" class="mb-2">
            Кредит погашен!
        </NTag>

        <div>
            <h2 class="text-lg">
                Платежи по кредиту
            </h2>
            <NDataTable
                :data="credit.payments"
                :columns="columns"
                :single-line="false"
                :row-key="(row) => row?.id"
                size="small"
                max-height="300px"
            />
        </div>

        <div class="mt-4">
            <h2 class="text-lg mb-2">
                История выплат по кредиту
            </h2>

            <NTimeline v-if="credit.payoffs?.length">
                <NTimelineItem
                    v-for="payoff in credit.payoffs"
                    :key="payoff.id"
                    :time="payoff.payoffTime"
                    type="success"
                >
                    {{ getPayoffContent(payoff) }}
                </NTimelineItem>
            </NTimeline>

            <div v-else>
                Выплаты по кредиту отсутствуют
            </div>
        </div>

        <div class="mt-4">
            <h2 class="text-lg">
                Залог
            </h2>

            <n-descriptions v-if="credit.pledges?.length" size="small" bordered>
                <n-descriptions-item label="Тип залога">
                    {{ credit?.pledges?.[0]?.vinCode ? 'Автомобиль' : 'Недвижимость' }}
                </n-descriptions-item>
                <n-descriptions-item v-if="credit?.pledges?.[0]?.vinCode" label="VIN-код автомобиля">
                    {{ credit?.pledges?.[0]?.vinCode }}
                </n-descriptions-item>
                <n-descriptions-item v-if="credit?.pledges?.[0]?.cadastralNumber" label="Кадастровый номер недвижимости">
                    {{ credit?.pledges?.[0]?.cadastralNumber }}
                </n-descriptions-item>
                <n-descriptions-item v-if="credit?.pledges?.[0]?.expectedPrice" label="Стоимость заложенного объекта, рублей">
                    {{ credit?.pledges?.[0]?.expectedPrice }}
                </n-descriptions-item>
            </n-descriptions>

            <div v-else>
                Залог отсутствует
            </div>
        </div>
    </n-card>
</template>

<script setup lang="ts">
import { computed, h } from 'vue';
import { NCard, NDataTable, NTimeline, NTimelineItem, NDescriptions, NDescriptionsItem, NTag, type DataTableColumn } from 'naive-ui';
import { type Credit, type CreditPayment, type CreditPayoff } from '@/api';

interface Props {
    credit: Credit;
    clientType: 'ur' | 'fiz';
}

const props = defineProps<Props>();

const columns: DataTableColumn<CreditPayment>[] = [
    {
        title: 'Платежный период',
        key: 'periodStart',
        render(row: CreditPayment) {
            return h('span', `${row.periodStart}-${row.periodEnd}`)
        },
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Величина долга на начало платежного периода',
        key: 'baseatstart',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Величина процентов за платежный период, к оплате',
        key: 'totalpercents',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Погашено процентов за платежный период',
        key: 'paidpercents',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Непогашенных процентов за платежный период',
        key: 'unpaidpercents',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Величина погашения основного долга, к оплате',
        key: 'totalbase',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Погашено основного долга за платежный период',
        key: 'paidbase',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Непогашено основного долга за платежный период',
        key: 'unpaidbase',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Величина пени за неуплату платежа по данному периоду',
        key: 'totalpennies',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Выплаченная пеня',
        key: 'paidpennies',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Невыплаченная пеня',
        key: 'unpaidpennies',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Всего погашено за данный период',
        key: 'currentlypaid',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Осталось погасить за данный период',
        key: 'currentlyunpaid',
        className: 'break-keep text-xs',
        align: 'center',
    },
    {
        title: 'Суммарный платеж за данный период',
        key: 'totalpayment',
        className: 'break-keep text-xs',
    },
]

const title = computed(() => {
    switch (props.clientType) {
        case 'ur':
            return `Выписка по кредиту № ${props.credit.uuid} юридическому лицу (ОГРН ${props.credit.ogrn})`
        case 'fiz':
            return `Выписка по кредиту № ${props.credit.uuid} физическому лицу (паспорт ${props.credit.passport})`
        default:
            break;
    }
})

function getPayoffContent(payoff: CreditPayoff) {
    let content = "";

    let penniesPayment = payoff.penniespayment;
    let percentPayment = payoff.percentspayment;
    let basePaymentScheduled = payoff.basepaymentscheduled;
    let basePaymentEarly = payoff.basepaymentearly;
    let totalPayment = payoff.totalPayment;

    content = content + "Выплата в размере "+totalPayment+" рублей. Было погашено ";

    let andFlag=false;

    if(penniesPayment!=0) {
        if(andFlag) {
            content=content+" и ";
        }
        content=content+penniesPayment+" рублей пеней";
        andFlag=true;
    }

    if(percentPayment!=0) {
        if(andFlag) {
            content=content+" и ";
        }
        content=content+percentPayment+" рублей процентов";
        andFlag=true;
    }

    if(basePaymentEarly!=0) {
        if(andFlag) {
            content=content+" и ";
        }
        content=content+basePaymentEarly+" рублей базы досрочно";
        andFlag=true;
    }

    if(basePaymentScheduled!=0) {
        if(andFlag) {
            content=content+" и ";
        }
        content=content+basePaymentScheduled+" рублей базы недосрочно";
        andFlag=true;
    }

    return content
}

</script>
