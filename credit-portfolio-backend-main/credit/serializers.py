from rest_framework import serializers

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

from credit.services.statistics import get_client_credit_statistics, get_credit_statistics


class RatingAcraSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingAcra
        fields = "__all__"


class RatingNraSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingNra
        fields = "__all__"


class RatingNcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingNcr
        fields = "__all__"


class RatingExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingExpert
        fields = "__all__"


class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = "__all__"


class CreditPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPayment
        fields = "__all__"


class CreditPayoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPayoff
        fields = "__all__"

    
class CreditStatisticsSerializer(serializers.Serializer):
    paidpercents = serializers.FloatField(allow_null=True)
    unpaidpercents = serializers.FloatField(allow_null=True)
    paidbase = serializers.FloatField(allow_null=True)
    unpaidbase = serializers.FloatField(allow_null=True)
    paidpennies = serializers.FloatField(allow_null=True)
    unpaidpennies = serializers.FloatField(allow_null=True)
    currentlypaid = serializers.FloatField(allow_null=True)
    currentlyunpaid = serializers.FloatField(allow_null=True)
    paid_payments = serializers.IntegerField(allow_null=True)
    unpaid_payments = serializers.IntegerField(allow_null=True)
    timestamp = serializers.DateTimeField(allow_null=True)


class UrClientSerializer(serializers.ModelSerializer):
    ratingacra_detail = RatingAcraSerializer(read_only=True, source="ratingacra")
    ratingnra_detail = RatingNraSerializer(read_only=True, source="ratingnra")
    ratingncr_detail = RatingNcrSerializer(read_only=True, source="ratingncr")
    ratingexpert_detail = RatingExpertSerializer(read_only=True, source="ratingexpert")

    is_valid_info = serializers.BooleanField(read_only=True)

    high_risk_zayceva = serializers.BooleanField(read_only=True)
    high_risk_saifullin = serializers.BooleanField(read_only=True)

    credit_statistics = serializers.SerializerMethodField()

    class Meta:
        model = UrClient
        fields = "__all__"

    def get_credit_statistics(self, instance) -> CreditStatisticsSerializer:
        return get_client_credit_statistics(instance)


class FizClientSerializer(serializers.ModelSerializer):
    is_valid_info = serializers.BooleanField(read_only=True)

    credit_statistics = serializers.SerializerMethodField()

    class Meta:
        model = FizClient
        fields = "__all__"

    def get_credit_statistics(self, instance) -> CreditStatisticsSerializer:
        return get_client_credit_statistics(instance)


class CreditPayoffCreateSerializer(serializers.Serializer):
    payoff_amount = serializers.FloatField()
    credit = serializers.PrimaryKeyRelatedField(queryset=Credit.objects.all())


class CreditPayoffResultSerializer(serializers.Serializer):
    credit_payoff = CreditPayoffSerializer(read_only=True)
    remainder = serializers.FloatField(allow_null=True, read_only=True)


class CreditSerializer(serializers.ModelSerializer):
    ogrn = serializers.CharField(source="ur_client.ogrn", allow_null=True, read_only=True)
    passport = serializers.CharField(source="fiz_client.passport", allow_null=True, read_only=True)
    pledges = PledgeSerializer(many=True, read_only=True)
    payments = CreditPaymentSerializer(many=True, read_only=True)
    payoffs = CreditPayoffSerializer(many=True, read_only=True)

    credit_statistics = serializers.SerializerMethodField()

    ur_client_detail = UrClientSerializer(source="ur_client", allow_null=True, read_only=True)
    fiz_client_detail = FizClientSerializer(source="fiz_client", allow_null=True, read_only=True)

    class Meta:
        model = Credit
        fields = "__all__"

    def get_unpaid_payments(self, instance) -> list[int]:
        return instance.payments.filter(currentlyunpaid__gt=0).values_list('id', flat=True)
    
    def get_credit_statistics(self, instance) -> CreditStatisticsSerializer:
        return get_credit_statistics(instance)
    

class CreditRestructureCreateSerializer(serializers.Serializer):
    credit = serializers.PrimaryKeyRelatedField(queryset=Credit.objects.all())
    term = serializers.IntegerField()
    yearlypercents = serializers.FloatField()
    dailypennies = serializers.FloatField()
    totalbase = serializers.FloatField()


class CreditworthinessCheckSerializer(serializers.Serializer):
    fiz_client = serializers.PrimaryKeyRelatedField(queryset=FizClient.objects.all())
    term = serializers.IntegerField()
    yearlypercents = serializers.FloatField()
    dailypennies = serializers.FloatField(required=False, allow_null=True)
    totalbase = serializers.FloatField()


class CreditworthinessCheckResultSerializer(serializers.Serializer):
    ok = serializers.BooleanField()
