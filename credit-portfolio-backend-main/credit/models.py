import uuid

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from credit.services.rating import (
    calculate_ur_client_high_risk_zayceva,
    calculate_ur_client_high_risk_saifullin,
)


INFO_OUTDATED_DAYS = 365


class RatingAcra(models.Model):
    value = models.CharField(max_length=255, unique=True)


class RatingNra(models.Model):
    value = models.CharField(max_length=255, unique=True)


class RatingNcr(models.Model):
    value = models.CharField(max_length=255, unique=True)


class RatingExpert(models.Model):
    value = models.CharField(max_length=255, unique=True)


class UrClient(models.Model):
    ogrn=models.CharField(max_length=13, unique=True)

    ratingacra=models.ForeignKey(RatingAcra, on_delete=models.PROTECT, related_name="clients")
    ratingnra=models.ForeignKey(RatingNra, on_delete=models.PROTECT, related_name="clients")
    ratingncr=models.ForeignKey(RatingNcr, on_delete=models.PROTECT, related_name="clients")
    ratingexpert=models.ForeignKey(RatingExpert, on_delete=models.PROTECT, related_name="clients")

    str2300=models.BigIntegerField()
    str1300=models.BigIntegerField()
    str2400=models.BigIntegerField()
    str2110pred=models.PositiveBigIntegerField()

    str1520=models.PositiveBigIntegerField()
    str1230=models.PositiveBigIntegerField()
    str1510=models.PositiveBigIntegerField()
    str2110=models.PositiveBigIntegerField()
    str1250=models.PositiveBigIntegerField()
    str1400=models.PositiveBigIntegerField()
    str1500=models.PositiveBigIntegerField()
    str1600=models.PositiveBigIntegerField()
    str1100=models.PositiveBigIntegerField()
    str1200=models.PositiveBigIntegerField()
    str1550=models.PositiveBigIntegerField()
    str1600pred=models.PositiveBigIntegerField()
    infoupdatedate=models.DateTimeField(auto_now=True)

    @property
    def is_valid_info(self):
        diff = timezone.now() - self.infoupdatedate
        if diff.days > INFO_OUTDATED_DAYS:
            return False
        return True

    @property
    def high_risk_zayceva(self):
        return calculate_ur_client_high_risk_zayceva(self)
    
    @property
    def high_risk_saifullin(self):
        return calculate_ur_client_high_risk_saifullin(self)

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"


class FizClient(models.Model):
    passport=models.CharField(max_length=10, unique=True)    

    #nullable сведения о заёмщике
    nbkiRating=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MaxValueValidator(999),MinValueValidator(1)])
    okbRating=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MaxValueValidator(999),MinValueValidator(1)])
    bkiCreditInfoRating=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MaxValueValidator(999),MinValueValidator(1)])
    bkiSBRating=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MaxValueValidator(999),MinValueValidator(1)])
    dti=models.FloatField(blank=True,null=True)
    revolbal=models.FloatField(blank=True,null=True)
    mthssincerecentbc=models.PositiveIntegerField(blank=True,null=True)
    bcutil=models.FloatField(blank=True,null=True)
    revolutil=models.FloatField(blank=True,null=True)    
    
    #Non-nullable сведения о заёмщике
    annualinc=models.FloatField()
    avgcurbal=models.FloatField()
    totalacc=models.PositiveIntegerField()
    accopenpast24mths=models.PositiveIntegerField()
    totalbclimit=models.FloatField()
    totalilhighcreditlimit=models.FloatField()
    totalilrevhilim=models.FloatField()
    emplength=models.PositiveIntegerField()
    totalbalexmort=models.FloatField()
    bcopentobuy=models.FloatField()
    infoupdatedate=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"
    
    @property
    def is_valid_info(self):
        diff = timezone.now() - self.infoupdatedate
        if diff.days > INFO_OUTDATED_DAYS:
            return False
        return True


class Credit(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)

    term=models.PositiveSmallIntegerField(validators=[MaxValueValidator(999),MinValueValidator(0)])
    yearlypercents=models.FloatField()
    dailypennies=models.FloatField()
    totalbase=models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    ur_client = models.ForeignKey(UrClient, on_delete=models.CASCADE, related_name="credits", blank=True, null=True)
    fiz_client = models.ForeignKey(FizClient, on_delete=models.CASCADE, related_name="credits", blank=True, null=True)

    class Meta:
        verbose_name = "Кредит"
        verbose_name_plural = "Кредиты"
        constraints = [
            models.CheckConstraint(
                name="ur_client_or_fiz_client",
                check=(
                    Q(ur_client__isnull=True, fiz_client__isnull=False)
                    | Q(ur_client__isnull=False, fiz_client__isnull=True)
                ),
            ),
        ]


class Pledge(models.Model):
    vinCode=models.CharField(max_length=17, blank=True, null=True)
    cadastralNumber=models.CharField(max_length=28, blank=True, null=True)
    expectedPrice=models.PositiveBigIntegerField()
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name="pledges")
    
    class Meta:
        verbose_name = "Залог"
        verbose_name_plural = "Залоги"


class CreditPayment(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name="payments")
    periodStart=models.DateField()
    periodEnd=models.DateField()
    baseatstart=models.FloatField()
    totalpercents=models.FloatField()
    paidpercents=models.FloatField(default=0.0)
    unpaidpercents=models.FloatField()
    totalbase=models.FloatField()
    paidbase=models.FloatField(default=0.0)
    unpaidbase=models.FloatField()
    totalpennies=models.FloatField(default=0.0)
    paidpennies=models.FloatField(default=0.0)
    unpaidpennies=models.FloatField(default=0.0)
    currentlypaid=models.FloatField(default=0.0)
    currentlyunpaid=models.FloatField()
    totalpayment=models.FloatField()
    updatedate=models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Плановый платеж по кредиту"
        verbose_name_plural = "Плановые платежи по кредитам"


class CreditPayoff(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name="payoffs")
    penniespayment=models.FloatField(default=0.0)
    percentspayment=models.FloatField(default=0.0)
    basepaymentscheduled=models.FloatField(default=0.0)
    basepaymentearly=models.FloatField(default=0.0)
    totalPayment=models.FloatField(default=0.0)
    payoffTime=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Выплата по кредиту"
        verbose_name_plural = "Выплаты по кредитам"
