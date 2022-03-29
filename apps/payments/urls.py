from django.urls import path

from .api.views import AppSubscriptionPaymentAPI, ConfirmAppSubscriptionAPI

urlpatterns = [
    path("subscribe&mode=<str:mode>/", AppSubscriptionPaymentAPI.as_view()),
    path("confirm-subscription/", ConfirmAppSubscriptionAPI.as_view())
]
