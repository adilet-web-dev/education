from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=["POST"], detail=True)
    def subscribe(self, request, pk=None):
        user = self.get_object()
        user.profile.subscribers.add(request.user.profile)

        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def unsubscribe(self, request, pk=None):
        user = self.get_object()
        user.profile.subscribers.remove(request.user.profile)

        return Response(status=status.HTTP_200_OK)
