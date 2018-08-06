import datetime
from datetime import datetime as dt

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sns_kanri.sns.filter import RecordFilter
from sns_kanri.sns.models import SNS, Rate, Record, Statistic, Time
from sns_kanri.sns.pagination import StandardResultsSetPagination
from sns_kanri.sns.serializer import (
    RateSerializer, RecordOutputSerializer, RecordSerializer, SNSSerializer,
    StatisticSerializer, TimeSerializer,
)
from sns_kanri.utils import date_range, get_total_time


class SNSViewSet(viewsets.ModelViewSet):
    """SNSのview_set"""
    permission_classes = (IsAuthenticated,)
    serializer_class = SNSSerializer
    queryset = SNS.objects.filter(enabled=True)

    def get_queryset(self):
        key = self.request.GET.get(key="all", default=None)
        queryset = super().get_queryset()
        if key:
            return queryset
        return queryset.filter(enabled=True)

    def get_queryset(self):
        key = self.request.GET.get(key="all", default=None)
        queryset = super().get_queryset()
        if key:
            return queryset
        return queryset.filter(enabled=True)


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


class RecordOutputViewSet(viewsets.ModelViewSet):
    """RecordOutputの一覧"""
    permission_classes = (IsAuthenticated,)
    filter_class = RecordFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = RecordOutputSerializer
    queryset = Record.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class StatisticView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    filter_class = RecordFilter

    def get_queryset(self):
        self.start_date = self.get_date("date_0")
        self.end_date = self.get_date("date_1")
        if self.start_date and self.end_date:
            return Record.objects.filter(
                user=self.request.user,
                date__gte=self.start_date,
                date__lte=self.end_date
            ).select_related()
        return Record.objects.filter(
            user=self.request.user).select_related()

    def get(self, request, *args, **kwargs):
        results = {}

        queryset = self.filter_queryset(self.get_queryset())
        sns_queryset = SNS.objects.all()

        if self.start_date and self.end_date:
            statistic_list = []
            for date in date_range(self.start_date, self.end_date):
                sns_list = []
                date_records = queryset.filter(date=date)
                for sns in sns_queryset:
                    times = date_records.filter(sns=sns)
                    total_time = get_total_time(times)
                    sns_list.append(total_time / 3600)
                statistic_list.append(Statistic(date, sns_list))

            results['statistic'] = StatisticSerializer(statistic_list, many=True).data

            rate_list = []
            all_total_time = get_total_time(queryset)

            for sns in sns_queryset:
                times = queryset.filter(sns=sns).values_list('time', flat=True)
                if not times:
                    continue
                times = map(lambda time: dt.combine(datetime.date.min, time) - dt.min, times)
                total_time = int(sum(times, datetime.timedelta()).total_seconds())
                rate_list.append(Rate(sns, (total_time / all_total_time) * 100))

            rate_list.sort(key=lambda rate: rate.num, reverse=True)
            results['rate'] = RateSerializer(rate_list, many=True).data

        return Response(results)

    def get_date(self, key):
        date = None
        date_str = self.request.GET.get(key=key, default=None)
        if date_str:
            date = dt.strptime(date_str, "%Y-%m-%d")
            date = datetime.date(date.year, date.month, date.day)
        return date


class TimeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Record.objects.filter(
            user=self.request.user,
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        today = datetime.date.today()
        month_queryset = queryset.filter(date__month=today.month)
        month_time = get_total_time(month_queryset) / 3600

        queryset = queryset.filter(date__gte=(today - datetime.timedelta(days=7)))
        week_time = get_total_time(queryset) / 3600

        queryset = queryset.filter(date=today)
        day_time = get_total_time(queryset) / 3600

        return Response(TimeSerializer(Time(day_time, week_time, month_time)).data)
