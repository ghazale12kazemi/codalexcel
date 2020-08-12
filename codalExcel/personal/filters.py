import django_filters
from django_filters import DateFilter
from .models import *


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Codal
        fields = '__all__'
        exclude = ['filename','title','publish_date_time','forosh','sood_amaliyati','sood_khales','duration']