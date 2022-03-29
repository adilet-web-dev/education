from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404

from data_management.models import AppManagement
from .serializers import PaymentSerializer
from apps.payments.models import Payment
from apps.courses.models import Course


class AppSubscriptionPaymentAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        am = AppManagement.get_solo()

        mode = self.kwargs['mode']
        amount = 0
        if mode == "base":
            amount = am.base_subscription_price
        else:
            amount = am.pro_subscription_price

        serializer.save(
            client=self.request.user,
            datetime=timezone.now(),
            name=f"subscription:{mode}",
            amount=amount
        )


class CoursePurchaseAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer


class ConfirmAppSubscriptionAPI(APIView):
    def post(self, request: Request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=request.data["order_id"])
        profile = payment.client.profile
        if payment.name == "subscription:base":

            profile.app_subscription_mode = "BASE"
            profile.save()

        elif payment.name == "subscription:pro":

            profile.app_subscription_mode = "PRO"
            profile.save()

        return Response(status=status.HTTP_200_OK)
