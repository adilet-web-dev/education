from django.urls import path
from .api.views import RetrieveUpdateProfileAPIView, UserPurchasedCoursesListAPIView


urlpatterns = [
    path("profile/", RetrieveUpdateProfileAPIView.as_view()),
    path("courses/", UserPurchasedCoursesListAPIView.as_view())
]