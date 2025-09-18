from datetime import timedelta, date as datetime_date

from django.db import transaction
from django.utils import timezone
from credit.models import Credit, CreditPayment, CreditPayoff


def create_credit_payments(credit: Credit):
    term = credit.term
    credit_base = credit.totalbase
    yearly_percents = credit.yearlypercents
    today = credit.created_at.date()
    
    monthly_percents=yearly_percents / 100 / 12                                                    #Из процентов в доли? на месяц
    total_payment=(credit_base*monthly_percents)/(1-1/((1+monthly_percents)**term))                #Ежемесячный платеж
    total_payment=max(0,round(total_payment,2))                                                     #Округляем до копеек
    payments_list=[]
    cur_day_increment=today
    cur_credit_base_decrement=credit_base
    for i in range(term):        
        periodstart=cur_day_increment
        cur_day_increment=cur_day_increment+timedelta(days=29)
        periodend=cur_day_increment
        cur_day_increment=cur_day_increment+timedelta(days=1)
        curCreditBaseAtStart=max(0,cur_credit_base_decrement)
        curPercents=max(0,round(curCreditBaseAtStart*monthly_percents,2))
        curBasePayment=max(0,round(total_payment-curPercents,2))
        newPayment= CreditPayment.objects.create(
            credit=credit,
            periodStart=periodstart,
            periodEnd=periodend,
            baseatstart=curCreditBaseAtStart,
            totalpercents=curPercents,
            totalpayment=total_payment,
            totalbase=curBasePayment,
            unpaidpercents=curPercents,
            unpaidbase=curBasePayment,
            currentlyunpaid=total_payment,
        )
        cur_credit_base_decrement=max(0, round(cur_credit_base_decrement - curBasePayment, 2))
        payments_list.append(newPayment)

    #Считаем сумму по столбцу Уплата по базе
    sum_total_payment=0.0
    for i in payments_list:
        sum_total_payment = sum_total_payment + i.totalbase
    sum_total_payment = max(0, round(sum_total_payment, 2))
    difference = sum_total_payment - credit_base
    #Корректируем последний платеж по кредиту - все, что связано с базой, а также срочную уплату и невыплаченную сумму
    payments_list[-1].baseatstart = max(0, round(payments_list[-1].baseatstart-difference, 2))
    payments_list[-1].totalpayment = max(0, round(payments_list[-1].totalpayment-difference, 2))
    payments_list[-1].unpaidbase = max(0, round(payments_list[-1].unpaidbase-difference, 2))
    payments_list[-1].totalbase = max(0, round(payments_list[-1].totalbase-difference, 2))
    payments_list[-1].currentlyunpaid = max(0, round(payments_list[-1].currentlyunpaid-difference, 2))
    payments_list[-1].save()


def update_credit_payments_payment_early(credit: Credit, remainder:float, payments: list[CreditPayment]):
    term = len(payments)    
    credit_base = payments[0].baseatstart - remainder
    retval = -credit_base if credit_base < 0 else 0
    credit_base = max(0, credit_base)
    yearly_percents = credit.yearlypercents
    
    monthly_percents=yearly_percents / 100 / 12                                                    #Из процентов в доли? на месяц
    total_payment=(credit_base*monthly_percents)/(1-1/((1+monthly_percents)**term))                #Ежемесячный платеж
    total_payment=max(0,round(total_payment,2))                                                     #Округляем до копеек
    
    cur_credit_base_decrement=credit_base
    for payment in payments:     
        curCreditBaseAtStart=max(0,cur_credit_base_decrement)
        curPercents=max(0,round(curCreditBaseAtStart*monthly_percents,2))
        curBasePayment=max(0,round(total_payment-curPercents,2))

        payment.baseatstart=curCreditBaseAtStart
        payment.totalpercents=curPercents
        payment.totalpayment=total_payment
        payment.totalbase=curBasePayment
        payment.unpaidpercents=curPercents
        payment.unpaidbase=curBasePayment
        payment.currentlyunpaid=total_payment
        payment.save()

        cur_credit_base_decrement=max(0, round(cur_credit_base_decrement - curBasePayment, 2))

    #Считаем сумму по столбцу Уплата по базе
    sum_total_payment=0.0
    for payment in payments: 
        sum_total_payment = sum_total_payment + payment.totalbase
    sum_total_payment = max(0, round(sum_total_payment, 2))
    difference = sum_total_payment - credit_base
    #Корректируем последний платеж по кредиту - все, что связано с базой, а также срочную уплату и невыплаченную сумму
    payments[-1].baseatstart = max(0, round(payments[-1].baseatstart-difference, 2))
    payments[-1].totalpayment = max(0, round(payments[-1].totalpayment-difference, 2))
    payments[-1].unpaidbase = max(0, round(payments[-1].unpaidbase-difference, 2))
    payments[-1].totalbase = max(0, round(payments[-1].totalbase-difference, 2))
    payments[-1].currentlyunpaid = max(0, round(payments[-1].currentlyunpaid-difference, 2))
    payments[-1].save()

    return retval


def calculate_pennies(credit_payment: CreditPayment, date: datetime_date):
    period_end = credit_payment.periodEnd
    last_update_date = credit_payment.updatedate.date()
    if (date > period_end) and (date > last_update_date):
        diff = min((date - period_end).days, (date - last_update_date).days)
        pennies = diff * credit_payment.credit.dailypennies * (credit_payment.unpaidbase + credit_payment.unpaidpercents) / 100
        return pennies
    return 0


def check_if_penny_update_needed(credit_payment: CreditPayment):    
    return (credit_payment.unpaidbase + credit_payment.unpaidpercents) > 0


def check_if_credit_is_fully_paid(credit_payment: CreditPayment):    
    return (credit_payment.currentlyunpaid<=0)


def update_credit_payments_pennies(credit_payment: CreditPayment, date: datetime_date):
    if not check_if_penny_update_needed(credit_payment):
        return
    
    pennies=calculate_pennies(credit_payment, date=date)
    if pennies:
        credit_payment.unpaidpennies=round(pennies+credit_payment.unpaidpennies,2)
        credit_payment.totalpayment=round(pennies+credit_payment.totalpayment,2)
        credit_payment.totalpennies=round(pennies+credit_payment.totalpennies,2)
        credit_payment.currentlyunpaid=round(pennies+credit_payment.currentlyunpaid,2)
        credit_payment.updatedate=date
        credit_payment.save()
    

def update_credit_pennies(credit: Credit, date: datetime_date):
    for payment in credit.payments.all():
        update_credit_payments_pennies(payment, date=date)


def update_credit_payment_currents(payment:CreditPayment):
    payment.currentlyunpaid=round(payment.unpaidbase+payment.unpaidpercents+payment.unpaidpennies,2)
    payment.currentlypaid=round(payment.paidbase+payment.paidpercents+payment.paidpennies,2)
    payment.save()


def create_credit_payment_payoff(credit: Credit, payoff_amount: float, date: datetime_date) -> tuple[CreditPayoff, float]:
    with transaction.atomic():
        update_credit_pennies(credit, date)

        remainder=payoff_amount
        payoff_base_scheduled=0
        payoff_base_early=0
        payoff_percents=0
        payoff_pennies=0

        # Ищем задолжности
        outdated_unpaid_payments = credit.payments.filter(periodEnd__lt=date, currentlyunpaid__gt=0).order_by('periodStart')

        # 6 распределяем выплату по процентам задолжностей
        for payment in outdated_unpaid_payments:
            if payment.unpaidpercents<=0:
                continue
            if remainder<=0:
                break
            payment_amount=min(remainder, payment.unpaidpercents)
            payoff_percents += payment_amount
            payment.unpaidpercents=round(payment.unpaidpercents-payment_amount,2)
            payment.paidpercents=round(payment.paidpercents+payment_amount,2)
            payment.save()
            update_credit_payment_currents(payment)
            remainder=remainder-payment_amount

        # 7 распределяем остаток по основному долгу задолжностей
        for payment in outdated_unpaid_payments:
            if payment.unpaidbase<=0:
                continue
            if remainder<=0:
                break
            payment_amount=min(remainder,payment.unpaidbase)
            payoff_base_scheduled += payment_amount
            payment.unpaidbase=round(payment.unpaidbase-payment_amount,2)
            payment.paidbase=round(payment.paidbase+payment_amount,2)
            payment.save()
            update_credit_payment_currents(payment)
            remainder=remainder-payment_amount

        # 8, 9 Распределяем остаток по процентам, начисленным за текущий период
        # а также распределяем остаток по основному долгу за текущий период
        current_period_payment = credit.payments.filter(periodStart__lte=date, periodEnd__gte=date, currentlyunpaid__gt=0).first()

        if current_period_payment is not None:
            if current_period_payment.unpaidpercents > 0 and remainder > 0:
                payment_amount=min(remainder, current_period_payment.unpaidpercents)
                payoff_percents += payment_amount
                current_period_payment.unpaidpercents=round(current_period_payment.unpaidpercents - payment_amount,2)
                current_period_payment.paidpercents=round(current_period_payment.paidpercents + payment_amount,2)
                current_period_payment.save()
                update_credit_payment_currents(current_period_payment)
                remainder=remainder-payment_amount

            if current_period_payment.unpaidbase > 0 and remainder > 0:
                payment_amount=min(remainder,current_period_payment.unpaidbase)
                payoff_base_scheduled += payment_amount
                current_period_payment.unpaidbase=round(current_period_payment.unpaidbase-payment_amount,2)
                current_period_payment.paidbase=round(current_period_payment.paidbase+payment_amount,2)
                current_period_payment.save()
                update_credit_payment_currents(current_period_payment)
                remainder=remainder-payment_amount

        # 10 Распределяем остаток на пени
        payments_with_pennies = credit.payments.filter(periodEnd__lt=date, currentlyunpaid__gt=0).order_by('periodStart')
        for payment in payments_with_pennies:
            if payment.unpaidpennies<=0:
                continue
            if remainder<=0:
                break
            payment_amount=min(remainder,payment.unpaidpennies)
            payoff_pennies += payment_amount
            payment.unpaidpennies=round(payment.unpaidpennies-payment_amount,2)
            payment.paidpennies=round(payment.paidpennies+payment_amount,2)
            payment.save()
            update_credit_payment_currents(payment)
            remainder=remainder-payment_amount
        
        retval = remainder

        # 11 Проверяем остались ли еще платежи
        if remainder > 0:
            future_payments = credit.payments.filter(periodStart__gt=date, currentlyunpaid__gt=0).order_by('periodStart')
            if len(future_payments):
                retval = update_credit_payments_payment_early(credit=credit, remainder=remainder, payments=list(future_payments))
                if not retval:
                    payoff_base_early += remainder
                else:
                    payoff_base_early += remainder - retval

        payoff_instance = CreditPayoff.objects.create(
            credit=credit,
            penniespayment=round(payoff_pennies, 2),
            percentspayment=round(payoff_percents, 2),
            basepaymentscheduled=round(payoff_base_scheduled, 2),
            basepaymentearly=round(payoff_base_early, 2),
            totalPayment=round(payoff_amount-retval, 2),
        )

        return payoff_instance, retval
