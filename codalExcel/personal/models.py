from bs4 import BeautifulSoup
from django.db import models
from django.utils.html import format_html

TRANS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
ARAB_TRANS = str.maketrans('يك', 'یک')


class Symbol(models.Model):
    slug = models.CharField(max_length=128, unique=True)
    company_name = models.CharField(max_length=128)

    def __str__(self):
        return self.slug


class Codal(models.Model):
    title = models.CharField(max_length=128)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    filename = models.CharField(max_length=128)
    publish_date_time = models.DateTimeField()
    fund = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    forosh = models.CharField(max_length=128)
    sood_amaliyati = models.CharField(max_length=128)
    sood_khales = models.CharField(max_length=128)
    duration = models.CharField(max_length=128)
    year = models.CharField(max_length=128)

    @property
    def download_link(self):
        return f'{self.filename}'


    def __str__(self):
        return self.title
