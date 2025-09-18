import django_filters

from .models import (
    UrClient,
    FizClient,
    Credit,
    Pledge,
    CreditPayment,
    CreditPayoff,
)


class UrClientFilter(django_filters.FilterSet):
    class Meta:
        fields = ["ogrn"]
        model = UrClient


class FizClientFilter(django_filters.FilterSet):
    class Meta:
        fields = ["passport"]
        model = FizClient


class CreditFilter(django_filters.FilterSet):
    ur_clients_only = django_filters.BooleanFilter("fiz_client", lookup_expr="isnull")
    fiz_clients_only = django_filters.BooleanFilter("ur_client", lookup_expr="isnull")

    class Meta:
        fields = [
            "id",
            "uuid",
            "ur_client",
            "ur_client__ogrn",
            "fiz_client",
            "fiz_client__passport",
            "ur_clients_only",
            "fiz_clients_only",
        ]
        model = Credit


class PledgeFilter(django_filters.FilterSet):
    class Meta:
        fields = ["credit"]
        model = Pledge


class CreditPaymentFilter(django_filters.FilterSet):
    class Meta:
        fields = ["credit"]
        model = CreditPayment


class CreditPayoffFilter(django_filters.FilterSet):
    class Meta:
        fields = ["credit"]
        model = CreditPayoff
