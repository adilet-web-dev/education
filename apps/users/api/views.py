from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from .serializers import TemporaryUserSerializer, ProfileSerializer
from apps.users.models import User, TemporaryUser, Profile
from apps.courses.api.serializers import CourseSerializer


class RegisterUserAPIView(CreateAPIView):
    """
    1 step registration
    get email, username, password fields as usual, but saves it in TemporaryUser model
    It sends verification code to that email
    """
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
    """
    2 step registration
    checks verification code sent to user email, if it's True
    it creates regular User from temporary user
    """
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


class RetrieveUpdateProfileAPIView(RetrieveUpdateAPIView):
    """
    3 step registration and profile update
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserPurchasedCoursesListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.courses
