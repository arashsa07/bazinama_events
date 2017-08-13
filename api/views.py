from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from registration.models import State
from registration.serializers import StateSerializer


class StateViewSet(ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
