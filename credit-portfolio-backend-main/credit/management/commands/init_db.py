from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand

from credit.models import RatingAcra, RatingNcr, RatingNra, RatingExpert


ratings_acra=["Неизвестно","AAA(ru)","AA+(ru)","AA(ru)","AA-(ru)","A+(ru)","A(ru)","A-(ru)","BBB+(ru)","BBB(ru)","BBB-(ru)","BB+(ru)","BB(ru)","BB-(ru)","B+(ru)","B(ru)","B-(ru)","CCC(ru)","CC(ru)","C(ru)","SD(ru)","D(ru)"]
ratings_expert=["Неизвестно","ruAAA","ruAA+","ruAA","ruAA-","ruA+","ruA","ruA-","ruBBB+","ruBBB","ruBBB-","ruBB+","ruBB","ruBB-","ruB+","ruB","ruB-","ruCCC","ruCC","ruC","ruRD","ruD"]
ratings_ncr=["Неизвестно","AAA.ru","AA+.ru","AA.ru","AA-.ru","A+.ru","A.ru","A-.ru","BBB+.ru","BBB.ru","BBB-.ru","BB+.ru","BB.ru","BB-.ru","B+.ru","B.ru","B-.ru","CCC.ru","CC.ru","C.ru","D"]
ratings_nra=["Неизвестно","AAA|ru|","AA+|ru|","AA|ru|","AA-|ru|","A+|ru|","A|ru|","A-|ru|","BBB+|ru|","BBB|ru|","BBB-|ru|","BB+|ru|","BB|ru|","BB-|ru|","B+|ru|","B|ru|","B-|ru|","CCC|ru|","CC|ru|","C|ru|","RD|ru|","SD|ru|","D|ru|"]

model_rating_mappings = [
    {
        "model": RatingAcra,
        "values": ratings_acra,
    },
    {
        "model": RatingExpert,
        "values": ratings_expert,
    },
    {
        "model": RatingNcr,
        "values": ratings_ncr,
    },
    {
        "model": RatingNra,
        "values": ratings_nra,
    },
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for rating_model in model_rating_mappings:
            model = rating_model["model"]
            for rating in rating_model["values"]:
                print(f"Создание рейтинга {rating} модели {model.__name__}")
                model.objects.create(value=rating)
