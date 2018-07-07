from django_filters import ChoiceFilter, DateFromToRangeFilter, FilterSet
from django_filters.widgets import RangeWidget

from sns_kanri.sns.models import Record


class RecordFilter(FilterSet):
    date = DateFromToRangeFilter(label='対象期間', widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Record
        fields = [
            'sns',
            'date',
            'time'
        ]
