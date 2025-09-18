from typing import Union
from django.db.models import Sum
from django.utils import timezone

from credit.models import UrClient, FizClient, Credit


def get_client_credit_statistics(
    client: Union["UrClient", "FizClient"],
) -> dict[str, float | int | bool | None]:
    stats = {
        "paidpercents": round(client.credits.aggregate(Sum("payments__paidpercents"))["payments__paidpercents__sum"] or 0, 2),
        "unpaidpercents": round(client.credits.aggregate(Sum("payments__unpaidpercents"))["payments__unpaidpercents__sum"] or 0, 2),
        "paidbase": round((client.credits.aggregate(Sum("payments__paidbase"))["payments__paidbase__sum"] or 0)+(client.credits.aggregate(Sum("payoffs__basepaymentearly"))["payoffs__basepaymentearly__sum"] or 0), 2),
        "unpaidbase": round(client.credits.aggregate(Sum("payments__unpaidbase"))["payments__unpaidbase__sum"] or 0, 2),
        "paidpennies": round(client.credits.aggregate(Sum("payments__paidpennies"))["payments__paidpennies__sum"] or 0, 2),
        "unpaidpennies": round(client.credits.aggregate(Sum("payments__unpaidpennies"))["payments__unpaidpennies__sum"] or 0, 2),
        "currentlypaid": round(client.credits.aggregate(Sum("payments__currentlypaid"))["payments__currentlypaid__sum"] or 0, 2),
        "currentlyunpaid": round(client.credits.aggregate(Sum("payments__currentlyunpaid"))["payments__currentlyunpaid__sum"] or 0, 2),
        "paid_payments": None,
        "unpaid_payments": None,
        "timestamp": timezone.now(),
    }
    return stats


def get_credit_statistics(credit: Credit) -> dict[str, float | int | bool | None]:
    stats = {
        "paidpercents": round(credit.payments.aggregate(Sum("paidpercents"))["paidpercents__sum"] or 0, 2),
        "unpaidpercents": round(credit.payments.aggregate(Sum("unpaidpercents"))["unpaidpercents__sum"] or 0, 2),
        "paidbase": round((credit.payments.aggregate(Sum("paidbase"))["paidbase__sum"] or 0) + (credit.payoffs.aggregate(Sum("basepaymentearly"))["basepaymentearly__sum"] or 0), 2),
        "unpaidbase": round(credit.payments.aggregate(Sum("unpaidbase"))["unpaidbase__sum"] or 0, 2),
        "paidpennies": round(credit.payments.aggregate(Sum("paidpennies"))["paidpennies__sum"] or 0, 2),
        "unpaidpennies": round(credit.payments.aggregate(Sum("unpaidpennies"))["unpaidpennies__sum"] or 0, 2),
        "currentlypaid": round(credit.payments.aggregate(Sum("currentlypaid"))["currentlypaid__sum"] or 0, 2),
        "currentlyunpaid": round(credit.payments.aggregate(Sum("currentlyunpaid"))["currentlyunpaid__sum"] or 0, 2),
        "paid_payments": credit.payments.filter(currentlyunpaid__lte=0).count(),
        "unpaid_payments": credit.payments.filter(currentlyunpaid__gt=0).count(),
        "timestamp": timezone.now(),
    }
    return stats
