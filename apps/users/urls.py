from django.urls import path

from .api.views import RegisterUserAPIView, VerifyEmailAPIView, RetrieveUpdateProfileAPIView


urlpatterns = [
    path("register/", RegisterUserAPIView.as_view()),
    path("verify-email/", VerifyEmailAPIView.as_view()),
]
