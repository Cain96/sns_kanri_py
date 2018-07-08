from django_filters import DateFromToRangeFilter, FilterSet, TimeRangeFilter
from django_filters.widgets import RangeWidget

from sns_kanri.sns.models import Record


class RecordFilter(FilterSet):
    date = DateFromToRangeFilter(label='対象期間', widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))
    time = TimeRangeFilter(label='対象時間', widget=RangeWidget(attrs={'placeholder': 'hh:mm'}))

    class Meta:
        model = Record
        fields = [
            'sns',
            'date',
            'time'
        ]
