from django.urls import path
from .api.views import RetrieveUpdateProfileAPIView


urlpatterns = [
    path("profile/", RetrieveUpdateProfileAPIView.as_view())
]