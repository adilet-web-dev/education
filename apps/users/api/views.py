from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from .serializers import TemporaryUserSerializer
from apps.users.models import User, TemporaryUser


class RegisterUserAPIView(CreateAPIView):
    serializer_class = TemporaryUserSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_already_exists = User.objects.filter(email=request.data["email"]).exists()
        if email_already_exists:
            data = {"message": "email already exists"}
            return Response(status=status.HTTP_403_FORBIDDEN, data=data)

        temp_user = serializer.save()

        try:
            status_code = send_mail(
                _("Verify your email"),
                _(f"Verification code: {temp_user.verification_code}"),
                None,
                [temp_user.email]
            )
        except:  # there is more than one exceptions that I don't know, so let's catch all
            temp_user.delete()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if status_code == 1:
            return Response(status=status.HTTP_200_OK)

        else:
            temp_user.delete()
            data = {"message": "email does not exist"}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)


class VerifyEmailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        temp_user = get_object_or_404(TemporaryUser, email=request.data.get("email"))
        if request.data.get("verification_code") == temp_user.verification_code:
            data = TemporaryUserSerializer(temp_user).data
            User.objects.create_user(**data)
            temp_user.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            data = {"message": _("wrong verification code")}
            return Response(status=status.HTTP_403_FORBIDDEN, data=data)