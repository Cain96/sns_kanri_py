import datetime
from datetime import datetime as dt

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sns_kanri.sns.filter import RecordFilter
from sns_kanri.sns.models import SNS, Record, Statistic
from sns_kanri.sns.pagination import StandardResultsSetPagination
from sns_kanri.sns.serializer import (
    RecordSerializer, SNSSerializer, StatisticSerializer,
)
from sns_kanri.utils import date_range


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


class StatisticListView(generics.ListAPIView):
    """Statisticの一覧"""
    permission_classes = (IsAuthenticated,)
    filter_class = RecordFilter
    serializer_class = StatisticSerializer

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user).select_related()

    def get(self, request, *args, **kwargs):
        results = {}

        queryset = self.filter_queryset(self.get_queryset())
        sns_queryset = SNS.objects.all()
        start_date = self.get_date("date_0")
        end_date = self.get_date("date_1")
        statistic_list = []

        if start_date and end_date:
            for date in date_range(start_date, end_date):
                sns_list = []
                date_records = queryset.filter(date=date)
                for sns in sns_queryset:
                    times = date_records.filter(sns=sns).values_list('time', flat=True)
                    times = map(lambda time: dt.combine(datetime.date.min, time) - dt.min, times)
                    total_time = int(sum(times, datetime.timedelta()).total_seconds())
                    sns_list.append("{:.1f}".format(total_time / 3600))
                statistic_list.append(Statistic(date, sns_list))

        data = self.get_serializer(statistic_list, many=True).data
        results['statistic'] = data

        return Response(results)

    def get_date(self, key):
        date = None
        date_str = self.request.GET.get(key=key, default=None)
        if date_str:
            date = dt.strptime(date_str, "%Y-%m-%d")
            date = datetime.date(date.year, date.month, date.day)
        return date
