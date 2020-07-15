from django.db import models
import pandas

TRANS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')


class Codal(models.Model):
    title = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
    filename = models.CharField(max_length=128)
    publish_date_time = models.DateTimeField()

    @property
    def download_link(self):
        return f'{self.filename}'

    @property
    def some_value(self):
        try:
            df = pandas.read_html(self.filename)[0]
            sood = int(df.loc[3][2].translate(TRANS).replace(',', ''))
            return sood
        except Exception:
            return 'bad'

    def __str__(self):
        return self.symbol
