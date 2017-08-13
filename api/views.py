from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from registration.models import State
from registration.serializers import StateSerializer


class StateAPIView(generics.ListAPIView):
    """
    Return states and their cities.
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
