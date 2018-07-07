from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from sns_kanri.sns.filter import RecordFilter
from sns_kanri.sns.models import SNS, Record
from sns_kanri.sns.pagination import StandardResultsSetPagination
from sns_kanri.sns.serializer import RecordSerializer, SNSSerializer


class SNSViewSet(viewsets.ModelViewSet):
    """SNSのview_set"""
    permission_classes = (IsAuthenticated,)
    serializer_class = SNSSerializer
    queryset = SNS.objects.all()


class RecordViewSet(viewsets.ModelViewSet):
    """Recordの一覧"""
    permission_classes = (IsAuthenticated,)
    filter_class = RecordFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = RecordSerializer
    queryset = Record.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
