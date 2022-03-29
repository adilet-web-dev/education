from django.urls import path

from .api.views import (
    AppSubscriptionPaymentAPI,
    ConfirmAppSubscriptionPaymentAPI,
    CoursePurchaseAPI,
    ConfirmCoursePurchaseAPI
)

urlpatterns = [
    path("subscribe&mode=<str:mode>/", AppSubscriptionPaymentAPI.as_view()),
    path("purchase-course/", CoursePurchaseAPI.as_view()),
    path("confirm-course-purchase/", ConfirmCoursePurchaseAPI.as_view()),
    path("confirm-subscription/", ConfirmAppSubscriptionPaymentAPI.as_view())
]
