from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.http import Http404

from app_management.models import AppManagement
from .serializers import PaymentSerializer
from apps.payments.models import Payment
from apps.courses.models import Course


class AppSubscriptionPaymentAPI(CreateAPIView):
    """
    Creates payment object but not completed, must be confirmed by side payment service.
    query parameter must be either "base" or "pro"
    """
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
            name=f"subscription:{mode}",
            amount=amount
        )


class CoursePurchaseAPI(CreateAPIView):
    """
    Creates payment object but not completed, must be confirmed by side payment service.
    if course is free and user has base subscription user can have only 10 free courses per month
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self, request: Request, *args, **kwargs):
        course = self.get_course()
        profile = request.user.profile
        if course.cost == 0:

            on_base_subscription = profile.app_subscription_mode == "BASE"
            has_free_courses = profile.free_courses_number > 0
            has_no_subscription = profile.app_subscription_mode is None

            if has_no_subscription:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={"error": "to get free course user must have base or pro subscription"}
                )

            if on_base_subscription and not has_free_courses:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={"error": "with base subscription user can get only 10 free courses per month"}
                )

            profile.courses.add(course)
            profile.free_courses_number += 1
            profile.save()

            return Response(status=status.HTTP_200_OK)

        else:
            super(CoursePurchaseAPI, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        course = self.get_course()

        serializer.save(
            client=self.request.user,
            name=f"course:{course.id}",
            amount=course.cost
        )

    def get_course(self):
        course_id = self.request.data.get("course_id")
        if course_id is None:
            raise Http404

        course = get_object_or_404(Course, id=course_id)
        return course


class ConfirmCoursePurchaseAPI(APIView):
    """
    Payment confirmation by payment service and final execution of purchase,
    WARNING! Not integrated with any payment service
    if it's confirmed course will be available for user
    """
    def post(self, request: Request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=request.data.get("order_id"))
        try:
            course_id = int(payment.name.split(":")[1])
        except ValueError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Payment instance does not contain course id"}
            )

        course = get_object_or_404(Course, id=course_id)
        payment.client.profile.courses.add(course)
        payment.client.profile.save()
        payment.completed = True
        payment.save()

        return Response(status=status.HTTP_200_OK)


class ConfirmAppSubscriptionPaymentAPI(APIView):
    """
    Payment confirmation by payment service and final execution of subscription,
    WARNING! Not integrated with any payment service
    """
    def post(self, request: Request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=request.data.get("order_id"))
        profile = payment.client.profile
        if payment.name == "subscription:base":

            profile.app_subscription_mode = "BASE"
            profile.save()

        elif payment.name == "subscription:pro":

            profile.app_subscription_mode = "PRO"
            profile.save()

        payment.completed = True
        payment.save()

        return Response(status=status.HTTP_200_OK)
