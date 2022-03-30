from django.urls import path

from .api.views import (
    RegisterUserAPI,
    VerifyEmailAPI,
    SearchUserListAPI
)


urlpatterns = [
    path("register/", RegisterUserAPI.as_view()),
    path("verify-email/", VerifyEmailAPI.as_view()),
    path("searce&name=<str:name>/", SearchUserListAPI.as_view()),
]
