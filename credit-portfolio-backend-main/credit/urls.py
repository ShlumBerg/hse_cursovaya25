from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()


router.register(r"rating-acra", views.RatingAcraApiView)
router.register(r"rating-nra", views.RatingNraApiView)
router.register(r"rating-ncr", views.RatingNcrApiView)
router.register(r"rating-expert", views.RatingExpertApiView)

router.register(r"ur-client", views.UrClientApiView)
router.register(r"fiz-client", views.FizClientApiView)
router.register(r"credit", views.CreditApiView)
router.register(r"pledge", views.PledgeApiView)
router.register(r"credit-payment", views.CreditPaymentApiView)
router.register(r"credit-payoff", views.CreditPayoffApiView)


urlpatterns = [
    path("", include(router.urls)),
    path("create-credit-payoff/", views.create_credit_payoff),
    path("restructure-credit/", views.restructure_credit),
    path("check-fiz-client-creditworthiness/", views.check_fiz_client_creditworthiness),
]
