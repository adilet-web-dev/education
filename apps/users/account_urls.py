from django.urls import path
from .api.views import RetrieveUpdateProfileAPI, UserPurchasedCoursesListAPI


urlpatterns = [
    path("profile/", RetrieveUpdateProfileAPI.as_view()),
    path("courses/", UserPurchasedCoursesListAPI.as_view())
]