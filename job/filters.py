from datetime import date

import django_filters
from django_filters import CharFilter

from job.models import Position


class PositionFilter(django_filters.FilterSet):
    final_apply_date = CharFilter(method='filter_final_apply_date')

    class Meta:
        model = Position
        fields = ['final_apply_date']

    def filter_final_apply_date(self, queryset, name, value):
        if value.lower() == 'all':
            return queryset
        elif value.lower() == 'available':
            return queryset.filter(final_apply_date__gte=date.today())
        else:
            return queryset.none()
