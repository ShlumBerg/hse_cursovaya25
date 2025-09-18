from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import (
    RatingAcra,
    RatingNra,
    RatingNcr,
    RatingExpert,
    UrClient,
    FizClient,
    Pledge,
    Credit,
    CreditPayment,
    CreditPayoff,
)

from .serializers import (
    RatingAcraSerializer,
    RatingNraSerializer,
    RatingNcrSerializer,
    RatingExpertSerializer,
    UrClientSerializer,
    FizClientSerializer,
    CreditSerializer,
    PledgeSerializer,
    CreditPaymentSerializer,
    CreditPayoffSerializer,
    CreditPayoffCreateSerializer,
    CreditPayoffResultSerializer,
    CreditRestructureCreateSerializer,
    CreditworthinessCheckSerializer,
    CreditworthinessCheckResultSerializer,
)

from .filters import (
    UrClientFilter,
    FizClientFilter,
    CreditFilter,
    PledgeFilter,
    CreditPaymentFilter,
    CreditPayoffFilter,
)

from credit.services.payment import create_credit_payments, create_credit_payment_payoff
from credit.services.check_if_credible_fiz_client import check_if_credible_fiz_client


class RatingAcraApiView(viewsets.ModelViewSet):
    queryset = RatingAcra.objects.all()
    serializer_class = RatingAcraSerializer


class RatingNraApiView(viewsets.ModelViewSet):
    queryset = RatingNra.objects.all()
    serializer_class = RatingNraSerializer


class RatingNcrApiView(viewsets.ModelViewSet):
    queryset = RatingNcr.objects.all()
    serializer_class = RatingNcrSerializer


class RatingExpertApiView(viewsets.ModelViewSet):
    queryset = RatingExpert.objects.all()
    serializer_class = RatingExpertSerializer


class UrClientApiView(viewsets.ModelViewSet):
    queryset = UrClient.objects.all()
    serializer_class = UrClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UrClientFilter


class FizClientApiView(viewsets.ModelViewSet):
    queryset = FizClient.objects.all()
    serializer_class = FizClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FizClientFilter


class CreditApiView(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CreditFilter

    def perform_create(self, serializer):
        with transaction.atomic():
            instance = serializer.save()
            create_credit_payments(instance)


class PledgeApiView(viewsets.ModelViewSet):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PledgeFilter


class CreditPaymentApiView(viewsets.ModelViewSet):
    queryset = CreditPayment.objects.all()
    serializer_class = CreditPaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CreditPaymentFilter


class CreditPayoffApiView(viewsets.ModelViewSet):
    queryset = CreditPayoff.objects.all()
    serializer_class = CreditPayoffSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CreditPayoffFilter


@extend_schema(
    request=CreditPayoffCreateSerializer,
    responses=CreditPayoffResultSerializer,
)
@api_view(["POST"])
def create_credit_payoff(request):
    serializer = CreditPayoffCreateSerializer(data=request.data)
    if serializer.is_valid():
        credit = serializer.validated_data["credit"]
        payoff_amout = serializer.validated_data["payoff_amount"]
        payoff_instance, remainder = create_credit_payment_payoff(
            credit=credit,
            payoff_amount=payoff_amout,
            date=timezone.now().date(),
        )
        return Response(
            data={
                "credit_payoff": CreditPayoffSerializer(payoff_instance).data,
                "remainder": round(remainder, 2) or None,
            }
        )


@extend_schema(
    request=CreditRestructureCreateSerializer,
    responses=CreditSerializer,
)
@api_view(["POST"])
def restructure_credit(request):
    serializer = CreditRestructureCreateSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            old_credit: Credit = serializer.validated_data["credit"]

            new_credit = Credit(
                term=serializer.validated_data["term"],
                yearlypercents=serializer.validated_data["yearlypercents"],
                dailypennies=serializer.validated_data["dailypennies"],
                totalbase=serializer.validated_data["totalbase"],
                ur_client=old_credit.ur_client,
                fiz_client=old_credit.fiz_client,
            )
            
            new_credit.save()
            old_credit.delete()

            create_credit_payments(new_credit)

            return_serializer = CreditSerializer(new_credit, context=dict(request=request))
            return Response(data=return_serializer.data)


@extend_schema(
    request=CreditworthinessCheckSerializer,
    responses=CreditworthinessCheckResultSerializer,
)
@api_view(["POST"])
def check_fiz_client_creditworthiness(request):
    serializer = CreditworthinessCheckSerializer(data=request.data)
    if serializer.is_valid():
        fiz_client: FizClient = serializer.validated_data["fiz_client"]
        result = check_if_credible_fiz_client(
            fiz_client=fiz_client,
            int_rate=serializer.validated_data["yearlypercents"],
            funded_amnt=serializer.validated_data["totalbase"],
            term=serializer.validated_data["term"],
            date=timezone.now().date(),
        )
        return Response(data={"ok": result})
