from random import randint

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import ProfileSerializer, RegisterSerializer
from .models import UserProfile
from utils.send_message import adp_send_sms

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        verify_code = str(randint(10000, 99999))
        serializer.save(verify_code=verify_code)
        msg = render_to_string(
            'phone_verify.txt',
            context={
                'verify_code': verify_code,
            },
        )
        sent_message = adp_send_sms(serializer.data['phone_number'], msg)
        if not sent_message:
            raise ValidationError({'detail': 'Could not sent verification SMS'})


class ProfileAPIView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        instance = UserProfile.objects.select_related('user').get(user=self.request.user)
        return instance
